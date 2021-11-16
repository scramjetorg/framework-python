from datastream import DataStream
from multiprocessing import Process
import asyncio
import os
import time
from ansi_color_codes import *
import utils
import sys
from test.large_test_files import path_to_text_without_newlines

log = utils.LogWithTimer.log
maxp = 4

# transformacje:
# - na koniec liczyć chunki/sumę bajtów?
# - coś takiego żeby było przetwarzanie stringów, a nie bytesów. Najprościej doklejać stringa.

async def echo(x):
    log(f"{yellow}Processing:{reset} {repr(x)}")
    return x

def run(coro):
    print(f"\n{strong}Running {coro.__name__}:{reset}")
    asyncio.run(coro())

def check_if_string(chunk):
    if not isinstance(chunk, str):
        print(f'Got {type(chunk)}, not str!')
    return chunk

def count_and_sum(accumulator, item):
    chunk_count, combined_length = accumulator
    return (chunk_count + 1, combined_length + len(item))

async def read_large_file():
    FILE = path_to_text_without_newlines
    res = await DataStream.from_file(FILE).map(check_if_string).reduce(count_and_sum, (0, 0))
    print(f'Read {res[0]} chunks, {res[1]} bytes in total.')

run(read_large_file)


async def read_from_stdin():
    pass


async def read_from_unix_pipe():
    pass


async def read_from_large_file_object():
    pass


async def read_from_async_fifo():
    pass


async def read_from_sync_iterable():
    pass


async def read_with_changed_chunk_size():
    pass


async def read_large_data_from_tcp():
    pass


async def read_from_another_stream():
    pass
