# generating infinite random data
from string import ascii_lowercase
import random

def random_letter_generator():
    while True:
        yield random.choice(ascii_lowercase)



# NETWORK ---------------------------------------

# Reading and writing to/from TCP connection
async def tcp_connection():
    reader, writer = await asyncio.open_connection('localhost', 8888)

    # read specific amount of data (returns bytes):
    data = await reader.read(1024)
    print(data)

    # data from TCP connection is iterable, too:
    async for data in reader:
        print(data)

    # writing data (must be bytes, not string)
    writer.write(b"foo bar")
    await writer.drain()


# Reading from HTTP
import aiohttp

async def get_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
