from datastream import DataStream
from multiprocessing import Process
import asyncio
import os
import time
from ansi_color_codes import *
import utils
import sys
from test import large_test_files

# LARGE_FILE = large_test_files.path_to_text_without_newlines
#
# print("binary")
# with open(LARGE_FILE, 'rb') as file:
#     count, length = 0, 0
#     print(repr(file))
#     for chunk in iter(lambda: file.read1(), b''):
#         count += 1
#         length += len(chunk)
#     print(f'Read {count} chunk(s), {length} bytes in total.')
#
# print("text")
# with open(LARGE_FILE) as file:
#     count, length, types = 0, 0, set()
#     print(repr(file))
#     for chunk in iter(lambda: file.read(3000), ''):
#         count += 1
#         length += len(chunk)
#         types.add(type(chunk))
#     print(f'Read {count} chunk(s) of type(s) {types}, {length} bytes in total.')
#
# print("text accessing buffer below")
# with open(LARGE_FILE) as file:
#     count, length, types = 0, 0, set()
#     print(repr(file))
#     print(hasattr(file.buffer, 'read1'))
#     # print(file._has_read1)
#     print(repr(file.buffer))
#     for chunk in iter(lambda: file.buffer.read1(), b''):
#         count += 1
#         length += len(chunk)
#         types.add(type(chunk))
#     print(f'Read {count} chunk(s) of type(s) {types}, {length} bytes in total.')

data = ['f', 'oo', '\n', 'bar baz', ' ', 'bax\nqux']
path = 'test_pipe'

def write_to_pipe():
    with open(path, 'w') as pipe:
        for chunk in data:
            time.sleep(0.01)
            print(f'{yellow}Write into pipe{reset}:', repr(chunk))
            pipe.write(chunk)
            pipe.flush()

# Problem: text files wait until line is complete
print("\nReading from text file")
write = Process(target=write_to_pipe)
write.start()

with open(path) as file:
    for chunk in file:
        print("Got chunk:", repr(chunk))

write.join()


# Binary files can walk arou nd this
print("\nReading from binary file")
write = Process(target=write_to_pipe)
write.start()

with open(path, 'rb') as file:
    for chunk in iter(lambda: file.read(), b''):
        print("Got chunk:", repr(chunk))

write.join()


# But text files don't have this API
print("\nText file with read()")
write = Process(target=write_to_pipe)
write.start()

with open(path) as file:
    for chunk in iter(lambda: file.read(4), ''):
        print("Got chunk:", repr(chunk))

write.join()


# Solution??
print("\nText file with underlying buffer method swapped")
write = Process(target=write_to_pipe)
write.start()

with open(path) as file:
    file.buffer.read = file.buffer.read1
    for chunk in iter(lambda: file.read(), ''):
        print("Got chunk:", repr(chunk))

write.join()

# Binary files can walk around this
print("\nno buffering, raw")
write = Process(target=write_to_pipe)
write.start()

with open(path, 'rb', buffering=0) as file:
    for chunk in iter(lambda: file.read(10), b''):
        print("Got chunk:", repr(chunk))

write.join()

