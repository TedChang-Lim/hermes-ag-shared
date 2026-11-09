# semiseron.kr 파비콘 추가 (2026-11-09)

마스터님 지적: "탭에 노트북LM·다음·구글 아이콘은 나오는데 우리는 아무것도 안 나온다."
확인해 보니 **파비콘이 아예 없었다.**

## 원인

```
GET /favicon.ico → 404 (9,379B 오류 페이지)
index.html → rel="icon" 링크 0개
```

## 조치

1. `assets/logo/symbol_light.png` 에서 **왼쪽 큰 A만 잘라냄** (x 120~695)
   - 심볼 전체(세로 글자 '새미새론' + 별 3개)를 16px로 줄이면 글자가 뭉개진다
2. 잉크색(#080908) 정사각 타일에 여백 14%로 얹어 아이콘 생성
3. 산출물 7개 + head 링크 6줄 + `site.webmanifest`

| 파일 | 비고 |
|---|---|
| favicon.ico | 16·32·48 포함 |
| favicon-32x32.png / 48 / 192 / 512 | 탭·북마크·PWA |
| apple-touch-icon.png | 180, iOS 홈화면 |
| site.webmanifest | 이름·테마색 |

## 검증 (라이브)

```
/favicon.ico           200  image/vnd.microsoft.icon  450B
/favicon-32x32.png     200  image/png                1,085B
/favicon-192x192.png   200  image/png                7,259B
/apple-touch-icon.png  200  image/png                6,050B
/site.webmanifest      200  application/manifest+json
```

커밋 `1d2f556`. GitHub Pages 반영까지 약 100초 걸렸다(20초 간격 6회 폴링).

## 전 에이전트가 알아야 할 것

1. **파비콘은 사이트 저장소 루트에 두고 `/favicon.ico` 로 접근돼야 한다.** `assets/` 안에만 두면 브라우저는 못 찾는다.
2. **로고를 파비콘으로 그대로 축소하지 마라.** 워드마크·세로 텍스트는 16px에서 사라진다. **심볼의 한 글자만** 남긴다.
3. **브라우저는 파비콘을 오래 캐시한다.** 마스터님께 "안 바뀐 것 같다"는 말을 들으면 새 탭으로 열게 안내한다.
4. 배포 뒤 `curl -o /dev/null -w "%{http_code}"` 로 **ico가 200인지** 반드시 확인한다. index.html만 고치고 끝내면 여전히 404다.

## 기억

- 파비콘 생성 코드는 이 문서에 절차만 남겼다. 다시 만들 때는 `symbol_light.png` 에서 A 영역(x 120~695)만 자르고, 32/48/180/192/512 + ico(16·32·48)를 만들면 된다.
- 다모아 기록: `knot/wiki/semiseron-favicon-2026-11-09.md`
