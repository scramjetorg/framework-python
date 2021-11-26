from scramjet.streams import DataStream
import asyncio
import sys

krzysiek = ['172.20.10.131', 9616]
localhost = ['127.0.0.1', 8888]

if len(sys.argv) == 2:
    address = ['127.0.0.1', int(sys.argv[1])]

def echo(chunk, descr):
    print(f'{descr} {chunk}')
    return chunk

async def download_fruits(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    bytes = DataStream.read_from(reader, chunk_size=8).map(echo, 'Got')
    fruits = bytes.decode("UTF-8").map(echo, 'Yummy!')
    salad = await fruits.reduce(lambda a, b: a + b)
    print(f'Serving today: {salad}')

asyncio.run(download_fruits(*address))
