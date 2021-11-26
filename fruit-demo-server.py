from scramjet.streams import DataStream
import random
import asyncio
from fruits import fruit_codes, fruit_mapping

def package_fruit(fruit_code):
    return fruit_mapping[fruit_code].encode("UTF-8")

async def produce_fruits():
    random.seed()
    random_codes = [random.choice(fruit_codes) for _ in range(10)]
    source = DataStream.read_from(random_codes)
    f1 = DataStream().filter(lambda c: c <= 'l').map(package_fruit)
    f2 = DataStream().filter(lambda c: c >= 'l').map(package_fruit)
    source.pipe(f1)
    source.pipe(f2)
    return f1, f2

async def send_fruits(which_stream, reader, writer):
    print(f"Sending serving...")
    streams = await produce_fruits()
    serving = await streams[which_stream].reduce(lambda a, b: a + b)
    writer.write(serving)
    await writer.drain()
    print("Close the connection.")
    writer.close()

async def serve_fruits():
    addr1 = ['127.0.0.1', 8001]
    addr2 = ['127.0.0.1', 8002]
    async def send1(reader, writer):
        await send_fruits(0, reader, writer)
    async def send2(reader, writer):
        await send_fruits(1, reader, writer)
    server1 = await asyncio.start_server(send1, *addr1)
    server2 = await asyncio.start_server(send2, *addr2)
    print(f'Serving fruits on {addr1}...')
    print(f'Serving fruits on {addr2}...')
    async with server1, server2:
        await asyncio.gather(
            server1.serve_forever(), server2.serve_forever()
        )

asyncio.run(serve_fruits())
