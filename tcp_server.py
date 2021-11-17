import asyncio
from test.large_test_files import path_to_text_without_newlines
LARGE_FILE = path_to_text_without_newlines

async def serve_small_data(reader, writer):
    data = b'test'
    print(f"Sending {len(data)} bytes...")
    writer.write(data)
    await writer.drain()
    await asyncio.sleep(2)
    print("Close the connection.")
    writer.close()

async def serve_big_file(reader, writer):
    with open(LARGE_FILE, 'rb') as f:
        print(f'reading from {f}')
        data = f.read()
        print(f"Sending {len(data)} bytes...")
        writer.write(data)
        await writer.drain()
    print("Close the connection.")
    writer.close()

async def main():
    server = await asyncio.start_server(serve_big_file, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()

asyncio.run(main())

