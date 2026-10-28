import asyncio
from pathlib import Path
import edge_tts

OUT = Path('audio')
OUT.mkdir(exist_ok=True)
VOICE = 'ar-SA-HamedNeural'
COUNTERS = {1:'واحد',2:'اثنين',3:'ثلاثة',4:'أربعة'}

async def main():
    for number, word in COUNTERS.items():
        path = OUT / f'counter{number}.mp3'
        text = f'الرجاء التوجه إلى الشباك رقم {word}'
        for attempt in range(5):
            try:
                await edge_tts.Communicate(text, VOICE, rate='-5%').save(str(path))
                if path.stat().st_size > 1000:
                    print(f'Created {path}: {text}', flush=True)
                    break
            except Exception as exc:
                print(f'Attempt {attempt+1} failed: {exc}', flush=True)
            await asyncio.sleep(2*(attempt+1))
        else:
            raise RuntimeError(f'Failed to generate {path}')

asyncio.run(main())
