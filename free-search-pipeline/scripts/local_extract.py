import sys
import asyncio
import httpx
from readability import Document
from bs4 import BeautifulSoup
import subprocess
import os
import json
import shutil

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}

# ──────────────────────────────────────────────
# 루나 추가 2026-10-28 — Phase 2.6 크롤러 UA
#   Threads·Instagram·X 등은 일반 UA 에는 JS 셸만 주고,
#   크롤러(링크 프리뷰) UA 에는 og:/twitter: 메타태그를 내준다.
#   Jina(2.5)가 제목만 줄 때 여기서 본문을 건진다. 외부 전송 없음(로컬).
# ──────────────────────────────────────────────
CRAWLER_UAS = [
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)",
    "WhatsApp/2.23",
]


def parse_og_meta(html_text: str) -> dict:
    """og:/twitter: 메타태그를 dict 로 추출 (HTML 엔티티 디코드)."""
    import html as _html
    import re as _re
    out: dict[str, str] = {}
    for a, b in _re.findall(
        r'<meta[^>]+(?:property|name)=["\'](?:og|twitter):([a-z_]+)["\'][^>]*?content=["\']([^"\']*)',
        html_text, _re.I,
    ):
        out.setdefault(a.lower(), _html.unescape(b))
    for a, b in _re.findall(
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]*?(?:property|name)=["\'](?:og|twitter):([a-z_]+)["\']',
        html_text, _re.I,
    ):
        out.setdefault(b.lower(), _html.unescape(a))
    return out

# ──────────────────────────────────────────────
# LLM 후처리 프롬프트 (한글 노이즈 제거용)
# ──────────────────────────────────────────────
KOREAN_NOISE_CLEAN_PROMPT = """다음 텍스트는 웹페이지에서 추출한 원문입니다. 네비게이션 바, 사이드바, 푸터, 광고, 쿠키 배너 등 본문이 아닌 노이즈를 제거하고, **실제 기사/본문 내용만 깔끔하게 정리**해 주세요.

규칙:
1. 본문과 무관한 메뉴/링크/버튼 텍스트 제거
2. 반복되는 헤더/푸터/사이드바 문구 제거
3. 광고/쿠키/구독 유도 문구 제거
4. 본문 단락 구조 유지 (문단 구분 유지)
5. 한국어 자연스러운 문장으로 정리
6. 출처 URL, 저작권 표기 등은 마지막에 한 줄로만 남김

원문:
{text}

정제된 본문:"""

async def clean_korean_content(text: str, agent_llm=None) -> str:
    """
    추출된 텍스트를 LLM으로 정제 (한글 노이즈 제거)
    agent_llm: 에이전트가 가진 LLM 호출 함수 (None이면 원문 반환)
    """
    if agent_llm is None or len(text) < 200:
        return text
    
    try:
        prompt = KOREAN_NOISE_CLEAN_PROMPT.format(text=text[:8000])
        cleaned = await agent_llm(prompt)
        if cleaned and len(cleaned) > 100:
            return cleaned.strip()
    except Exception:
        pass
    return text

