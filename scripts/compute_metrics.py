import csv
from pathlib import Path

from src.metrics import compute_all

STIMULI_DIR = Path("data/stimuli")
RESULTS_DIR = Path("results")
OUTPUT_CSV = RESULTS_DIR / "metrics_table.csv"


def parse_stimulus_name(stem):
    """'pink_noise__lp_1kHz' → ('pink_noise', 'lp_1kHz')."""
    if "__" in stem:
        ref, mod = stem.split("__", 1)
        return ref, mod
    return stem, "baseline"


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    paths = sorted(STIMULI_DIR.glob("*.wav"))
    if not paths:
        raise FileNotFoundError(f"No hay WAVs en {STIMULI_DIR}")

    rows = []
    print(f"Computando métricas de {len(paths)} estímulos...\n")
    for i, p in enumerate(paths, 1):
        ref, mod = parse_stimulus_name(p.stem)
        result = compute_all(p)
        result["reference"] = ref
        result["modification"] = mod
        result["filename"] = p.name
        rows.append(result)
        print(f"  [{i:2d}/{len(paths)}] {p.name:42s}  "
              f"L={result['loudness_sone']:5.2f}  "
              f"S={result['sharpness_acum']:4.2f}  "
              f"R={result['roughness_asper']:5.3f}  "
              f"SII={result['sii']:.3f}")

    columns = ["reference", "modification", "filename", "spl_db",
               "loudness_sone", "sharpness_acum", "roughness_asper", "sii"]
    with open(OUTPUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        for row in rows:
            w.writerow({k: row[k] for k in columns})

    print(f"\n✅ Guardado en {OUTPUT_CSV}")


if __name__ == "__main__":
    main()