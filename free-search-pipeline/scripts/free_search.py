#!/usr/bin/env python3
import os
import sys

# 에이전트(execute_code 등)가 PYTHONPATH 를 물려주면 다른 파이썬의 site-packages 가
# 먼저 잡혀 lxml 같은 바이너리 패키지가 'No module named lxml.etree' 로 깨진다.
# 이 스크립트는 자기 venv 만 신뢰한다. (다른 import 보다 먼저 실행돼야 한다)
for _p in filter(None, os.environ.get("PYTHONPATH", "").split(os.pathsep)):
    while _p in sys.path:
        sys.path.remove(_p)

import asyncio
import httpx
import json
from bs4 import BeautifulSoup
import urllib.parse
import argparse
import sqlite3
import time
import hashlib
import shutil
import subprocess
from pathlib import Path

# Import local extractor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from local_extract import extract_url

# ──────────────────────────────────────────────
# 로컬 캐시 (SQLite) - DDG 검색 결과 1시간 보관
# ──────────────────────────────────────────────
CACHE_DB = Path(os.path.dirname(os.path.abspath(__file__))) / "search_cache.db"

# 루나 패치 2026-10-28: 캐시 TTL·본문 길이를 환경변수로 조정 가능하게
CACHE_TTL_HOURS = float(os.environ.get("FREE_SEARCH_CACHE_TTL_HOURS", "1"))
DEFAULT_MAX_CHARS = int(os.environ.get("FREE_SEARCH_MAX_CHARS", "1500"))

