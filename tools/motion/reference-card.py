#!/usr/bin/env python3
"""
reference-card.py — 레퍼런스 영상 → 렌더 파라미터 카드(JSON + MD)

추출 항목
  1) 리듬   : 컷 타임, 샷 길이 분포(평균/중앙/표준편차), 균등도, 3초 초과 비율
  2) 색     : k-means 팔레트(6색) + 점유율, 밝기 곡선
  3) 모션   : 초당 프레임 차분 에너지(모션 강도), 피크 구간
  4) 소리   : BPM(자기상관), 온셋 밀도, 비트 격자 대비 컷 정렬도
  5) 요약   : 우리 렌더 파라미터로의 변환 제안

사용: python3 reference-card.py ref.mp4 out_dir [label]
"""
import sys, os, json, subprocess, math
import numpy as np

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, **kw)


def probe(path):
    r = run([FFPROBE, "-v", "error", "-show_entries",
             "format=duration:stream=codec_type,width,height,r_frame_rate",
             "-of", "json", path])
    j = json.loads(r.stdout.decode())
    d = float(j["format"]["duration"])
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), {})
    num, den = (v.get("r_frame_rate", "30/1").split("/") + ["1"])[:2]
    fps = float(num) / float(den or 1)
    return d, fps, int(v.get("width", 0)), int(v.get("height", 0))


def cuts(path, thr=0.32):
    r = run([FFMPEG, "-hide_banner", "-i", path, "-filter:v",
             f"select='gt(scene,{thr})',showinfo", "-f", "null", "-"])
    out = []
    for line in r.stderr.decode(errors="ignore").split("\n"):
        if "pts_time:" in line:
            try:
                out.append(float(line.split("pts_time:")[1].split()[0]))
            except Exception:
                pass
    return sorted(set(round(x, 3) for x in out))


def frames_rgb(path, fps=0.5, w=96, h=54, limit=None):
    cmd = [FFMPEG, "-v", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    r = run(cmd)
    buf = np.frombuffer(r.stdout, dtype=np.uint8)
    n = len(buf) // (w * h * 3)
    return buf[: n * w * h * 3].reshape(n, h, w, 3).astype(np.float32)


def kmeans_palette(imgs, k=6, iters=12):
    px = imgs.reshape(-1, 3)
    if len(px) > 60000:
        idx = np.linspace(0, len(px) - 1, 60000).astype(int)
        px = px[idx]
    rng = np.random.default_rng(7)
    cent = px[rng.choice(len(px), k, replace=False)]
    for _ in range(iters):
        d = ((px[:, None, :] - cent[None, :, :]) ** 2).sum(-1)
        lab = d.argmin(1)
        for j in range(k):
            m = lab == j
            if m.any():
                cent[j] = px[m].mean(0)
    lab = ((px[:, None, :] - cent[None, :, :]) ** 2).sum(-1).argmin(1)
    share = np.bincount(lab, minlength=k) / len(px)
    order = np.argsort(-share)
    return [{"hex": "#%02x%02x%02x" % tuple(int(c) for c in cent[j]),
             "share": round(float(share[j]), 3)} for j in order]


def audio_mono(path, sr=8000):
    r = run([FFMPEG, "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr),
             "-f", "s16le", "-"])
    return np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32) / 32768.0, sr


def onset_env(x, sr, hop=256, win=1024):
    if len(x) < win * 2:
        return np.zeros(1), hop
    n = 1 + (len(x) - win) // hop
    w = np.hanning(win).astype(np.float32)
    prev = None
    env = np.zeros(n, dtype=np.float32)
    for i in range(n):
        seg = x[i * hop: i * hop + win] * w
        mag = np.abs(np.fft.rfft(seg))
        if prev is not None:
            diff = mag - prev
            env[i] = float(np.maximum(diff, 0).sum())
        prev = mag
    if env.max() > 0:
        env /= env.max()
    return env, hop


def estimate_bpm(env, hop, sr):
    fps_env = sr / hop
    e = env - env.mean()
    ac = np.correlate(e, e, mode="full")[len(e) - 1:]
    if len(ac) < 10 or ac[0] <= 0:
        return 0, []
    lo = int(fps_env * 60 / 190)
    hi = int(fps_env * 60 / 60)
    hi = min(hi, len(ac) - 2)
    if hi <= lo:
        return 0, ac
    seg = ac[lo:hi]
    lag = lo + int(seg.argmax())
    bpm = 60.0 * fps_env / lag
    return round(float(bpm), 1), ac


def peaks(env, hop, sr, thr=0.35, min_gap=0.10):
    fps_env = sr / hop
    out = []
    last = -9
    for i in range(1, len(env) - 1):
        if env[i] > thr and env[i] >= env[i - 1] and env[i] > env[i + 1]:
            t = i / fps_env
            if t - last >= min_gap:
                out.append(round(t, 3))
                last = t
    return out


