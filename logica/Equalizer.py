import numpy as np
import scipy.fft as fft
import sounddevice as sd
from matplotlib import pyplot as plt

def equalize(FFT, filter):
    return FFT * filter

def filters(freqs, cutoff_begin, cutoff_end):
    
    freq_name = {(16, 60): 'Sub-Bass',
                 (60, 250): 'Bass',
                 (250, 2000): 'Low Mids',
                 (2000, 4000): 'High Mids',
                 (4000, 6000): 'Presence',
                 (6000, 16000): 'Brilliance',
    }

    filtro = np.zeros(len(freqs))
    filter_name = 'Default'  # Valor predeterminado si no se encuentra en ningún rango

    for tupla, nombre in freq_name.items():
        if cutoff_begin in range(tupla[0], tupla[1]) and cutoff_end in range(tupla[0], tupla[1]):
            filtro[(freqs >= cutoff_begin) & (freqs < cutoff_end)] = 1
            filter_name = nombre  # Actualizar el nombre del filtro

    return filtro, filter_name


def equalizer_plot(FFT, freqs, filter, filter_name):
    
    plt.figure(figsize=(15, 10))

    plt.subplot(3, 1, 1)
    plt.plot(freqs[:len(FFT) // 2], np.abs(FFT)[:len(FFT) // 2], label = 'FFT audio input', color = 'blue')
    plt.ylabel('Amplitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.title('Espectro de Frecuencia del Audio (Antes de Ecualización)')

    # Visualizar el filtro 
    plt.subplot(3, 1, 2)

    plt.plot(freqs[:len(FFT) // 2], filter[:len(FFT) // 2], label = filter_name, color = 'red')
    plt.ylabel('Amplitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.title('Respuesta en Frecuencia del Filtro')
    plt.legend()

    # Visualizar el espectro de frecuencia después de aplicar el filtro 
    plt.subplot(3, 1, 3)
    plt.plot(freqs[:len(FFT) // 2], np.abs(equalize(FFT, filter))[:len(FFT) // 2], label = 'FFT audio output', color = 'green')
    plt.ylabel('Amplitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.title('Espectro de Frecuencia del Audio (Después de Ecualización)')
    plt.legend()

    plt.tight_layout()
    plt.show()

def equalizer_play(equalizer, Fs):
    
    # Obtener la señal ecualizada en el dominio del tiempo
    audio_ecualizado = np.real(fft.ifft(equalizer))

    # Normalizar la señal para evitar problemas de saturación
    audio_ecualizado /= np.max(np.abs(audio_ecualizado))

    # Reproducir la señal ecualizada
    sd.play(audio_ecualizado, Fs)
    sd.wait()  # Esperar a que termine la reproducción
