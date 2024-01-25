from glob import glob
from Bits_sample import bits_per_sample
from FFT_process import fft_process
from Validador import Validador
import Equalizer as eq


FACTOR_DECIMACION = 5


def ecualizador(song):

    try:
        FFT, freqs, Fs = fft_process(song, factor=FACTOR_DECIMACION)
    except:
        print('No se pudo leer el audio')
        return

    print('<1> Sub-Bass\n<2> Bass\n<3> Low-Midrange\n<4> Upper-Midrange\n<5> Presence\n<6> Brilliance')
    tipo_filtro = Validador.val_int('Escoja el tipo de filtro')

    if tipo_filtro not in range(1, 7):
        print('Opcion no valida')
        return

    gain_out_freqs = Validador.val_float('Ingrese la ganancia para las frecuencias fuera del filtro')
    gain_in_freqs = Validador.val_float('Ingrese la ganancia para las frecuencias dentro del filtro')
    filter, name_filter, cortes = eq.filters(freqs, tipo_filtro, gain_out_freqs, gain_in_freqs)

    while(True):

        print('<1> Reproducir audio\n<2> Informacion\n<3> Graficas\n<4> Salir')
        option = input('>> ')

        match option:

            case '1':
                eq.equalizer_play(eq.equalize(FFT, filter), Fs, factor=FACTOR_DECIMACION)
            
            case '2':
                print('Bits por muestra:', bits_per_sample(song))
                print('Frecuencia de muestreo:', Fs)
                print('Frecuencias ingresadas:', cortes[0], 'Hz', cortes[1], 'Hz')
                print('Filtro usado:', name_filter)

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
                print('No hay audio') if file == '' else ecualizador(file)

            case '3':
                print('Saliendo...')
                return
            
            case _:
                print("Opcion no valida")


if __name__ == '__main__':
    run()
