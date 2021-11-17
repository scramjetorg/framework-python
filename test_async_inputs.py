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

def run(coro):
    print(f"\n{strong}Running {coro.__name__}:{reset}")
    utils.LogWithTimer.reset()
    return asyncio.run(coro())


# async reading - should be non-blocking and immediate

async def async_ordinal(x):
    log(f'{yellow}ordinal start:{reset} {x.decode()}')
    await asyncio.sleep(1)
    result = ord(x.decode().upper()) - 64
    log(f'{yellow}ordinal end:{reset} {x.decode()} -> {result}')
    return result


def echo_with_netcat():
    os.system(f"(echo a; echo b; echo c; sleep 3; echo d; echo e; echo f) | nc -lN localhost 9999")
    # os.system(f"(echo -e 'a\nb\nc\n'; sleep 1; echo -e 'd\ne\nf\n') | nc -lN localhost 8888")

server = Process(target=echo_with_netcat)
server.start()

async def read_from_tcp_socket():
    reader, writer = await asyncio.open_connection('localhost', 9999)
    s = DataStream.from_socket(reader, max_parallel=2)
    result = await s.flatmap(lambda s: s.split()).map(async_ordinal).to_list()
    writer.close()
    return result
run(read_from_tcp_socket)


server.join()
PIPE = 'test_pipe'
try:
    os.remove(PIPE)
except FileNotFoundError:
    pass
os.mkfifo(PIPE)

def write_to_pipe():
    with open(PIPE, 'w') as pipe:
        pipe.write('a\nb\nc\n')
        pipe.flush()
        time.sleep(3)
        pipe.write('d\ne\nf\n')
        pipe.flush()


async def read_from_path():
    write = Process(target=write_to_pipe)
    write.start()
    s = DataStream.from_file(PIPE, max_parallel=2)
    
    return await s.flatmap(lambda s: s.split()).map(async_ordinal).to_list()
    write.join()
run(read_from_path)


async def read_from_file_object():
    write = Process(target=write_to_pipe)
    write.start()
    with open(PIPE) as f:
        s = DataStream.from_iostream(f, max_parallel=2)
        return await s.flatmap(lambda s: s.split()).map(async_ordinal).to_list()
    write.join()
run(read_from_file_object)
