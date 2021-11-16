import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    data = bytearray()
    while True:
        chunk = await reader.read()
        print(len(chunk))
        if not chunk:
            break
        data += chunk

    print(len(data))

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client('Hello World!'))

