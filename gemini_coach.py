import asyncio
import pyaudio
import wave
from google import genai
from google.genai import types
from google.genai import errors

class GeminiCoach:
    def __init__(self, api_key, model):
        self.client = genai.Client(api_key=api_key)
        self.model  = model

    async def analizar(self, prompt, output_wav="analisis.wav"):
        config = types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            system_instruction="Eres un entrenador de ping pong. Hablá en español con acento argentino."
        )

        p      = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

        audio_chunks = []

        try:
            async with self.client.aio.live.connect(model=self.model, config=config) as session:
                print("📤 Enviando prompt...")

                # Usar send_client_content con turn_complete=True
                # para que Gemini sepa que debe responder
                await session.send_client_content(
                    turns={"role": "user", "parts": [{"text": prompt}]},
                    turn_complete=True
                )

                print("🔊 Gemini hablando...")
                async for response in session.receive():
                    if response.data:
                        stream.write(response.data)
                        audio_chunks.append(response.data)

                    if response.server_content and response.server_content.turn_complete:
                        print("✅ Gemini terminó de hablar.")
                        break

        except errors.APIError as e:
            print(f"⚠️ Conexión cerrada: {e} — guardando audio recibido...")

        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

            if audio_chunks:
                audio_bytes = b"".join(audio_chunks)
                with wave.open(output_wav, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(24000)
                    wf.writeframes(audio_bytes)
                print(f"💾 Audio guardado en: {output_wav}")
            else:
                print("❌ No se recibió audio.")