import numpy as np
import soundfile as sf
from pathlib import Path

from src import modifications as mods
from src.stimuli_config import COMMON_MODIFICATIONS, SPECIFIC_MODIFICATIONS

REFERENCE_DIR = Path("data/reference")
STIMULI_DIR   = Path("data/stimuli")

FUNC_MAP = {
    "change_level":       mods.change_level,
    "lowpass_filter":     mods.lowpass_filter,
    "highpass_filter":    mods.highpass_filter,
    "amplitude_modulate": mods.amplitude_modulate,
    "attenuate_tone":     mods.attenuate_tone,
}

# Funciones que necesitan fs como argumento
NEEDS_FS = {"lowpass_filter", "highpass_filter",
            "amplitude_modulate", "attenuate_tone"}


def apply_modification(x, fs, mod):
    if mod["fn"] is None:
        return x.copy()
    func = FUNC_MAP[mod["fn"]]
    if mod["fn"] in NEEDS_FS:
        return func(x, fs=fs, **mod["params"])
    return func(x, **mod["params"])


def main():
    STIMULI_DIR.mkdir(parents=True, exist_ok=True)
    refs = sorted(REFERENCE_DIR.glob("*.wav"))
    if not refs:
        raise FileNotFoundError(f"No se encontraron WAVs en {REFERENCE_DIR}")

    total, clipped = 0, 0
    for ref_path in refs:
        ref_name = ref_path.stem
        x, fs = sf.read(str(ref_path))

        mod_list = list(COMMON_MODIFICATIONS)
        if ref_name in SPECIFIC_MODIFICATIONS:
            mod_list += SPECIFIC_MODIFICATIONS[ref_name]

        print(f"\n{ref_name}:")
        for mod in mod_list:
            y = apply_modification(x, fs, mod)
            peak = np.max(np.abs(y))
            rms  = np.sqrt(np.mean(y**2))

            flag = ""
            if peak > 0.99:
                flag = "  ⚠️ CLIP"
                clipped += 1

            out_path = STIMULI_DIR / f"{ref_name}__{mod['name']}.wav"
            sf.write(str(out_path), y, fs)
            print(f"  {mod['name']:18s}  RMS={rms:.4f}  peak={peak:.3f}{flag}")
            total += 1

    print(f"\nGenerados {total} estímulos en {STIMULI_DIR}/")
    if clipped:
        print(f"⚠️  {clipped} estímulos con clipping — revisa parámetros")


if __name__ == "__main__":
    main()