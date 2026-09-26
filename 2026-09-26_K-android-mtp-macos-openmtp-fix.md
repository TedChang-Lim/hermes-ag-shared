# 안드로이드↔macOS 파일 전송(MTP) 정비 완료 — K 보고서

- **작성:** K (Cline Desktop, 새미새론AI교육원 정식 상주 8번)
- **일시:** 2026-09-26 (마스터님 승인 하에 실행)
- **수신:** 해나(총괄), AG(기획), 전 에이전트
- **중요도:** 중 — 신규 자산 4종 + K 전역 규칙 신설 (타 에이전트 참고 사항 있음)

---

## 1. 무엇을 했는가
마스터님의 Galaxy S23 Ultra(SM-S918N) → MacBook Pro(M3 Max, macOS 26.6.2 Tahoe) 사진·영상 대량 이동 문제를 **현장 진단 → 해결 → 검증**까지 완료했습니다.

- **성과:** `/Volumes/ARCHIVE` 65Gi → 103Gi = **38GB 전송 성공**, 오류 로그 0건
- **검증:** `MTP_INITIALIZE_SUCCESS` / `MTP_LIST_FILES_SUCCESS` / `Model: SM-S918N` 기록 확인

## 2. 원인 (증거 기반 · 추측 없음)
1. **macOS Finder는 MTP 미지원** — Android 4.0부터 UMS 폐지 → MTP 전환. 애플은 PTP만 지원.
   (Apple USB 스택은 인터페이스를 `MTP@0`으로 인식만 하고 열지 않음)
2. **이미지캡처 스택이 MTP 인터페이스 선점** — `ptpcamerad` / `icdd` / `Photos`
   → libusb 프로브 결과 `iface 0 class=0x06/0x01/0x01`, `claim rc=-3 (LIBUSB_ERROR_ACCESS)`
3. **멈춘 OpenMTP 헬퍼 `mtp-cli storage-list`가 인터페이스 영구 점유** ← 결정적 주범
   → `ioreg`에서 `"IOUserClientCreator" = "pid 13447, mtp-cli"` 로 특정
4. 폰 측 MTP 서버 wedged → 잠금 해제 + USB 모드 재선택으로 초기화 필요

## 3. 해결 (재현 가능)
1. `launchctl disable gui/$(id -u)/com.apple.ptpcamerad` (SIP로 bootout은 불가)
2. `pkill -9 ptpcamerad; pkill -9 icdd; pkill -x Photos; pkill -x mtp-cli`
3. **4~6초 정착 대기** (선점자 종료 시 USB 재열거 발생 → 즉시 실행하면 실패)
4. 폰: 잠금 해제 → 알림창 'USB로 충전 중' → **'파일 전송/Android Auto' 재선택**
5. OpenMTP 실행 → ⌘R → 좌측 패널 `/Volumes/ARCHIVE`에서 ⌘V
6. 다음부터는 **`galaxy-connect`** 한 줄 (전 단계 자동 + 연결 검증)

## 4. 신규 자산 (`~/bin/`)
`galaxy-connect.sh`(별칭 `galaxy-connect`) · `mtpprobe` · `mtpclient` · `usbreset`
+ `~/ARCHIVE`, `~/L-CACHE` 심볼릭 링크(OpenMTP 로컬 패널 접근용)

## 5. 타 에이전트 참고 (중요)
- **K 전역 규칙 신설:** `~/.clinerules` — 세션 시작 시 `agent.md`(SSOT)와 `9_K.md`를 정독하도록 고정했습니다.
  (해나 `~/.hermes/AGENTS.md`, 루나 `~/.openclaw/workspace/AGENTS.md`, AG `~/.gemini/config/AGENTS.md`는 이미 존재했고 **K만 전역 지침이 없던 구조적 공백**이 원인이었습니다)
- **금기:** OpenMTP 사용 중 `kill -9` 금지 / `mtpprobe`를 MTP 세션 중 실행 금지 / 외장 볼륨은 ⌘E 추출
- 위키 정본: `~/wiki/concepts/android-mtp-macos-openmtp.md`
  다모아 사본: `~/초보프로젝트/knot/wiki/android-mtp-macos-openmtp-2026-09-26.md`

## 6. 라이브 사이트 관련
본 작업은 **로컬 파일 전송 인프라** 건으로, `semiseron.kr` / `meta-ai-labs` / `kacec.kr` 라이브 사이트에는 **일절 손대지 않았습니다.**
