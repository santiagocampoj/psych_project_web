# Psychoacoustics Project — Perceptual analysis pipeline

Study of how controlled audio modifications (filtering, level change, amplitude modulation, tone attenuation) affect **standard psychoacoustic metrics** (Loudness, Sharpness, Roughness, SII) and, in a second phase, the **perceptual responses** of listeners.

## Pipeline

```
data/reference_raw/              ← raw WAVs (4 references)
       │
       ▼  src/preprocessing.py
data/reference/                  ← mono, 48 kHz, 5 s, RMS=0.05
       │
       ▼  scripts/generate_stimuli.py
data/stimuli/                    ← 42 modified stimuli
       │
       ▼  scripts/compute_metrics.py
results/metrics_table.csv        ← metrics per stimulus
       │
       ▼  app/  (pending)
results/responses.csv            ← listener ratings (pending)
       │
       ▼  analysis/correlate.ipynb  (pending)
metric ↔ perception correlation
```

## How to reproduce

Requirements: Python 3.10+, `numpy scipy soundfile mosqito`.

```bash
# Full pipeline:
python run_pipeline.py

# Or step by step:
python -m src.preprocessing
python -m scripts.generate_stimuli
python -m scripts.compute_metrics
```

## Structure

```
psych_pro/
├── data/
│   ├── reference_raw/       # raw WAVs (Freesound + synthesized pink noise)
│   ├── reference/           # preprocessed
│   └── stimuli/             # 42 stimuli
├── src/
│   ├── preprocessing.py     # mono, resample to 48 kHz, trim 5 s, fades, RMS=0.05
│   ├── modifications.py     # change_level, lowpass/highpass_filter, AM, attenuate_tone
│   ├── stimuli_config.py    # modification matrix
│   └── metrics.py           # MoSQITo wrapper + fixed Pa scaling
├── scripts/
│   ├── generate_stimuli.py
│   └── compute_metrics.py
├── results/
│   └── metrics_table.csv
├── analysis/                # pending
├── app/                     # pending
├── run_pipeline.py
└── README.md
```

## Design decisions

**Fixed Pa scaling.** The RMS=0.05 in preprocessed WAVs represents a 70 dB SPL baseline. The factor `SCALING_TO_PA = 1.264` is **the same for all 42 stimuli** — this is why level modifications are preserved (a +6 dB stimulus is correctly computed at 76 dB SPL).

**Modifications do not re-normalize RMS.** If a low-pass removes energy, SPL drops physically. This reflects the actual perceptual reality of each modification.

**SII computed against `'loud'` speech (~75 dB ANSI).** At `'normal'` level, SII saturates to 0 with 70 dB baseline noise. `'loud'` gives a measurable dynamic range.

**6 dB headroom.** Lower RMS target (0.05 instead of 0.1) allows `change_level(+6)` without clipping.

## Computed metrics

| Metric | Unit | Standard | MoSQITo function |
|---|---|---|---|
| Loudness | sone | ISO 532-1 | `loudness_zwst` |
| Sharpness | acum | DIN 45692 | `sharpness_din_st` |
| Roughness | asper | Daniel-Weber 1997 | `roughness_dw` |
| SII | [0, 1] | ANSI S3.5 | `sii_ansi` |

## Modifications

10 common modifications × 4 references + 2 refrigerator-specific = **42 stimuli**.

| Modification | Parameters | Target metric |
|---|---|---|
| `baseline` | no change | — |
| `level_m6, m3, p3, p6` | ±3, ±6 dB | Loudness |
| `lp_1kHz, 2kHz, 4kHz` | Butterworth order 4 | Sharpness |
| `am70_d05, d10` | AM at 70 Hz, depth 0.5/1.0 | Roughness |
| `tone_62_20dB, 40dB` | refrigerator only, Q=10 | (expected sub-perceptual) |

## Status

- [x] Offline pipeline complete (preprocessing → stimuli → metrics)
- [ ] Exploratory metrics analysis (PCA, metric-metric correlations)
- [ ] Web perceptual test
- [ ] Metric ↔ perception correlation notebook
- [ ] Consonancia/disonancia (range 1-5) & agradable desagradable (or 1-7)