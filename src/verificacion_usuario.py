import sounddevice as sd
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from scipy.io.wavfile import write
from db_config import conectar_db

encoder = VoiceEncoder()

def grabar_voz(duracion_segundos=5, fs=16000):
    print("Grabando...")
    audio = sd.rec(int(duracion_segundos * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Grabación completada.")
    return audio.flatten(), fs

def verificar_usuario(nombre_usuario):
    duracion = 5  # Duración de la grabación en segundos
    audio, fs = grabar_voz(duracion)  # Se devuelve también la frecuencia de muestreo

    # Convertir audio a formato WAV y luego a numpy array
    wav_path = "../temp.wav"
    write(wav_path, fs, audio.astype(np.int16))

    # Cargar el archivo WAV y procesar
    wav = preprocess_wav(wav_path)
    huella_actual = encoder.embed_utterance(wav)

    db = conectar_db()
    cursor = db.cursor()

    query = "SELECT huella_voz FROM usuarios WHERE nombre_usuario = %s"
    cursor.execute(query, (nombre_usuario,))
    result = cursor.fetchone()

    if result is None:
        print("Usuario no encontrado.")
        return

    huella_registrada_blob = result[0]
    huella_registrada = np.frombuffer(huella_registrada_blob, dtype=np.float32)

    distancia = np.linalg.norm(huella_registrada - huella_actual)
    print(f"Distancia entre huellas: {distancia}")

    umbral = 0.6
    if distancia < umbral:
        print("Verificación exitosa. Identidad confirmada.")
    else:
        print("Verificación fallida. Identidad no confirmada.")

    cursor.close()
    db.close()


