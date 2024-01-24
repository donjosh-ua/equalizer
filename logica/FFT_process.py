import scipy.fft as fft
from scipy.io.wavfile import read

def fft_process(file_name):
    #Leer el archivo de audio 
    Fs, audio = read(file_name)

    #Cambiar a un solo canal si el audio es de dos canales y suavizar audio wav
    if audio.ndim == 1 :
        audio = audio.reshape(-1)
    else :
        audio = audio[:, 0].ravel()

        
    #FTT es un arreglo con la transformada de fourier real
    FFT = fft.fft(audio)

    #Asocia la amplitudes con su frecuencia determinada
    freqs = fft.fftfreq(len(FFT), 1.0 / Fs)

    return FFT, freqs, Fs



