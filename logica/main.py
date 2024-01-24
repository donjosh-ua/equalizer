from Bits_sample import bits_per_sample
from FFT_process import fft_process
from glob import glob
from Validador import Validador

import Equalizer as eq


def ecualizador(song):

    FFT, freqs, Fs = fft_process(song)
            
    cutoff_begin = int(input("Ingresar frecuencia inicial del filtro\n"))
    cutoff_end = int(input("Ingresar frecuencia final del filtro\n"))

    filter, name_filter = eq.filters(freqs, cutoff_begin, cutoff_end)

    while(True):

        print("<1> Reproducir audio\n<2> Informacion\n<3> Graficas\n<4> Atras")
        option = input('>> ')

        match option:

            case '1':
                eq.equalizer_play(eq.equalize(FFT, filter), Fs)
            
            case '2':
                bits_per_sample(song)
                print('Frecuencia de muestreo', Fs)
                print('Frecuencias ingresadas', cutoff_begin, ' ', cutoff_end)
                print('Filtro usado', name_filter)

            case '3':
                eq.equalizer_plot(FFT, freqs, filter, name_filter)

            case '4':
                return
            
            case _:
                print("Opcion no valida")


def run():

    file = ''
    songs = glob('./datos' + '/*.wav')
    while(True):
        
        print("<1> Elegir audio\n<2> Ecualizar\n<3> Salir")
        option = input(">> ")
        
        match option:

            case '1':
                for i in range(len(songs)):
                    print(f'<{(i + 1)}> {songs[i].split('/')[-1]}')

                file = songs[Validador.val_int() - 1]

            case '2':
                if file == '':
                    print('No se ha seleccionado ningun audio')
                else:
                    ecualizador(file)

            case '3':
                print('Saliendo...')
                return
            
            case _:
                print("Opcion no valida")


if __name__ == '__main__':
    run()
