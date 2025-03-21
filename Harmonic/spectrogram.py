import soundfile as sf
from pathlib import Path
import librosa
import numpy as np
import matplotlib.pyplot as plt

TICKS = np.array([31.25, 62.5, 125, 250, 500, 1000, 2000, 4000, 8000])
TICK_LABELS = np.array(["31.25", "62.5", "125", "250", "500", "1k", "2k", "4k", "8k"])

def spectrogram(signal, sample_rate, output_path: Path): #If not working as expected, try the previos version with parameters
    
    n_fft=2048 
    hop_length = 512
    window_type = 'hann'
    
    stft = librosa.stft(signal, n_fft=n_fft, hop_length=hop_length, window=window_type, center=True) # Short-time Fourier transform
    power_spectrogram = np.abs(stft)**2
    spectrogram_db = librosa.power_to_db(power_spectrogram, ref=np.max)
    
    plt.figure(figsize=(10, 4))
    img = librosa.display.specshow(
        spectrogram_db,
        y_axis='log',
        x_axis='time',
        sr=sample_rate,
        cmap='inferno',
        hop_length=hop_length,
        # window=window_type,
        n_fft=n_fft
    )
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.yticks(TICKS, TICK_LABELS)
    plt.colorbar(img, format="%+2.f dBFS")
    plt.show()

def main():
    plt.rcParams.update({"font.size": 20})
    signal, sample_rate = librosa.load(
        Path("recordings") / "001 AL FATIHAH.wav",
        sr=None,
        mono=True,
        dtype='float32'
    )
    print(f'Sample rate: {sample_rate}')
    spectrogram(signal, sample_rate, Path('img') / 'spectrogram.png')

if __name__ == "__main__":
    main()