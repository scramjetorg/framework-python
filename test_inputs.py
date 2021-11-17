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
LARGE_FILE = path_to_text_without_newlines

async def echo(x):
    log(f"{yellow}Processing:{reset} {repr(x)}")
    return x

def run(coro):
    print(f"\n{strong}Running {coro.__name__}:{reset}")
    res = asyncio.run(coro())
    print(f'Read {res[0]} chunk(s) of type(s) {res[1]}, {res[2]} bytes in total.')

def analyze_chunks(accumulator, chunk):
    chunk_count, chunk_types, combined_length = accumulator
    chunk_types.add(type(chunk))
    return (chunk_count + 1, chunk_types, combined_length + len(chunk))


# default reading (bulk)

async def read_from_path():
    s = DataStream.from_file(LARGE_FILE)
    return await s.reduce(analyze_chunks, (0, set(), 0))
run(read_from_path)

async def read_from_file_object():
    with open(LARGE_FILE) as f:
        s = DataStream.from_iterable(f)
        return await s.reduce(analyze_chunks, (0, set(), 0))
run(read_from_file_object)

async def read_from_tcp_socket():
    pass

async def read_from_another_stream():
    s = DataStream.from_iterable(DataStream.from_file(LARGE_FILE))
    return await s.reduce(analyze_chunks, (0, set(), 0))
run(read_from_another_stream)


# async reading - should be non-blocking and immediate


# changing buffering (chunk size, reading lines)


### other sources and special cases

async def read_from_unix_socket():
    pass

async def read_from_websocket():
    pass

async def read_from_stdin():
    pass

async def read_from_unix_pipe():
    pass
