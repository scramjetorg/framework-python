from datastream import DataStream
from multiprocessing import Process
import asyncio
import os
import time
from ansi_color_codes import *
import utils
import sys
from test import large_test_files

log = utils.LogWithTimer.log
maxp = 4
LARGE_FILE = large_test_files.path_to_text_without_newlines

def run(coro):
    print(f"\n{strong}Running {coro.__name__}:{reset}")
    utils.LogWithTimer.reset()
    res = asyncio.run(coro())
    print(f'Read {res[0]} chunk(s) of type(s) {res[1]}, {res[2]} bytes in total.')

def analyze_chunks(accumulator, chunk):
    chunk_count, chunk_types, combined_length = accumulator
    chunk_types.add(type(chunk))
    return (chunk_count + 1, chunk_types, combined_length + len(chunk))



# reading from continuous file - should split into even chunks

async def read_from_path():
    s = DataStream.from_file(LARGE_FILE)
    return await s.reduce(analyze_chunks, (0, set(), 0))
run(read_from_path)

async def read_from_file_object():
    with open(LARGE_FILE) as file:
        s = DataStream.from_iostream(file)
        return await s.reduce(analyze_chunks, (0, set(), 0))
run(read_from_file_object)

def serve_with_netcat():
    os.system(f'nc -lN localhost 8888 < {LARGE_FILE}')

server = Process(target=serve_with_netcat)
server.start()

async def read_from_tcp_socket():
    reader, writer = await asyncio.open_connection('localhost', 8888)
    s = DataStream.from_socket(reader)
    result = await s.reduce(analyze_chunks, (0, set(), 0))
    writer.close()
    return result
run(read_from_tcp_socket)

server.join()

async def read_from_another_stream():
    s = DataStream.from_iterable(DataStream.from_file(LARGE_FILE))
    return await s.reduce(analyze_chunks, (0, set(), 0))
run(read_from_another_stream)


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
