import wave
import numpy as np
import scipy.fft as fft
import sounddevice as sd
from scipy.io.wavfile import read
from matplotlib import pyplot as plt



def bits_per_sample(file_name):
    # Leer el archivo WAV con wave
    with wave.open(file_name, 'rb') as wav_file:
        # Obtener la resolución en bits
        bits_per_sample = wav_file.getsampwidth() * 8

    print(f"Bits por muestra: {bits_per_sample}")


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


option = 0
file_name = ""

while(option != 3):
    option = int(input("1.Elegir audio\n2.Ecualizar\n3.Salir\n"))

    if option == 1:
        file_name = "./datos/Shawn Mendes - Treat You Better.wav"

    elif option == 2:
        FFT, freqs, Fs = fft_process(file_name)
            
        cutoff_begin = int(input("Ingresar frecuencia inicial del filtro\n"))
        cutoff_end = int(input("Ingresar frecuencia final del filtro\n"))


        filter, name_filter = filters(freqs, cutoff_begin, cutoff_end)

        option = 0
        while(option != 4):
            option = int(input("1.Reproducir audio\n2.Informacion\n3.Graficas\n4.Atras\n"))
               
            if option == 1:
                equalizer_play(equalize(FFT, filter), Fs)

            elif option == 2:
                bits_per_sample(file_name)
                print('Frecuencia de muestreo', Fs)
                print('Frecuencias ingresadas', cutoff_begin, ' ', cutoff_end)
                print('Filtro usado', name_filter)

            elif option == 3:
                equalizer_plot(FFT, freqs, filter, name_filter)
        
        option = 0
                
                










        



