import asyncio
import pyaudio
from google import genai
from google.genai import types

API_KEY = "AIzaSyC9qx7WZR-joQPamj1LvrnVpLxnrX02mMU"
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-3.1-flash-live-preview"

SAMPLE_RATE = 24000
CHANNELS = 1
FORMAT = pyaudio.paInt16

# ─── TU SERIE DE ÁNGULOS (como si fueran frames) ──────────────────
serie_angulos = [
    {"frame": 1, "angulo_brazo": 30, "angulo_muneca": 90,  "angulo_cuerpo": 20},
    {"frame": 2, "angulo_brazo": 45, "angulo_muneca": 100, "angulo_cuerpo": 25},
    {"frame": 3, "angulo_brazo": 75, "angulo_muneca": 120, "angulo_cuerpo": 40},
    {"frame": 4, "angulo_brazo": 90, "angulo_muneca": 130, "angulo_cuerpo": 45},  # impacto
    {"frame": 5, "angulo_brazo": 60, "angulo_muneca": 110, "angulo_cuerpo": 35},
]

async def analizar_serie():
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        system_instruction="""
        Eres un entrenador experto en ping pong. 
        Recibirás ángulos frame por frame de un saque.
        Al final da un análisis completo y recomendaciones en español., utiliza un acento argentino
        """
    )

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, output=True)

    async with client.aio.live.connect(model=MODEL, config=config) as session:

        # 1️⃣ Enviar todos los ángulos frame por frame
        print("📤 Enviando ángulos...")
        for angulo in serie_angulos:
            await session.send_realtime_input(
                text=f"Frame {angulo['frame']}: brazo={angulo['angulo_brazo']}°, "
                     f"muñeca={angulo['angulo_muneca']}°, "
                     f"cuerpo={angulo['angulo_cuerpo']}°"
            )
            await asyncio.sleep(0.1)  # pequeña pausa entre frames

        # 2️⃣ Pedir el análisis final
        await session.send_realtime_input(
            text="Ya tienes todos los frames del saque. Da tu análisis completo y recomendaciones."
        )

        # 3️⃣ Reproducir la respuesta de voz
        print("🔊 Gemini analizando y hablando...")
        async for response in session.receive():
            if response.data:
                stream.write(response.data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("✅ Listo")

asyncio.run(analizar_serie())