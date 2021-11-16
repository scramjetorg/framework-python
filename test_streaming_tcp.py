from datastream import DataStream
import asyncio
from ansi_color_codes import *
from utils import print_trimmed as trim

async def echo(x):
    print(f"{yellow}Echo:{reset} {trim(x)}")
    await asyncio.sleep(0.02)
    return x

async def stream_from_tcp():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    bytes_recv = await (
        DataStream
            .from_socket(reader)
            .map(echo)
            .map(lambda chunk: len(chunk))
            .reduce(lambda a, b: a+b)
    )
    print('Close the connection')
    writer.close()
    print(bytes_recv)

asyncio.run(stream_from_tcp())