async def extract_url(url: str, max_chars: int = 4000, agent_llm=None) -> dict:
    """
    Extract article content from a URL using 100% free local tools.
    1. Local httpx + readability (Fast & 0-cost)
    2. Fallback to insane-extract if blocked (403/WAF)
    3. Fallback to Wayback Archive
    4. Optional: LLM post-processing for Korean noise cleanup
    """
    url = url.strip()
    if not url.startswith("http"):
        url = "https://" + url

    # Phase 1: Local HTTP + Readability
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, headers=HEADERS) as client:
            resp = await client.get(url)
            if resp.status_code == 200 and len(resp.text) > 200:
                doc = Document(resp.text)
                title = doc.title()
                summary_html = doc.summary()
                soup = BeautifulSoup(summary_html, "html.parser")
                text = soup.get_text("\n", strip=True)
                if len(text) > 100:
                    # LLM 후처리: 한글 노이즈 제거 (에이전트가 LLM 제공 시)
                    cleaned_text = await clean_korean_content(text, agent_llm)
                    return {
                        "status": "success",
                        "method": "local_readability",
                        "url": url,
                        "title": title,
                        "content": cleaned_text[:max_chars]
                    }
    except Exception as e:
        pass

    # Phase 2: Insane Extract CLI (TLS Impersonation / WAF Bypass)
    # 루나 패치 2026-10-28: 경로 하드코딩 제거 (환경변수 → PATH → 홈 기준 순서)
    insane_cli = (
        os.environ.get("INSANE_EXTRACT_BIN")
        or os.path.join(os.path.expanduser("~"), ".local/bin/insane-extract")
    )
    if os.path.exists(insane_cli):
        try:
            res = subprocess.run([insane_cli, url], capture_output=True, text=True, timeout=15)
            if res.returncode == 0 and len(res.stdout.strip()) > 100:
                # Insane 결과도 LLM 후처리
                cleaned_text = await clean_korean_content(res.stdout.strip(), agent_llm)
                return {
                    "status": "success",
                    "method": "insane_extract_waf_bypass",
                    "url": url,
                    "title": "",
                    "content": cleaned_text[:max_chars]
                }
        except Exception:
            pass

    # Phase 2.5: 크롤러 UA 재시도 (og:/twitter: 메타태그) — 루나 추가 2026-10-28
    #   ★ Jina(2.6)보다 반드시 먼저 돈다. 이유 2가지:
    #     ① 로컬에서 끝난다(외부 전송 없음) → 프라이버시 우선
    #     ② Jina는 Threads 같은 페이지에서 네비게이션만 물어와 "성공"으로 오판한다
    #   Threads·Instagram·X 등은 일반 UA에 JS 셸만 주고, 크롤러(링크 프리뷰) UA에는
    #   og: 메타태그를 내준다. og:description이 비면 og:image URL을 넘겨 이미지 판독으로 연결.
    for _cua in CRAWLER_UAS:
        try:
            async with httpx.AsyncClient(
                timeout=15.0, follow_redirects=True,
                headers={"User-Agent": _cua, "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8"},
            ) as client:
                resp = await client.get(url)
            if resp.status_code != 200 or len(resp.text) < 500:
                continue
            og = parse_og_meta(resp.text)
            _title = og.get("title", "")
            _desc = og.get("description", "")
            _img = og.get("image", "")
            if not (_title or _desc):
                continue
            # 제목만 있고 본문이 없으면 이미지 판독으로 넘긴다
            body = _desc
            if not body and _img:
                body = (
                    f"[og:image] {_img}\n"
                    "→ 본문이 이미지에 있습니다. view_image 로 판독하십시오."
                )
            if not body.strip():
                continue
            return {
                "status": "success",
                "method": "crawler_ua_og",
                "url": og.get("url", url),
                "title": _title,
                "content": f"{_title}\n\n{body}".strip()[:max_chars],
            }
        except Exception:
            continue

    # Phase 2.6: Agent Reach 읽기 (Jina 백엔드) — JS 렌더링·WAF 페이지용 최후 수단
    #   Threads·인스타그램처럼 본문이 스크립트로만 그려지는 페이지는
    #   1·2단계로 못 읽는다. agent-reach 가 설치돼 있으면 여기서 뚫린다.
    reach_bin = (
        os.environ.get("AGENT_REACH_BIN")
        or shutil.which("agent-reach")
        or os.path.join(os.path.expanduser("~"), ".local", "bin", "agent-reach")
    )
    # --no-reach 로 끌 수 있다. Jina 는 URL 을 외부 서버로 넘기므로
    # 사내 문서·개인정보 페이지에는 쓰지 않는다.
    _no_reach = os.environ.get("FREE_SEARCH_NO_REACH", "").lower() in ("1", "true", "yes")
    if reach_bin and os.path.exists(reach_bin) and not _no_reach:
        try:
            res = await asyncio.to_thread(
                subprocess.run,
                [reach_bin, "web", "read", url],
                capture_output=True, text=True, timeout=120,
            )
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout.strip().splitlines()[-1])
                items = data.get("items") or []
                if data.get("ok") and items:
                    raw = items[0].get("text") or ""
                    if len(raw.strip()) > 100:
                        cleaned_text = await clean_korean_content(raw.strip(), agent_llm)
                        return {
                            "status": "success",
                            "method": f"agent_reach_{data.get('backend', 'read')}",
                            "url": url,
                            "title": items[0].get("title", ""),
                            "content": cleaned_text[:max_chars]
                        }
        except Exception:
            pass

    # Phase 3: Wayback Archive Fallback
    try:
        wayback_api = f"https://archive.org/wayback/available?url={url}"
        async with httpx.AsyncClient(timeout=8.0, headers=HEADERS) as client:
            wb_resp = await client.get(wayback_api)
            if wb_resp.status_code == 200:
                wb_data = wb_resp.json()
                closest = wb_data.get("archived_snapshots", {}).get("closest", {})
                if closest.get("available") and closest.get("url"):
                    snap_url = closest["url"]
                    snap_resp = await client.get(snap_url)
                    if snap_resp.status_code == 200:
                        doc = Document(snap_resp.text)
                        soup = BeautifulSoup(doc.summary(), "html.parser")
                        text = soup.get_text("\n", strip=True)
                        # Wayback 결과도 LLM 후처리
                        cleaned_text = await clean_korean_content(text, agent_llm)
                        return {
                            "status": "success",
                            "method": "wayback_snapshot",
                            "url": url,
                            "title": doc.title() + " (Archived)",
                            "content": cleaned_text[:max_chars]
                        }
    except Exception:
        pass

    return {
        "status": "error",
        "method": "failed",
        "url": url,
        "content": "페이지 내용을 추출하지 못했습니다."
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 local_extract.py <URL>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    res = asyncio.run(extract_url(target_url))
    print(f"=== [{res['method'].upper()}] {res.get('title', '')} ===")
    print(res["content"])
