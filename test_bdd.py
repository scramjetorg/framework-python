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

def is_sentence_end(string):
    return string[-1] == '.'

def join_words(words):
    return " ".join(words)

# Chunk size can be controlled, and newlines don't affect it.
async def main():
    SIZE = 32
    FILE = 'sample_text_4.txt'
    result = await (
        DataStream
            .from_file(FILE, max_chunk_size=SIZE)
            .map(echo, 'chunk', blue)
            .map(lambda raw: raw.decode("utf-8"))
            .sequence(lambda s: s.split(' '))
            .map(echo, 'word', grey)
            .aggregate(is_sentence_end, join_words)
            .map(echo, 'sentence', yellow)
            .map(lambda sentence: len(sentence.split()))
            .average()
    )
    print("results:", result)

asyncio.run(main())
