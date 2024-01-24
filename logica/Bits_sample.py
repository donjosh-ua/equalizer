import wave


def bits_per_sample(file_name):

    # Leer el archivo WAV con wave
    with wave.open(file_name, 'rb') as wav_file:
        bits_per_sample = wav_file.getsampwidth() * 8

    print(f"Bits por muestra: {bits_per_sample}")
