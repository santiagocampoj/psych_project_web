"""
Cruza métricas físicas (results/metrics_table.csv) con puntuaciones
perceptuales (CSVs individuales en data/responses/) y calcula correlaciones.

Genera:
  results/correlations.csv          - tabla de r y p por par
  results/correlations_grid.png     - scatter plots (4x2)
  results/correlations_heatmap.png  - heatmap de la matriz de r
"""
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

METRICS_FILE  = Path("results/metrics_table.csv")
RESPONSES_DIR = Path("data/responses")
RESULTS_DIR   = Path("results")

PHYSICAL   = ['loudness_sone', 'sharpness_acum', 'roughness_asper', 'sii']
PERCEPTUAL = ['consonance', 'pleasantness_vs_ref']

PHYS_LABELS = {
    'loudness_sone':   'Loudness (sone)',
    'sharpness_acum':  'Sharpness (acum)',
    'roughness_asper': 'Roughness (asper)',
    'sii':             'SII',
}
PERC_LABELS = {
    'consonance':           'Consonancia',
    'pleasantness_vs_ref':  'Agradabilidad vs ref',
}


def load_data():
    metrics = pd.read_csv(METRICS_FILE)
    rating_files = sorted(RESPONSES_DIR.glob("*.csv"))
    if not rating_files:
        raise FileNotFoundError(f"No hay CSVs de puntuaciones en {RESPONSES_DIR}")
    print(f"Cargando {len(rating_files)} CSVs de puntuaciones...")
    ratings = pd.concat([pd.read_csv(p) for p in rating_files], ignore_index=True)
    n_raters = ratings['rater_id'].nunique()
    print(f"  {n_raters} participantes, {len(ratings)} puntuaciones totales")
    return metrics, ratings


def aggregate(metrics, ratings):
    """Media por estímulo entre todos los raters."""
    agg = ratings.groupby('stimulus')[PERCEPTUAL].mean().reset_index()
    return agg.merge(metrics, left_on='stimulus', right_on='filename', how='inner')


def compute_correlations(df):
    rows = []
    for phys in PHYSICAL:
        for perc in PERCEPTUAL:
            r, p = pearsonr(df[phys], df[perc])
            rows.append({'physical': phys, 'perceptual': perc,
                         'r': r, 'p': p, 'n': len(df)})
    return pd.DataFrame(rows)


def plot_scatter_grid(df, out_path):
    fig, axes = plt.subplots(len(PHYSICAL), len(PERCEPTUAL),
                             figsize=(8, 11), constrained_layout=True)
    for i, phys in enumerate(PHYSICAL):
        for j, perc in enumerate(PERCEPTUAL):
            ax = axes[i, j]
            ax.scatter(df[phys], df[perc], alpha=0.6, s=40,
                       edgecolor='k', linewidth=0.5)
            z = np.polyfit(df[phys], df[perc], 1)
            xs = np.linspace(df[phys].min(), df[phys].max(), 50)
            ax.plot(xs, np.polyval(z, xs), 'r--', alpha=0.6, linewidth=1.2)
            r, p = pearsonr(df[phys], df[perc])
            sig = '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))
            ax.set_title(f"r = {r:.3f}{sig}", fontsize=10)
            if i == len(PHYSICAL) - 1: ax.set_xlabel(PHYS_LABELS[phys])
            if j == 0:                 ax.set_ylabel(PERC_LABELS[perc])
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    print(f"  Guardado: {out_path}")


def plot_heatmap(corr_df, out_path):
    matrix = corr_df.pivot(index='physical', columns='perceptual', values='r')
    matrix = matrix.reindex(PHYSICAL)[PERCEPTUAL]
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(matrix.values, vmin=-1, vmax=1, cmap='RdBu_r', aspect='auto')
    ax.set_xticks(range(len(PERCEPTUAL)))
    ax.set_xticklabels([PERC_LABELS[p] for p in PERCEPTUAL], rotation=15)
    ax.set_yticks(range(len(PHYSICAL)))
    ax.set_yticklabels([PHYS_LABELS[p] for p in PHYSICAL])
    for i in range(len(PHYSICAL)):
        for j in range(len(PERCEPTUAL)):
            r = matrix.values[i, j]
            color = 'white' if abs(r) > 0.5 else 'black'
            ax.text(j, i, f"{r:.2f}", ha='center', va='center',
                    color=color, fontsize=11)
    fig.colorbar(im, ax=ax, label='r de Pearson')
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    print(f"  Guardado: {out_path}")


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    metrics, ratings = load_data()
    df = aggregate(metrics, ratings)
    print(f"\nEstímulos con métricas + puntuaciones: {len(df)}")

    corr = compute_correlations(df)
    print("\nCorrelaciones Pearson:")
    print(corr.to_string(index=False))

    corr.to_csv(RESULTS_DIR / "correlations.csv", index=False)
    print(f"\nGuardado: {RESULTS_DIR / 'correlations.csv'}")

    plot_scatter_grid(df, RESULTS_DIR / "correlations_grid.png")
    plot_heatmap(corr, RESULTS_DIR / "correlations_heatmap.png")


if __name__ == "__main__":
    main()