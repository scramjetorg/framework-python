from datastream import DataStream
import asyncio
import pyfca
import utils
from ansi_color_codes import *
from pprint import pprint
import pytest

log = utils.LogWithTimer.log
fmt = utils.print_formatted

@pytest.mark.asyncio
async def test_into():
    s1 = DataStream.from_iterable(range(8), max_parallel=4).map(lambda x: 2*x)
    async def write(stream, chunk):
        await stream.pyfca.write(chunk)
    s2 = DataStream(max_parallel=4, name="s2")
    s1.into(write, s2)
    result = await s2.to_list()
    assert result == [0, 2, 4, 6, 8, 10, 12, 14]

async def test_pipe_into_fs_stream():  # and other things
    pass

# test sklejania pajpów 
# s1 = Stream.from(blah).map(foo); s2 = Stream.from(plask).map(bar); s2.pipe(s1)

@pytest.mark.asyncio
async def test_pipe():
    s1 = DataStream.from_iterable(range(8), max_parallel=4).map(lambda x: 2*x)
    s2 = DataStream(max_parallel=4, name="s2")
    s1.pipe(s2)
    result = await s2.to_list()
    assert result == [0, 2, 4, 6, 8, 10, 12, 14]

def parse_and_square_even_dollars(stream):
    return (
        stream
            .map(lambda s: int(s))
            .filter(lambda x: x % 2 == 0)
            .map(lambda x: x**2)
            .map(lambda x: "$" + str(x))
        )

@pytest.mark.asyncio
async def test_use():
    data = ['8', '25', '3', '14', '20', '9', '13', '16']
    stream = DataStream.from_iterable(data, max_parallel=4)
    result = await stream.use(parse_and_square_even_dollars).to_list()
    assert result == ['$64', '$196', '$400', '$256']
