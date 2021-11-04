from datastream import DataStream
import asyncio
import aiofiles
from ansi_color_codes import *
import sys
import os
import re
import utils
log = utils.LogWithTimer.log

def echo(chunk, what, color):
    print(f'{color}Got {what}:{reset} {chunk}')
    return chunk

async def async_split(s):
    await asyncio.sleep(0.01)
    return s.split(' ')

# Chunk size can be controlled, and newlines don't affect it.
async def main():
    SIZE = 32
    await (
        DataStream
            # osobna metoda czy też to powinno być from_file?
            .from_stdin(sys.stdin, max_parallel=4, max_chunk_size=32)
            # .map(echo, 'chunk', blue)
            .map(lambda raw: raw.decode("utf-8"))
            .flatmap(async_split)
            # .map(echo, 'word', grey)
            .map(lambda word: f'{word}: {len(word)}\n'.encode('UTF-8'))
            .to_fobj(sys.stdout)
    )

asyncio.run(main())

# test:
# tr -dc A-Za-z0-9' ' </dev/urandom | tr 0-9 ' ' | head -c 200000 | tee /dev/stderr | python ./test_stdinout.py
