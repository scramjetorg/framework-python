from scramjet.streams import Stream
from scramjet.pyfca import DropChunk
import asyncio
from scramjet.ansi_color_codes import *
import scramjet.utils as utils
import pytest

log = utils.LogWithTimer.log

# transformations

async def async_is_even(x):
    await asyncio.sleep((x%5)/100)
    return x % 2 == 0

async def async_square(x):
    await asyncio.sleep((x%5)/100)
    return x**2

async def echo(x):
    log(f"{yellow}Processing:{reset} {repr(x)}")
    return x


# test cases

@pytest.mark.asyncio
async def test_simple_filtering():
    stream = Stream.from_iterable(range(12))
    result = await stream.filter(lambda x: x % 2 == 0).to_list()
    assert result == [0, 2, 4, 6, 8, 10]

@pytest.mark.asyncio
async def test_simple_filtering_with_args():
    stream = Stream.from_iterable(range(12))
    def foo(x, *args):
        return x < sum(args)
    result = await stream.filter(foo, 3, 5).to_list()
    assert result == [0, 1, 2, 3, 4, 5, 6, 7]

@pytest.mark.asyncio
async def test_simple_mapping():
    stream = Stream.from_iterable(range(8))
    result = await stream.map(lambda x: x**2).to_list()
    assert result == [0, 1, 4, 9, 16, 25, 36, 49]

@pytest.mark.asyncio
async def test_sync_transformations():
    result = await (
        Stream
            .from_iterable(range(12), max_parallel=4)
            .filter(lambda x: x % 2 == 0)
            .map(lambda x: x**2)
            .to_list()
    )
    assert result == [0, 4, 16, 36, 64, 100]

@pytest.mark.asyncio
async def test_async_transformations():
    result = await (
        Stream
            .from_iterable(range(12), max_parallel=4)
            .filter(async_is_even)
            .map(async_square)
            .to_list()
    )
    assert result == [0, 4, 16, 36, 64, 100]

# Stream should not start consuming input until a "sink" metod (e.g. to_list)
# is used (to avoid processing items before all transformations are added).
@pytest.mark.asyncio
async def test_adding_transformations_after_a_pause():
    result = Stream.from_iterable(range(12), max_parallel=4)
    # Let event loop run several times, to ensure that any writes to pyfca
    # if they were sheduled) had a chance to run.
    for _ in range(8):
        await asyncio.sleep(0)
    # Stream should not be consumed before transformations are added.
    result = await result.filter(async_is_even).map(async_square).to_list()
    assert result == [0, 4, 16, 36, 64, 100]

@pytest.mark.asyncio
async def test_filter_creates_new_stream_instance():
    stream = Stream.from_iterable(range(12), max_parallel=4)
    filtered = stream.filter(lambda x: x % 2 == 0)
    assert filtered != stream
    assert await filtered.to_list() == [0, 2, 4, 6, 8, 10]

@pytest.mark.asyncio
async def test_map_creates_new_stream_instance():
    stream = Stream.from_iterable(range(8), max_parallel=4)
    mapped = stream.map(lambda x: x**2)
    assert mapped != stream
    assert await mapped.to_list() == [0, 1, 4, 9, 16, 25, 36, 49]

@pytest.mark.asyncio
async def test_filtering_in_map_transformation():
    stream = Stream.from_iterable(range(8), max_parallel=4)
    # It should be possible to do filteing and mapping in one step.
    def filtering_map(x):
        # map and filter elements in one step
        return DropChunk if x % 3 == 0 else x*2
    result = await stream.map(filtering_map).to_list()
    assert result == [2, 4, 8, 10, 14]

@pytest.mark.asyncio
async def test_variadic_args():
    stream = Stream.from_iterable(range(8))
    # pow requires 2 arguments - base (chunk) and exponent (set to 2)
    result = await stream.map(pow, 2).to_list()
    assert result == [0, 1, 4, 9, 16, 25, 36, 49]

@pytest.mark.asyncio
async def test_transformations_on_data_from_file_object():
    with open("test/sample_numbers_1.txt") as f:
        stream = Stream.from_iterable(f, max_parallel=4)
        result = await (
            stream
                .map(echo)
                .map(lambda s: int(s.strip()))
                .filter(lambda x: x % 2 == 0)
                .map(lambda x: x**2)
                .map(lambda x: str(x))
                .to_list()
        )
        assert result == ['64', '196', '400', '256']
