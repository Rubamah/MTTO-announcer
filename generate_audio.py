import asyncio
import os
from pathlib import Path
import edge_tts
from num2words import num2words

OUT = Path('audio')
OUT.mkdir(exist_ok=True)
VOICE = 'ar-SA-HamedNeural'

async def make_one(n, semaphore):
    path = OUT / f'{n}.mp3'
    if path.exists() and path.stat().st_size > 1000:
        return
    words = num2words(n, lang='ar')
    text = f'تذكرة رقم {words}'
    async with semaphore:
        for attempt in range(5):
            try:
                await edge_tts.Communicate(text, VOICE, rate='-5%').save(str(path))
                if path.stat().st_size > 1000:
                    print(n, text, flush=True)
                    return
            except Exception as exc:
                print(f'Retrying {n}: {exc}', flush=True)
            await asyncio.sleep(2 * (attempt + 1))
        raise RuntimeError(f'Could not generate ticket {n}')

async def main():
    semaphore = asyncio.Semaphore(2)
    # Small batches to avoid overwhelming the service.
    for start in range(1, 1001, 20):
        await asyncio.gather(*(make_one(n, semaphore) for n in range(start, min(start+20,1001))))
        await asyncio.sleep(1)

asyncio.run(main())
