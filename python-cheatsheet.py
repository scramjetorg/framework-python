# BASICS ----------------------------------------

# create object of class Foo
f = Foo()

# generate a sequence of numbers
range(100)

# using async functions
import asyncio
async def say_later():
    await asyncio.sleep(1)
    print("Hello")

# lambda functions:
foo = lambda x: "foo"+x
# is equivalent to:
def foo(x):
    return "foo"+x



# FILES -----------------------------------------

path = '/tmp/example-file'

# reading from file (in text mode)
with open(path) as file:

    # read specific amount of data:
    data = file.read(1024)
    print(data)

    # iterate over file contents:
    for line in file:
        print(line)

# writing to a file:
with open(path, 'w') as file:
    file.write("foo bar")



# MISC ------------------------------------------

# splitting strings
"foo bar\nqux".split()    # -> ['foo', 'bar', 'qux']
"foo,bar,qux".split(',')  # -> ['foo', 'bar', 'qux']


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
