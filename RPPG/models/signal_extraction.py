import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

def bandpass_filter(signal, fs, low=0.75, high=3.0):
    b, a = butter(3, [low / (0.5 * fs), high / (0.5 * fs)], btype='band')
    return filtfilt(b, a, signal)

def compute_heart_rate(signals, timestamps):
    fs = len(timestamps) / max((timestamps[-1] - timestamps[0]), 1e-6)

    signal = bandpass_filter(signals[:, 1], fs)
    peaks, _ = find_peaks(signal, distance=fs / 2)
    rr_intervals = np.diff(timestamps[peaks])
    return 60.0 / np.mean(rr_intervals) if len(rr_intervals) > 0 else 0

def compute_respiration_rate(signals, timestamps):
    fs = len(timestamps) / max((timestamps[-1] - timestamps[0]), 1e-6)

    low_signal = bandpass_filter(signals[:, 0], fs, low=0.1, high=0.5)
    peaks, _ = find_peaks(low_signal, distance=fs * 2)
    return len(peaks) / (timestamps[-1] - timestamps[0]) * 60 if len(peaks) > 0 else 0

def compute_hrv(signals, timestamps):
    fs = len(timestamps) / max((timestamps[-1] - timestamps[0]), 1e-6)

    signal = bandpass_filter(signals[:, 1], fs)
    peaks, _ = find_peaks(signal, distance=fs / 2)
    rr_intervals = np.diff(timestamps[peaks]) * 1000
    return np.std(rr_intervals) if len(rr_intervals) > 1 else 0
