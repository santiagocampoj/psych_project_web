import argparse
import subprocess
import sys
import time



STEPS = [
    ("Preprocesado de referencias", ["python", "-m", "src.preprocessing"]),
    ("Generación de estímulos", ["python", "-m", "scripts.generate_stimuli"]),
    ("Cómputo de métricas", ["python", "-m", "scripts.compute_metrics"]),
]


def parse_args():
    p = argparse.ArgumentParser(description="Pipeline del experimento")
    p.add_argument("--skip", type=int, nargs="*", default=[],
                   help="Pasos a saltar (1-indexed)")
    p.add_argument("--only", type=int, nargs="*", default=[],
                   help="Solo correr estos pasos (1-indexed)")
    return p.parse_args()


def main():
    args = parse_args()
    bar = "=" * 60

    for i, (name, cmd) in enumerate(STEPS, 1):
        if args.only and i not in args.only:
            continue
        if i in args.skip:
            print(f"⏭️   [{i}/{len(STEPS)}] saltando: {name}")
            continue

        print(f"\n{bar}\n  [{i}/{len(STEPS)}] {name}\n{bar}")
        t0 = time.time()
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"\n❌ Fallo en paso {i}: {name}")
            sys.exit(1)
        print(f"   ({time.time() - t0:.1f}s)")

    print(f"\n{bar}\n  ✅ Pipeline completo\n{bar}")


if __name__ == "__main__":
    main()