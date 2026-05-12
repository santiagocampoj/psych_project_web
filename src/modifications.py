import numpy as np
# from scipy.signal import butter, filtfilt
from scipy.signal import butter, filtfilt, sosfiltfilt


def change_level(x, db):
    """Change the global level. +6 dB is amplitude x2, RMS x2"""
    return x * 10**(db / 20)


def lowpass_filter(x, fs, fc, order=4):
    """Butterworth low-pass zero pahse (filtfilt 2x order)."""
    b, a = butter(order, fc, btype='low', fs=fs)
    return filtfilt(b, a, x)


def highpass_filter(x, fs, fc, order=4):
    """Butterworth high-pass"""
    b, a = butter(order, fc, btype='high', fs=fs)
    return filtfilt(b, a, x)


def amplitude_modulate(x, fs, fmod, depth):
    """
    Amplitud modulation y(t) = x(t) · (1 + depth · sin(2π fmod t))

    fmod 4 Hz it is percieved like slow fluctuation
    fmod 70 Hz is (roughness)
    depth ∈ [0, 1]: modulation index (1 = AM al 100%)
    """
    t = np.arange(len(x)) / fs
    envelope = 1 + depth * np.sin(2 * np.pi * fmod * t)
    return x * envelope


def attenuate_tone(x, fs, f0, depth_db, Q=10):
    """
    attenuate a narrow band centered at f0 by depth_db dB

    Implemetation: subtract a fraction α of the bandpass around f0
        α = 1 − 10**(−depth_db/20)
        y = x − α · bandpass(x, f0 ± f0/(2Q))

    depth_db = 20  → −20 dB en f0  (mantiene el resto)
    depth_db = 40  → depth attenuation
    depth_db = 60+ → notch quasi-total
    high Q is like 20-50 y depth grande
    """
    bw = f0 / Q
    f_low = max(f0 - bw / 2, 1.0)
    f_high = min(f0 + bw / 2, fs / 2 - 1.0)
    sos = butter(4, [f_low, f_high], btype='band', fs=fs, output='sos')
    band = sosfiltfilt(sos, x)
    alpha = 1 - 10**(-depth_db / 20)
    return x - alpha * band