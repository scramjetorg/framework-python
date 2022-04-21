from scramjet.streams import Stream
import asyncio
import scramjet.utils as utils
from scramjet.ansi_color_codes import *
import pytest

log = utils.LogWithTimer.log
fmt = utils.print_formatted

@pytest.mark.asyncio
async def test_flattening_lists():
    data = ["foo\nbar", "cork", "qux\nbarf ploxx\n", "baz"]
    stream = Stream.from_iterable(data, max_parallel=4)
    result = await stream.flatmap(lambda s: s.split()).to_list()
    print('result:', result)
    assert result == ['foo', 'bar', 'cork', 'qux', 'barf', 'ploxx', 'baz']

@pytest.mark.asyncio
async def test_flattening_strings():
    data = ["a", "flatmap"]
    stream = Stream.from_iterable(data, max_parallel=4)
    result = await stream.flatmap(lambda s: s).to_list()
    print('result:', result)
    assert result == ['a', 'f', 'l', 'a', 't', 'm', 'a', 'p']

@pytest.mark.asyncio
async def test_empty_iterables():
    data = [1, 2, 3, 4]
    stream = Stream.from_iterable(data, max_parallel=4)
    result = await stream.flatmap(lambda x: []).to_list()
    print('result:', result)
    assert result == []

@pytest.mark.asyncio
async def test_flattening_non_iterables_errors():
    data = [1, 2, 3, 4]
    Stream.from_iterable(data).flatmap(lambda x: x)
    # find flatmap task and see if it errored as expected
    for task in asyncio.all_tasks():
        if task.get_name() == 'flatmap-consumer':
            with pytest.raises(TypeError):
                await task

@pytest.mark.asyncio
async def test_flattening_lists_with_coroutine():
    async def split(string: str):
        return string.split()
    data = ["foo\nbar", "cork", "qux\nbarf ploxx\n", "baz"]
    stream = Stream.from_iterable(data, max_parallel=1)
    result = await stream.flatmap(split).to_list()
    assert result == ['foo', 'bar', 'cork', 'qux', 'barf', 'ploxx', 'baz']
