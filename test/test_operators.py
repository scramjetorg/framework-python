from scramjet.streams import DataStream
import asyncio
from scramjet.ansi_color_codes import *
from scramjet.utils import LogWithTimer
import pytest

log = LogWithTimer.log

# transformations

async def async_is_even(x):
    await asyncio.sleep((x%5)/10)
    return x % 2 == 0

async def async_square(x):
    await asyncio.sleep((x%5)/10)
    return x**2

async def echo(x):
    log(f"{yellow}Processing:{reset} {repr(x)}")
    return x


# test cases

@pytest.mark.asyncio
async def test_redir_operator():
    result = []
    # parens necessary because of precedence...
    await (DataStream.from_iterable(range(8)) > result)
    print(result)
    assert result == [0, 1, 2, 3, 4, 5, 6, 7]

@pytest.mark.asyncio
async def test_map_operator():
    s = DataStream.from_iterable(range(8)) | async_square
    result = await s.to_list()
    print(result)
    assert result == [0, 1, 4, 9, 16, 25, 36, 49]

@pytest.mark.asyncio
async def test_map_operator_with_lambda():
    s = DataStream.from_iterable(range(8)) | (lambda x: x**2)
    result = await s.to_list()
    print(result)
    assert result == [0, 1, 4, 9, 16, 25, 36, 49]

@pytest.mark.asyncio
async def test_filter_operator():
    s = DataStream.from_iterable(range(8)) % async_is_even
    result = await s.to_list()
    print(result)
    assert result == [0, 2, 4, 6]

@pytest.mark.asyncio
async def test_chaining_maps():
    s = DataStream.from_iterable(range(8)) | (lambda x: x+1) | (lambda x: x*2) | (lambda x: str(x))
    result = await s.to_list()
    print(result)
    assert result == ['2', '4', '6', '8', '10', '12', '14', '16']

@pytest.mark.asyncio
async def test_operator_chaining():
    s = DataStream.from_iterable(range(12)) % async_is_even | async_square
    result = await s.to_list()
    print(result)
    assert result == [0, 4, 16, 36, 64, 100]

@pytest.mark.asyncio
async def test_operator_chaining_other_way():
    # parens necessary because of precedence...
    s = (DataStream.from_iterable(range(12)) | async_square ) % async_is_even
    result = await s.to_list()
    print(result)
    assert result == [0, 4, 16, 36, 64, 100]

@pytest.mark.asyncio
async def test_combining_map_with_sink():
    result = await (DataStream.from_iterable(range(8)) | (lambda x: x+2) > [])
    print(result)
    assert result == [2, 3, 4, 5, 6, 7, 8, 9]

