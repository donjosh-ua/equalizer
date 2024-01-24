import numpy as np
import scipy.fft as fft
import sounddevice as sd
from matplotlib import pyplot as plt


def equalize(FFT, filter):
    return FFT * filter


def filters(freqs, tipo, gain_outter_freqs=0, gain_inner_freqs=1):
    
    freq_name = {1: [(16, 60),      'Sub-Bass'],
                 2: [(60, 250),     'Bass'],
                 3: [(250, 2000),   'Low-Mids'],
                 4: [(2000, 4000),  'High-Mids'],
                 5: [(4000, 6000),  'Presence'],
                 6: [(6000, 16000), 'Brilliance']}

    tupla, nombre = freq_name[tipo]

    filtro = np.empty(len(freqs))
    filtro.fill(gain_outter_freqs)
    filtro[(freqs >= tupla[0]) & (freqs < tupla[1])] = gain_inner_freqs

    return filtro, nombre, tupla


def equalizer_plot(FFT, freqs, filter, filter_name):
    
    lim = len(FFT) // 2

    plt.figure(figsize=(15, 7))

    plt.subplot(3, 1, 1)
    plt.plot(freqs[:lim], np.abs(FFT)[:lim], label='FFT audio input', color='blue')
    plt.ylabel('Amplitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.title('Audio pre-ecualización')

    # Visualizar el filtro 
    plt.subplot(3, 1, 2)

    plt.plot(freqs[:lim], filter[:lim], label=filter_name, color='red')
    plt.ylabel('Amplitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.title('Filtro')
    plt.legend()

    # Visualizar el espectro de frecuencia después de aplicar el filtro 
    plt.subplot(3, 1, 3)
    plt.plot(freqs[:lim], np.abs(equalize(FFT, filter))[:lim], label='FFT audio output', color='green')
    plt.ylabel('Amplitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.title('Audio post-ecualización')
    plt.legend()

    plt.tight_layout()
    plt.show()


def equalizer_play(equalizer, Fs):
    
    # Obtener la señal ecualizada en el dominio del tiempo
    audio_ecualizado = np.real(fft.ifft(equalizer))

    # Normalizar la señal para evitar problemas de saturación
    audio_ecualizado /= np.max(np.abs(audio_ecualizado))

    # Reproducir la señal ecualizada
    # try:
    sd.play(audio_ecualizado, Fs)
    # except:
    #     print('No se pudo reproducir el audio')
    #     return
