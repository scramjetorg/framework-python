from datastream import DataStream
import asyncio
from ansi_color_codes import *
from utils import print_trimmed as trim

def echo(x):
    print(f"{yellow}Echo:{reset} {trim(x)}")
    return x

async def stream_large_file():
    file = '/home/jan/inbox/large-continuous-text-file.txt'
    await (
        DataStream
            .from_file(file)
            .map(echo)
            .to_devnull()
    )

print(f"\n{strong}Running stream_large_file:{reset}")
asyncio.run(stream_large_file())

