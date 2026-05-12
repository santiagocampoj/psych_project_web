import numpy as np
from mosqito.sq_metrics import (
    loudness_zwst, sharpness_din_st, roughness_dw, sii_ansi,
)

P_REF = 2e-5  # 20 µPa


def calibrate(x, db_spl):
    """
    Calibrates the input signal x to have the specified sound pressure level (SPL) in decibels (dB SPL).
    """
    rms = np.sqrt(np.mean(x**2))
    return x * (P_REF * 10**(db_spl / 20) / rms)


def tone(f0, duration, fs):
    """
    Generates a pure tone (sine wave) at frequency f0, sampled at fs for the given duration.
    """
    t = np.arange(0, duration, 1/fs)
    return np.sin(2 * np.pi * f0 * t)


def am_tone(fc, fmod, depth, duration, fs):
    """
    AM tone is a carrier (sine wave at frequency fc) whose amplitude is modulated by another sine wave (the envelope) 
    at frequency fmod. The depth parameter controls how much the amplitude varies, with 1.0 being full modulation and 0.0 being no modulation.
    """
    t = np.arange(0, duration, 1/fs)
    carrier = np.sin(2 * np.pi * fc * t)
    envelope = 0.5 * (1 + depth * np.sin(2 * np.pi * fmod * t))
    return carrier * envelope







def main():
    fs = 48000
    duration = 1.0
    print(f"\nMoSQITo sanity check  (fs={fs} Hz, dur={duration}s)\n" + "-"*55)



    # --- 1. Loudness: 1 kHz @ 60 dB SPL → ~4 sone ---
    x = calibrate(tone(1000, duration, fs), db_spl=60)
    N, _, _ = loudness_zwst(x, fs)
    print(f"Loudness   1 kHz @ 60 dB SPL : {N:6.2f} sone    (esperado ≈ 4)")



    # --- 2. Sharpness: 1 kHz @ 60 dB SPL → ~1 acum ---
    S = sharpness_din_st(x, fs)
    print(f"Sharpness  1 kHz @ 60 dB SPL : {S:6.2f} acum    (esperado ≈ 1)")



    # --- 3. Roughness: 1 kHz × AM 70 Hz, 100% @ 60 dB → ~1 asper --- AM stands for Amplitude Modulation 
    x_am = calibrate(am_tone(1000, 70, 1.0, duration, fs), db_spl=60)
    R, _, _, _ = roughness_dw(x_am, fs)
    print(f"Roughness  1 kHz × AM 70 Hz  : {np.mean(R):6.2f} asper   (esperado ≈ 1)")



    # --- 4. SII: ruido bajo → SII cercano a 1 ---
    rng = np.random.default_rng(seed=0)
    noise = calibrate(rng.standard_normal(int(duration * fs)), db_spl=40)
    SII, _, _ = sii_ansi(noise, fs, method='critical', speech_level='normal')
    print(f"SII        ruido @ 40 dB SPL : {SII:6.2f}         (esperado ≈ 1)")



    # --- 5. Bonus: verifica que loudness se dobla cada 10 dB ---
    print("\nVerificación cualitativa (loudness debería doblar cada 10 dB):")
    for db in [40, 50, 60, 70]:
        x = calibrate(tone(1000, duration, fs), db_spl=db)
        N, _, _ = loudness_zwst(x, fs)
        print(f"  1 kHz @ {db} dB SPL : {N:6.2f} sone")

    

    print("\nDiagnóstico SII (mismo ruido, distintos niveles):")
    for db in [20, 30, 40, 50, 60, 70, 80]:
        noise = calibrate(rng.standard_normal(int(duration * fs)), db_spl=db)
        SII, _, _ = sii_ansi(noise, fs, method='critical', speech_level='normal')
        print(f"  ruido @ {db} dB SPL : SII = {SII:.2f}")




if __name__ == "__main__":
    main()