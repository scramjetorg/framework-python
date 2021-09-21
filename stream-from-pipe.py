from datastream import DataStream
import asyncio
from ansi_color_codes import *
import sys

# transformations

async def echo(x):
    print(f"{green}Start processing: {repr(x)}{reset}")
    return x

async def is_even(x):
    await asyncio.sleep((x%5)/10)
    return x % 2 == 0

async def square(x):
    await asyncio.sleep((x%5)/10)
    return x**2

# test cases

async def main():
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    await (
        DataStream(4)
            .from_file(in_file)
            .map(echo)
            .map(lambda s: int(s.strip()))
            .filter(is_even)
            .map(square)
            .map(lambda x: str(x) + '\n')
            .to_file(out_file)
    )

asyncio.run(main())
