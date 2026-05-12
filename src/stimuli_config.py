"""
Matriz de modificaciones a aplicar a cada referencia.

COMMON_MODIFICATIONS  → se aplican a todas las referencias
SPECIFIC_MODIFICATIONS → solo aplican a la referencia indicada
                        (ej. attenuate_tone solo tiene sentido en señales tonales)

Cada modificación es un dict con:
    name   : nombre corto que va al nombre del archivo
    fn     : nombre de la función en src.modifications (None = sin modificar)
    params : kwargs que se pasan a la función
"""

COMMON_MODIFICATIONS = [
    {"name": "baseline","fn": None, "params": {}},

    # Nivel — apunta a Loudness (y SII via masking)
    {"name": "level_m6", "fn": "change_level", "params": {"db": -6}},
    {"name": "level_m3", "fn": "change_level", "params": {"db": -3}},
    {"name": "level_p3", "fn": "change_level", "params": {"db": +3}},
    {"name": "level_p6", "fn": "change_level", "params": {"db": +6}},

    # Low-pass — apunta  Sharpness y SII
    {"name": "lp_1kHz", "fn": "lowpass_filter", "params": {"fc": 1000}},
    {"name": "lp_2kHz", "fn": "lowpass_filter", "params": {"fc": 2000}},
    {"name": "lp_4kHz", "fn": "lowpass_filter", "params": {"fc": 4000}},

    # AM a 70 Hz — apunta a Roughness
    {"name": "am70_d05","fn": "amplitude_modulate", "params": {"fmod": 70, "depth": 0.5}},
    {"name": "am70_d10","fn": "amplitude_modulate", "params": {"fmod": 70, "depth": 1.0}},
]

SPECIFIC_MODIFICATIONS = {
    "refrigerator": [
        {"name": "tone_62_20dB", "fn": "attenuate_tone",
         "params": {"f0": 62, "depth_db": 20, "Q": 10}},
        {"name": "tone_62_40dB", "fn": "attenuate_tone",
         "params": {"f0": 62, "depth_db": 40, "Q": 10}},
    ],
}