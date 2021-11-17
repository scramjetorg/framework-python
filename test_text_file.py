from datastream import DataStream
from multiprocessing import Process
import asyncio
import os
import time
from ansi_color_codes import *
import utils
import sys
from test import large_test_files

LARGE_FILE = large_test_files.path_to_text_without_newlines

print("binary")
with open(LARGE_FILE, 'rb') as file:
    count, length = 0, 0
    print(repr(file))
    for chunk in iter(lambda: file.read1(), b''):
        count += 1
        length += len(chunk)
    print(f'Read {count} chunk(s), {length} bytes in total.')

print("text")
with open(LARGE_FILE) as file:
    count, length, types = 0, 0, set()
    print(repr(file))
    for chunk in iter(lambda: file.read(3000), ''):
        count += 1
        length += len(chunk)
        types.add(type(chunk))
    print(f'Read {count} chunk(s) of type(s) {types}, {length} bytes in total.')

print("text accessing buffer below")
with open(LARGE_FILE) as file:
    count, length, types = 0, 0, set()
    print(repr(file))
    print(hasattr(file.buffer, 'read1'))
    # print(file._has_read1)
    print(repr(file.buffer))
    for chunk in iter(lambda: file.buffer.read1(), b''):
        count += 1
        length += len(chunk)
        types.add(type(chunk))
    print(f'Read {count} chunk(s) of type(s) {types}, {length} bytes in total.')

data = ['f', 'oo', '\n', 'bar', ' ', 'baz\nqux']
path = 'test_pipe'
try:
    os.remove(path)
except FileNotFoundError:
    pass
os.mkfifo(path)

def write_to_pipe():
    with open(path, 'w') as pipe:
        for chunk in data:
            time.sleep(0.1)
            print(f'{yellow}Write into{reset} {repr(path)}:', repr(chunk))
            pipe.write(chunk)
            pipe.flush()

# Run in a separate process to avoid having to juggle reads and writes
write = Process(target=write_to_pipe)
write.start()
print("\n\nasync pipe")
with open(path) as file:
    count, length, types = 0, 0, set()
    print(repr(file))
    for chunk in file:
        print("Got chunk:", repr(chunk))
        count += 1
        length += len(chunk)
        types.add(type(chunk))
    print(f'Read {count} chunk(s) of type(s) {types}, {length} bytes in total.')

# Each piece of data written into the pipe should become a separate chunk.
write.join()
