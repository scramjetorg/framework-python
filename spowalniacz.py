from scramjet.streams import DataStream
import asyncio
import random
import sys

source = [sys.argv[1], sys.argv[2]]
dest = ['localhost', sys.argv[3]]

def echo(chunk, descr):
    print(f'{descr} {chunk}')
    return chunk

async def split_into_single_bytes(bytes_array):
    print("Processing...")
    await asyncio.sleep(random.uniform(1, 2))
    return [bytes_array[i:i+1] for i in range(len(bytes_array))]

async def delay(chunk):
    await asyncio.sleep(random.uniform(0.5, 1.5))
    return chunk

async def forward(client_reader, client_writer):
    srv_reader, srv_writer = await asyncio.open_connection(*source)
    data = (
        DataStream
            .read_from(srv_reader, max_parallel=1)
            .map(echo, 'Got')
            .flatmap(split_into_single_bytes)
            .map(echo, 'Sending')
            .map(delay)
    )
    async for chunk in data:
        client_writer.write(chunk)
        await client_writer.drain()
    print("Close the connection.")
    client_writer.close()

async def forward_slowly():
    server = await asyncio.start_server(forward, *dest)
    async with server:
        print(f'Forwarding fruits from {source} to {dest}, slowly...')
        await server.serve_forever()

asyncio.run(forward_slowly())
