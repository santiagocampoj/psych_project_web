import numpy as np
import soundfile as sf
from mosqito.sq_metrics import (
    loudness_zwst, sharpness_din_st, roughness_dw, sii_ansi,
)



# --- Constantes de calibración ---
P_REF = 2e-5 # 20 µPa, presión de referencia en aire
REFERENCE_FILE_RMS = 0.05 # RMS al que preprocessing.py deja las referencias
BASELINE_SPL_DB = 70 # SPL que representa ese RMS

SCALING_TO_PA = P_REF * 10**(BASELINE_SPL_DB / 20) / REFERENCE_FILE_RMS
# ≈ 0.0632 / 0.1 = 0.632



def compute_all(wav_path):
    """
    Carga un WAV, lo escala a Pascales con el factor fijo y devuelve
    las cuatro métricas + el SPL real (para verificación).
    """
    x, fs = sf.read(str(wav_path))
    if x.ndim > 1:
        x = x.mean(axis=1)
    x = x.astype(np.float64) * SCALING_TO_PA

    rms_pa = np.sqrt(np.mean(x**2))
    spl_db = 20 * np.log10(rms_pa / P_REF)

    N, _, _    = loudness_zwst(x, fs)
    S          = sharpness_din_st(x, fs)
    R, _, _, _ = roughness_dw(x, fs)
    # SII, _, _  = sii_ansi(x, fs, method='critical', speech_level='normal')
    SII, _, _  = sii_ansi(x, fs, method='critical', speech_level='loud')


    return {
        "spl_db":          float(spl_db),
        "loudness_sone":   float(N),
        "sharpness_acum":  float(S),
        "roughness_asper": float(np.mean(R)),
        "sii":             float(SII),
    }


if __name__ == "__main__":
    import sys
    from pprint import pprint
    pprint(compute_all(sys.argv[1]))