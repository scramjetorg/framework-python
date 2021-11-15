from datastream import DataStream
import asyncio
from ansi_color_codes import *
import pytest

# test cases

@pytest.mark.asyncio
async def test_writing_chunks_to_stream():
    stream = DataStream()
    for x in [1, 2, 3, 4]:
        stream.write(x)
    stream.pyfca.end()
    assert [1, 2, 3, 4] == await stream.to_list()

@pytest.mark.asyncio
async def test_reading_chunks_from_stream():
    stream = DataStream.from_iterable('abcd')
    assert await stream.read() == 'a'
    assert await stream.read() == 'b'
    assert await stream.read() == 'c'
    assert await stream.read() == 'd'

@pytest.mark.asyncio
async def test_reading_some_chunks_from_stream():
    stream = DataStream.from_iterable('abcd')
    assert await stream.read() == 'a'
    assert ['b', 'c', 'd'] == await stream.to_list()

@pytest.mark.asyncio
async def test_reading_and_writing_in_turn():
    stream = DataStream()
    for x in [1, 2, 3, 4]:
        await stream.write(x)
        assert await stream.read() == x
    stream.pyfca.end()
