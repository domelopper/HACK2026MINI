import asyncio
from video_analyzer import VideoAnalyzer
from gemini_coach   import GeminiCoach

API_KEY = "AIzaSyC9qx7WZR-joQPamj1LvrnVpLxnrX02mMU"
MODEL   = "gemini-3.1-flash-live-preview"

async def main():
    # 1. Analizar video → string
    prompt = VideoAnalyzer("Video.mp4").get_prompt()
    print(prompt)

    # 2. Mandar string a Gemini
    await GeminiCoach(API_KEY, MODEL).analizar(prompt)

asyncio.run(main())