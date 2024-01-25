import scipy.fft as fft
from scipy.io.wavfile import read
from scipy.signal import decimate


def fft_process(file_name, factor=10):

    # Leer el archivo de audio 
    Fs, audio = read(file_name)

    # Cambiar a un solo canal si el audio es de dos canales y suavizar audio wav
    audio = audio.reshape(-1) if audio.ndim == 1 else audio[:, 0].ravel()

    # Decimar el audio para que sea mas facil de procesar
    audio = decimate(audio, factor)

    # FTT es un arreglo con la transformada de fourier real
    FFT = fft.fft(audio)

    # Asocia la amplitudes con su frecuencia determinada
    freqs = fft.fftfreq(len(FFT), 1.0 / Fs)

    return FFT, freqs, Fs
