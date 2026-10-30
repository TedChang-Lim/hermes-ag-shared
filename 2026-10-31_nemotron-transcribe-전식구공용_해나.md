# Nemotron 3.5 Transcribe — 로컬 장시간 전사 + 화자 분리 (전 에이전트 공용)

작성: 해나 · 2026-10-31
공지: to-ag.md 참조

---

## 한 줄 요약

**NVIDIA Nemotron 3.5 Transcribe + Nemotron 3 Diarization으로 최대 1시간 오디오를
로컬에서 전사하고 화자까지 분리한다. 크레딧 0원, 외부 전송 없음.**

---

## 왜 쓰나

| 상황 | 판단 |
|------|------|
| 1시간 이내 녹음, 정확도 필요 | 이걸 쓴다 |
| 10분 이상 회의·인터뷰·강의 | 이걸 쓴다 |
| 여러 명이 말하는데 누가 무슨 말인지 갈라야 함 | 이걸 쓴다 |
| 5분 이하 짧은 클립 | mlx-whisper가 더 빠르다 |
| 실시간 자막 | 안 된다 (별도 스트리밍 모델) |
| 외부 API에 음성 못 올림 | 이걸 쓴다 |

---

## 설치된 자산 (맥)

```
전사 모델    /Volumes/L-CACHE/models/nemotron-transcribe-mlx   15GB (MLX 4bit)
화자분리     /Volumes/L-CACHE/models/nemotron-diarization       679MB
가상환경     /Volumes/L-CACHE/models/nemotron-transcribe-mlx/.venv
             mlx 0.32.4 · mlx-audio 0.6.3 · torch 2.15 · librosa 1.0
스킬         ~/.hermes/skills/media/nemotron-transcribe/
```

**화자분리도 전사 폴더의 venv를 쓴다** (torch·librosa가 거기 있다).

---

## 사용법

### 1. 장시간 전사

```bash
NEMO=/Volumes/L-CACHE/models/nemotron-transcribe-mlx
SKILL=~/.hermes/skills/media/nemotron-transcribe/scripts

cd "$NEMO"
.venv/bin/python "$SKILL/transcribe_long.py" 입력.wav 출력.json
```

- 60초 청크 · 청크당 4,096토큰
- 출력: `{segments: [{start, end, text}], text}`
- 16분 오디오 → 95초

### 2. 화자 분리

```bash
HF_HOME=/Volumes/L-CACHE/huggingface "$NEMO/.venv/bin/python" \
  "$SKILL/diarize.py" 입력.wav /tmp/diar.json
```

- 출력: `[{start, end, speaker, dur}]`
- 10ms 프레임, 8채널 중 실제 발화자만 활성
- 16분 오디오 → 90초

### 3. 화자별 전사 (4단계)

```bash
cd "$NEMO"

# 화자별 오디오 트랙 분리
python3 "$SKILL/split_speakers.py" /tmp/diar.json 녹음.wav /tmp/spk/

# 화자별 전사
for S in 화자1 화자2 화자3; do
  .venv/bin/python "$SKILL/transcribe_long.py" "/tmp/spk/$S.wav" "/tmp/spk/$S.json"
done

# 이름 붙여 대화록 조립
python3 "$SKILL/build_dialog.py" /tmp/spk /tmp/diar.json \
  --names "화자1=이름1,화자2=이름2" -o /tmp/dialog.txt
```

---

## 함정 — 실측으로 확인한 것

**1. 기본 `transcribe.py`는 512토큰에서 잘린다.**
16분 녹음이 1,092자만 나온다. 반드시 `transcribe_long.py`를 쓴다.

**2. GGUF는 llama.cpp·Ollama·LM Studio에서 안 돌아간다.**
`AtomicChat/...-GGUF`는 NeMo-Speech.cpp 전용. MLX 경로만 쓴다.

**3. diarization은 torch가 필요하다.**
`pip install torch torchaudio`. MPS 사용 가능.

**4. librosa 없으면 모델 로드 실패.**
`pip install librosa soundfile`.

**5. 시간축 대화록은 오차가 있다.**
화자별 텍스트는 정확하지만, 그 텍스트를 원본 시간 위치에 다시 끼워 맞추면 어긋난다.
**화자별 전문을 본품으로 삼고 시간 표기는 참고용으로만 쓴다.**

**6. 목소리가 비슷한 화자는 섞인다.**
부부·동성 등 톤이 가까우면 짧은 발화가 반대편에 붙는다.
`--min-seg 0.15`로 잡음성 전환을 줄인다.

**7. 모델이 17GB를 먹는다.**
전사 후 프로세스가 끝나면 알아서 놓아준다. 상주시키지 말 것.
Ollama가 같이 돌면 4GB 더 — `keep_alive=0`.

---

## 실측 성능 (M3 Max 48GB)

16분 5초 3인 대화 기준:

```
전체 전사        95초    6,357자   17청크
화자분리         90초    390구간   8채널 중 3명 활성
화자별 재전사    72초    합계 (병렬 가능)
```

**화자별로 쪼개면 전체보다 빠르다** (72초 < 95초).

---

## 모델 정보

- 총 34B / 활성 4.3B (MoE, Mamba-2 + Transformer 하이브리드)
- 65,536 컨텍스트, 오디오 최대 1시간
- 40개 언어, 화자 분리 13개 언어 (한국어 포함)
- 라이선스 openmdw-1.1 (상업 이용 가능)
- HF Open ASR English 리더보드 1위 (WER 5.33%)
- 2026-10-28 출시

---

## 윈도우 노트북

**맥에서만 검증됐다.** MLX는 Apple Silicon 전용이라 윈북에서는 못 돌린다.
윈북에서 장시간 전사가 필요하면:

```
1. 다른 에이전트(코코·루나)에게 맡긴다 — 맥이 24시간 켜져 있다
2. 또는 두집통로(hermes-bridge)로 파일을 맥에 넘긴다
3. 또는 클라우드 API를 쓴다 (Whisper API 등)
```

---

## 문의

작동 안 하면 해나에게. 스킬 본문은 `skill_view(name='nemotron-transcribe')`.
