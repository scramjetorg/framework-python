from multiprocessing import Process
import asyncio
import os
from test import large_test_files

LARGE_FILE = large_test_files.path_to_text_without_newlines

def serve_with_netcat():
    os.system(f'nc -lN localhost 8888 < {LARGE_FILE}')

server = Process(target=serve_with_netcat)
server.start()

async def async_reader(reader, chunk_size=4096):
    chunk = await reader.read(chunk_size)
    while chunk != b'':
        yield chunk
        chunk = await reader.read(chunk_size)

async def read_from_tcp_socket():
    reader, writer = await asyncio.open_connection('localhost', 8888)
    async for item in async_reader(reader):
        print("Got:", repr(item))
asyncio.run(read_from_tcp_socket())

server.join()


