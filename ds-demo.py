from datastream import DataStream
import asyncio
import aiofiles
from ansi_color_codes import *
import sys
import os
import re
import utils
log = utils.LogWithTimer.log

os.makedirs("processing", exist_ok=True)

# transformations
async def start(data):
    chunk = data.rstrip()
    log(f"{yellow}Start processing:{reset} {repr(chunk)}")
    open(f"processing/{chunk}", 'w').close()
    return chunk

async def no_numbers(x):
    await asyncio.sleep(1)
    if re.match('[0-9]+', x):
        log(f"{cyan}drop:{reset} {repr(x)}")
        os.remove(f"processing/{x}")
        return False
    return True

async def count(x):
    log(f"{yellow}Start counting:{reset} {repr(x)}")
    length = len(x)
    await asyncio.sleep(length)
    log(f"{green}Finished counting{reset} - {x}: {length}")
    os.remove(f"processing/{x}")
    return f'{x}: {length}\n'


# streaming
async def main():
    in_file = sys.argv[1]
    out_file = sys.argv[2]

    async with aiofiles.open(in_file) as src:
        await (
            DataStream
                .from_iterable(src, max_parallel=4)
                .map(start)
                .filter(no_numbers)
                .map(count)
                .to_file(out_file)
        )

asyncio.run(main())

