from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np

encoder = VoiceEncoder()

def prueba_resemblyzer():
    wav_path = "../temp.wav"  # Ruta al archivo de audio
    try:
        wav = preprocess_wav(wav_path)
    except Exception as e:
        print(f"Error al cargar el archivo WAV: {e}")
        return

    huella_voz = encoder.embed_utterance(wav)
    print("Embedding generado con éxito:", huella_voz)

if __name__ == "__main__":
    prueba_resemblyzer()

