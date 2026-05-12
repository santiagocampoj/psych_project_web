"""
Normalize the refe audio files
"""
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from math import gcd
from pathlib import Path



TARGET_FS = 48000
TARGET_DURATION = 5.0
FADE_DURATION = 0.05
RMS_TARGET = 0.05



def preprocess_file(in_path, out_path):
    x, fs = sf.read(str(in_path))

    # mono
    if x.ndim > 1:
        x = x.mean(axis=1)
    x = x.astype(np.float64)

    # resample
    if fs != TARGET_FS:
        g = gcd(int(fs), TARGET_FS)
        x = resample_poly(x, TARGET_FS // g, fs // g)

    # trim al centro (evita silencios al inicio/fin)
    n = int(TARGET_DURATION * TARGET_FS)
    if len(x) >= n:
        start = (len(x) - n) // 2
        x = x[start:start + n]
    else:
        x = np.pad(x, (0, n - len(x)))

    # fades
    n_fade = int(FADE_DURATION * TARGET_FS)
    x[:n_fade] *= np.linspace(0, 1, n_fade)
    x[-n_fade:] *= np.linspace(1, 0, n_fade)

    # RMS común
    rms = np.sqrt(np.mean(x**2))
    if rms > 0:
        x *= RMS_TARGET / rms

    # safety contra clipping
    peak = np.max(np.abs(x))
    clipped = False
    if peak > 0.99:
        x *= 0.99 / peak
        clipped = True

    sf.write(str(out_path), x, TARGET_FS)
    return np.sqrt(np.mean(x**2)), np.max(np.abs(x)), clipped




def preprocess_directory(in_dir, out_dir):
    in_dir, out_dir = Path(in_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Preprocessing {in_dir} → {out_dir}")
    # .wav and .mp3
    for p in sorted(in_dir.glob("*.wav")) + sorted(in_dir.glob("*.mp3")):
        # rms, peak, clipped = preprocess_file(p, out_dir / p.name)
        rms, peak, clipped = preprocess_file(p, out_dir / (p.stem + ".wav"))
        flag = "  ⚠️ clipped" if clipped else ""
        print(f"  {p.name:30s}  RMS={rms:.4f}  peak={peak:.3f}{flag}")


if __name__ == "__main__":
    preprocess_directory("data/reference_raw", "data/reference")