import wave


def bits_per_sample(file_name):

    # Leer el archivo WAV con wave
    with wave.open(file_name, 'rb') as wav_file:
        return wav_file.getsampwidth() * 8
