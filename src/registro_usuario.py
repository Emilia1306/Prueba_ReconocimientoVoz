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

def registrar_usuario(nombre_usuario):
    duracion = 5  # Duración de la grabación en segundos
    audio, fs = grabar_voz(duracion)  # Se devuelve también la frecuencia de muestreo

    # Convertir audio a formato WAV y luego a numpy array
    wav_path = "../temp.wav"
    write(wav_path, fs, audio.astype(np.int16))
    
    # Cargar el archivo WAV y procesar
    wav = preprocess_wav(wav_path)
    huella_voz = encoder.embed_utterance(wav)
    huella_voz_blob = huella_voz.tobytes()

    db = conectar_db()
    cursor = db.cursor()

    query = "INSERT INTO usuarios (nombre_usuario, huella_voz) VALUES (%s, %s)"
    cursor.execute(query, (nombre_usuario, huella_voz_blob))
    db.commit()

    print(f"Usuario {nombre_usuario} registrado con éxito.")
    cursor.close()
    db.close()