def init_cache():
    """캐시 DB 초기화"""
    with sqlite3.connect(CACHE_DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS search_cache (
                query_hash TEXT PRIMARY KEY,
                query TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at ON search_cache(created_at)
        """)

def get_cached_search(query: str, max_age_hours: float | None = None) -> list | None:
    """캐시에서 검색 결과 조회 (기본 CACHE_TTL_HOURS, 환경변수로 조정 가능)"""
    if max_age_hours is None:
        max_age_hours = CACHE_TTL_HOURS
    init_cache()
    query_hash = hashlib.sha256(query.encode()).hexdigest()
    cutoff = time.time() - (max_age_hours * 3600)
    
    with sqlite3.connect(CACHE_DB) as conn:
        row = conn.execute(
            "SELECT results FROM search_cache WHERE query_hash = ? AND created_at > ?",
            (query_hash, cutoff)
        ).fetchone()
        if row:
            return json.loads(row[0])
    return None

def save_search_cache(query: str, results: list):
    """검색 결과를 캐시에 저장"""
    init_cache()
    query_hash = hashlib.sha256(query.encode()).hexdigest()
    with sqlite3.connect(CACHE_DB) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO search_cache (query_hash, query, results, created_at) VALUES (?, ?, ?, ?)",
            (query_hash, query, json.dumps(results, ensure_ascii=False), time.time())
        )

async def duckduckgo_search(query: str, max_results: int = 5, use_cache: bool = True) -> list:
    """Perform zero-cost DuckDuckGo search without API keys."""
    # 1. 캐시 확인 (use_cache=True일 때만)
    if use_cache:
        cached = get_cached_search(query)
        if cached:
            print(f"[*] 캐시 히트: \"{query}\"", file=sys.stderr)
            return cached[:max_results]
    
    encoded_query = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }
    
    results = []
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, headers=headers) as client:
            resp = await client.post("https://html.duckduckgo.com/html/", data={"q": query})
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                
                for r in soup.find_all("div", class_="result__body"):
                    title_elem = r.find("a", class_="result__a")
                    snippet_elem = r.find("a", class_="result__snippet")
                    if title_elem and title_elem.get("href"):
                        href = title_elem["href"]
                        # DDG redirect clean
                        if "uddg=" in href:
                            actual_url = urllib.parse.unquote(href.split("uddg=")[1].split("&")[0])
                        else:
                            actual_url = href
                            
                        title = title_elem.get_text(strip=True)
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                        
                        results.append({
                            "title": title,
                            "url": actual_url,
                            "snippet": snippet
                        })
                        if len(results) >= max_results:
                            break
    except Exception as e:
        print(f"[-] Search error: {e}", file=sys.stderr)
       
    # 2. 결과 캐시 저장
    if use_cache and results:
        save_search_cache(query, results)
    
    return results


# ──────────────────────────────────────────────
# 루나 패치 2026-10-28: SearXNG 백엔드 추가
#   목적 = DDG 단일 의존 해소. DDG가 CAPTCHA를 띄울 때 Bing으로 받친다.
#   실측: 2026-10-28 기준 SearXNG 엔진 중 bing만 정상(brave/duckduckgo/startpage는 CAPTCHA/쿼터)
# ──────────────────────────────────────────────
SEARXNG_BASE_URL = os.environ.get("SEARXNG_BASE_URL", "http://localhost:8080")
SEARXNG_ENGINES = os.environ.get("SEARXNG_ENGINES", "bing")


async def searxng_search(query: str, max_results: int = 5,
                         engines: str | None = None, language: str = "ko") -> list:
    """SearXNG 메타검색 (자체 호스팅 · 키 불필요 · JSON API)."""
    params = {
        "q": query,
        "format": "json",
        "language": language,
        "engines": engines or SEARXNG_ENGINES,
    }
    results = []
    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            resp = await client.get(f"{SEARXNG_BASE_URL}/search", params=params)
            if resp.status_code != 200:
                print(f"[-] SearXNG HTTP {resp.status_code}", file=sys.stderr)
                return []
            data = resp.json()
            for r in data.get("results", []):
                url = r.get("url")
                if not url:
                    continue
                results.append({
                    "title": r.get("title", ""),
                    "url": url,
                    "snippet": r.get("content", ""),
                    "engine": f"searxng:{r.get('engine', '?')}",
                })
                if len(results) >= max_results:
                    break
    except Exception as e:
        print(f"[-] SearXNG error: {e}", file=sys.stderr)
    return results


async def hound_search(query: str, max_results: int = 5, region: str | None = None) -> list:
    """hound(master-fetch) keyless 멀티메타서치를 subprocess로 호출.

    루나 패치 2026-10-28: hound는 별도 venv(Python 3.12)라 직접 import 불가 → CLI 래퍼 경유.
    실측: 한국어 27건 / 영어 정확 / 1.4~2.0초 (DDG 단일보다 엔진 풀이 넓고 빠름).
    """
    import subprocess, shutil

    hound_bin = os.environ.get("HOUND_SEARCH_BIN") or os.path.join(
        os.path.expanduser("~"), ".local/bin/hound-search"
    )
    if not os.path.exists(hound_bin):
        return []

    if region is None:
        # 한국어 포함 여부로 리전 자동 선택
        region = "kr-ko" if any("\uac00" <= ch <= "\ud7a3" for ch in query) else "us-en"

    cmd = [hound_bin, query, "-n", str(max_results), "--region", region]
    try:
        proc = await asyncio.to_thread(
            subprocess.run, cmd, capture_output=True, text=True, timeout=45
        )
    except Exception as e:
        print(f"[-] hound 실행 실패: {e}", file=sys.stderr)
        return []

    if proc.returncode != 0 and not proc.stdout.strip():
        print(f"[-] hound 실패(rc={proc.returncode}): {proc.stderr[:200]}", file=sys.stderr)
        return []

    try:
        data = json.loads(proc.stdout)
    except Exception:
        print(f"[-] hound JSON 파싱 실패: {proc.stdout[:200]}", file=sys.stderr)
        return []

    if data.get("error"):
        print(f"[-] hound 오류: {data['error']}", file=sys.stderr)
        return []

    out = []
    for r in data.get("results", []):
        if not r.get("url"):
            continue
        out.append({
            "title": r.get("title", ""),
            "url": r["url"],
            "snippet": r.get("snippet", ""),
            "engine": r.get("engine", "hound"),
        })
        if len(out) >= max_results:
            break
    return out


# ──────────────────────────────────────────────
# Agent Reach 백엔드 (2026-10-28 추가)
#   agent-reach CLI 를 subprocess 로 불러 웹·유튜브·GitHub 을 읽는다.
#   느리므로 auto 체인에서는 맨 마지막에만 쓴다.
# ──────────────────────────────────────────────
def _agent_reach_bin() -> str:
    """agent-reach 실행 경로. 환경변수 우선, 없으면 PATH, 마지막으로 ~/.local/bin."""
    env = os.environ.get("AGENT_REACH_BIN")
    if env and os.path.exists(env):
        return env
    found = shutil.which("agent-reach")
    if found:
        return found
    return os.path.join(os.path.expanduser("~"), ".local", "bin", "agent-reach")


async def reach_search(query: str, max_results: int = 5, channel: str = "web") -> list:
    """Agent Reach 로 검색. 실패하면 조용히 빈 목록.

    channel: web | youtube | github | bilibili | v2ex | reddit ...
    반환 항목은 다른 백엔드와 같은 모양(title/url/snippet/engine)으로 맞춘다.
    """
    binary = _agent_reach_bin()
    if not os.path.exists(binary):
        print(f"[!] agent-reach 없음({binary}) → reach 건너뜀", file=sys.stderr)
        return []

    cmd = [binary, channel, "search", query]
    try:
        # agent-reach 는 블로킹 CLI 라 별도 스레드에서 돌린다 (이벤트 루프 보호)
        proc = await asyncio.to_thread(
            subprocess.run, cmd, capture_output=True, text=True, timeout=120
        )
    except Exception as e:
        print(f"[!] reach 실행 실패({channel}): {e}", file=sys.stderr)
        return []

    if proc.returncode != 0:
        print(f"[!] reach rc={proc.returncode}: {(proc.stderr or '')[:150]}", file=sys.stderr)
        return []

    try:
        data = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception:
        print(f"[!] reach JSON 파싱 실패: {proc.stdout[:150]}", file=sys.stderr)
        return []

    if not data.get("ok"):
        print(f"[!] reach 오류: {str(data.get('error'))[:150]}", file=sys.stderr)
        return []

    out = []
    for r in data.get("items") or []:
        url = r.get("url")
        if not url:
            continue
        out.append({
            "title": r.get("title", ""),
            "url": url,
            "snippet": (r.get("text") or r.get("snippet") or "")[:400],
            "engine": f"reach:{channel}:{data.get('backend', '?')}",
        })
        if len(out) >= max_results:
            break
    return out


async def web_search_multi(query: str, max_results: int = 5, use_cache: bool = True,
                           backend: str = "auto") -> tuple[list, list]:
    """hound → DDG → SearXNG → Agent Reach 순서로 폴백. (results, tried_backends) 반환.

    backend: auto | hound | ddg | searxng | reach | reach:<채널>
      auto   = hound → ddg → searxng → reach (넓게 긁고, 안 되면 정밀·플랫폼 백엔드로)
      reach  = Agent Reach 웹 검색
      reach:youtube / reach:github / reach:reddit = 그 플랫폼만 검색
      ddg    = 한국어 정밀도 우선 (공공기관·뉴스 쿼리에 유리)
      hound  = 영어·기술문서·대량 결과 우선
    """
    tried: list[str] = []

    if backend in ("auto", "hound"):
        tried.append("hound")
        r = await hound_search(query, max_results=max_results)
        if r:
            print(f"[+] hound에서 {len(r)}건 확보", file=sys.stderr)
            return r, tried
        print("[!] hound 0건 → 다음 백엔드", file=sys.stderr)

    if backend in ("auto", "ddg", "duckduckgo"):
        tried.append("ddg")
        r = await duckduckgo_search(query, max_results=max_results, use_cache=use_cache)
        if r:
            return r, tried
        print("[!] DDG 0건 → SearXNG 폴백 시도", file=sys.stderr)

    if backend in ("auto", "searxng"):
        tried.append("searxng:" + SEARXNG_ENGINES)
        r = await searxng_search(query, max_results=max_results)
        if r:
            print(f"[+] SearXNG({SEARXNG_ENGINES})에서 {len(r)}건 확보", file=sys.stderr)
            return r, tried

    # Agent Reach — auto 체인의 마지막. 느리므로 앞 백엔드가 모두 0건일 때만.
    if backend == "auto" or backend == "reach" or backend.startswith("reach:"):
        channel = "web" if backend in ("auto", "reach") else backend.split(":", 1)[1]
        tried.append(f"reach:{channel}")
        r = await reach_search(query, max_results=max_results, channel=channel)
        if r:
            print(f"[+] Agent Reach({channel})에서 {len(r)}건 확보", file=sys.stderr)
            return r, tried
        print(f"[!] reach:{channel} 0건", file=sys.stderr)

    return [], tried

async def search_and_extract(query: str, max_results: int = 5, extract_body: bool = True, use_cache: bool = True, backend: str = "auto", max_chars: int | None = None) -> dict:
    """Main zero-cost search and live extraction pipeline."""
    if max_chars is None:
        max_chars = DEFAULT_MAX_CHARS
    print(f"[*] 0원 검색 시작: \"{query}\" (최대 {max_results}개, 백엔드={backend})", file=sys.stderr)
    search_results, backends_tried = await web_search_multi(
        query, max_results=max_results, use_cache=use_cache, backend=backend
    )
    
    if not search_results:
        # 루나 패치 2026-10-28: 조용한 실패 제거 — 0건이면 반드시 경고
        print(f"[!!] 경고: 검색 결과 0건 (시도 백엔드: {', '.join(backends_tried) or '없음'})", file=sys.stderr)
        print("[!!] 원인 후보: 네트워크 차단 / CAPTCHA / DDG HTML 구조 변경 / 잘못된 쿼리", file=sys.stderr)
        print("[!!] 대응: 쿼리를 바꾸거나 어절 단위로 쪼개 재시도하세요.", file=sys.stderr)
        return {
            "success": False,
            "query": query,
            "error": f"\"{query}\"에 대한 검색 결과를 찾을 수 없습니다.",
            "backends_tried": backends_tried,
            "results": []
        }
       
    # 루나 패치 2026-10-28: 본문 추출을 순차 → 병렬(asyncio.gather)로
    async def _extract_one(idx: int, res: dict) -> dict:
        item = {
            "index": idx,
            "title": res['title'],
            "url": res['url'],
            "snippet": res['snippet'],
            "engine": res.get('engine', ''),
        }
        if extract_body:
            extracted = await extract_url(res['url'], max_chars=max_chars)
            if extracted["status"] == "success" and len(extracted["content"]) > 100:
                item["extracted"] = {
                    "content": extracted["content"],
                    "method": extracted["method"]
                }
        return item

    if extract_body:
        print(f"[*] 본문 추출 중 (병렬 {len(search_results)}건)...", file=sys.stderr)
        output_results = list(await asyncio.gather(
            *[_extract_one(i, res) for i, res in enumerate(search_results, 1)]
        ))
    else:
        output_results = [
            {"index": i, "title": r['title'], "url": r['url'], "snippet": r['snippet']}
            for i, r in enumerate(search_results, 1)
        ]
    
    return {
        "success": True,
        "query": query,
        "results": output_results,
        "count": len(output_results)
    }

def format_markdown_output(data: dict) -> str:
    """Format results as markdown for human-readable output."""
    if not data.get("success"):
        return f"❌ {data.get('error', '알 수 없는 오류')}"

    # URL 단일 추출 모드 — query/results 가 없고 url/content/method 만 온다
    if "results" not in data and "url" in data:
        head = data.get("title") or data.get("url", "")
        out = [f"# 🔍 본문 추출: {head}\n",
               f"- **URL**: {data.get('url')}",
               f"- **방식**: {data.get('method', '?')}\n",
               "**본문**:",
               "> " + (data.get("content") or "").replace(chr(10), chr(10) + "> ")]
        return "\n".join(out)

    output = [f"# 🔍 0원 웹 검색 결과: \"{data.get('query', '')}\"\n"]
    
    for res in data["results"]:
        output.append(f"## {res['index']}. {res['title']}")
        output.append(f"- **URL**: {res['url']}")
        output.append(f"- **요약**: {res['snippet']}\n")
        
        if "extracted" in res:
            ext = res["extracted"]
            output.append(f"**[본문 발췌 ({ext['method']})]**:")
            output.append(f"> {ext['content'].replace(chr(10), chr(10)+'> ')}\n")
        
        output.append("---\n")
    
    return "\n".join(output)

async def extract_single_url(url: str, max_chars: int = 50000) -> dict:
    """Extract content from a single URL."""
    print(f"[*] 본문 추출 중: {url[:60]}...", file=sys.stderr)
    extracted = await extract_url(url, max_chars=max_chars)
    return {
        "success": extracted["status"] == "success",
        "url": url,
        "title": extracted.get("title", ""),
        "content": extracted.get("content", ""),
        "method": extracted.get("method", ""),
        "error": extracted.get("error") if extracted["status"] != "success" else None
    }

def main():
    parser = argparse.ArgumentParser(description="Free Search Pipeline - 0원 검색/추출")
    parser.add_argument("query", help="검색 쿼리 또는 URL")
    parser.add_argument("-n", "--max-results", type=int, default=5, help="최대 결과 수 (기본 5)")
    parser.add_argument("--backend", default="auto",
                        help="검색 백엔드: auto | hound | ddg | searxng | reach | reach:youtube | reach:github | reach:reddit")
    parser.add_argument("--max-chars", type=int, default=None,
                        help=f"본문 추출 최대 글자수 (기본 {DEFAULT_MAX_CHARS}, 환경변수 FREE_SEARCH_MAX_CHARS)")
    parser.add_argument("--json", action="store_true", help="JSON 출력")
    parser.add_argument("--no-extract", action="store_true", help="본문 추출 건너뛰기 (검색만)")
    parser.add_argument("--no-cache", action="store_true", help="캐시 사용 안 함 (강제 재검색)")
    parser.add_argument("--no-reach", dest="no_reach", action="store_true",
                        help="URL 읽기에서 Agent Reach(Jina) 폴백을 끈다 (사내문서·개인정보 보호용)")
    args = parser.parse_args()

    # Agent Reach(Jina) 는 URL 을 외부 서버로 넘긴다. 필요 없으면 끈다.
    if args.no_reach:
        os.environ["FREE_SEARCH_NO_REACH"] = "1"

    target = args.query
    
    if target.startswith("http://") or target.startswith("https://"):
        # URL direct extract mode
        result = asyncio.run(extract_single_url(target))
    else:
        # Search and extract mode
        result = asyncio.run(search_and_extract(target, max_results=args.max_results, extract_body=not args.no_extract, use_cache=not args.no_cache, backend=args.backend, max_chars=args.max_chars))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_markdown_output(result))

if __name__ == "__main__":
    main()