def align_score(cut_times, onsets, tol=0.12):
    if not onsets or not cut_times:
        return 0.0
    o = np.array(onsets)
    hit = 0
    for c in cut_times:
        if np.min(np.abs(o - c)) <= tol:
            hit += 1
    return round(100.0 * hit / len(cut_times), 1)


def analyze(path, label, mode="footage"):
    thr = 0.10 if mode == "motion" else 0.32
    dur, fps, w, h = probe(path)
    ct = cuts(path, thr)
    d = np.diff(ct).tolist() if len(ct) > 1 else []
    d = [x for x in d if x > 0.02]
    st = {
        "cuts": len(ct),
        "mean": round(float(np.mean(d)), 3) if d else 0,
        "median": round(float(np.median(d)), 3) if d else 0,
        "stdev": round(float(np.std(d)), 3) if d else 0,
        "min": round(min(d), 3) if d else 0,
        "max": round(max(d), 3) if d else 0,
        "over3s": round(100 * sum(1 for x in d if x > 3) / len(d), 1) if d else 0,
    }
    # 균등도: 표준편차/평균 (0에 가까울수록 메트로놈)
    st["cv"] = round(st["stdev"] / st["mean"], 3) if st["mean"] else 0

    imgs = frames_rgb(path, fps=0.5)
    pal = kmeans_palette(imgs) if len(imgs) else []
    lum = imgs.mean(axis=(1, 2, 3)) / 255.0 if len(imgs) else np.array([0])
    motion = np.abs(np.diff(imgs, axis=0)).mean(axis=(1, 2, 3)) / 255.0 if len(imgs) > 1 else np.array([0])

    x, sr = audio_mono(path)
    env, hop = onset_env(x, sr)
    bpm, _ = estimate_bpm(env, hop, sr)
    on = peaks(env, hop, sr)
    density = round(len(on) / (dur / 60.0), 1) if dur else 0
    align = align_score(ct, on)

    card = {
        "label": label,
        "mode": mode,
        "source": os.path.abspath(path),
        "duration": round(dur, 2),
        "fps": round(fps, 2),
        "size": f"{w}x{h}",
        "rhythm": st,
        "palette": pal,
        "luminance": {"mean": round(float(lum.mean()), 3),
                      "stdev": round(float(lum.std()), 3)},
        "motion": {"mean": round(float(motion.mean()), 4),
                   "p90": round(float(np.percentile(motion, 90)), 4)},
        "audio": {"bpm": bpm, "onsets": len(on), "density_per_min": density,
                  "cut_on_beat_pct": align},
        "suggest": {
            "shot_length_palette": [round(x, 2) for x in
                                    np.percentile(d, [10, 30, 50, 70, 90]).tolist()] if d else [],
            "cut_to_beat": "컷을 온셋에 스냅" if align >= 55 else "컷은 프레이즈 단위, 온셋은 강조에만",
            "hold_ratio": st["over3s"],
        },
    }
    return card


def to_md(card):
    r, p, a = card["rhythm"], card["palette"], card["audio"]
    L = []
    L.append(f"# 레퍼런스 카드 — {card['label']}\n")
    L.append(f"- 길이 **{card['duration']}s** / {card['fps']}fps / {card['size']}")
    L.append(f"- 컷 **{r['cuts']}회** · 평균 **{r['mean']}s** · 중앙 **{r['median']}s** · 표준편차 {r['stdev']}s")
    L.append(f"- 최단 {r['min']}s / 최장 {r['max']}s / **3초 초과 {r['over3s']}%**")
    L.append(f"- 변동계수(CV) **{r['cv']}**  → {'호흡형(긴+짧은 혼합)' if r['cv'] > 0.6 else '균등형'}")
    L.append(f"\n## 팔레트")
    for c in p:
        L.append(f"- `{c['hex']}` {int(c['share']*100)}%")
    L.append(f"\n## 소리")
    L.append(f"- BPM **{a['bpm']}** · 온셋 {a['onsets']}개({a['density_per_min']}/분)")
    L.append(f"- 컷-온셋 정렬 **{a['cut_on_beat_pct']}%** → {card['suggest']['cut_to_beat']}")
    L.append(f"\n## 우리 렌더 파라미터로")
    sp = card["suggest"]["shot_length_palette"]
    if sp:
        L.append(f"- 샷 길이 5단 분위: {sp} 초 → **{sp[0]}~{sp[-1]}초 범위에서 뽑아 쓴다**")
    L.append(f"- 3초 이상 홀드 **{r['over3s']}%** 확보 (여운)")
    return "\n".join(L)


if __name__ == "__main__":
    path, outdir = sys.argv[1], sys.argv[2]
    label = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(path)
    mode = sys.argv[4] if len(sys.argv) > 4 else "footage"
    os.makedirs(outdir, exist_ok=True)
    card = analyze(path, label, mode)
    base = os.path.join(outdir, label.replace(" ", "_"))
    json.dump(card, open(base + ".json", "w"), ensure_ascii=False, indent=1)
    open(base + ".md", "w").write(to_md(card))
    print(json.dumps(card, ensure_ascii=False, indent=1))
