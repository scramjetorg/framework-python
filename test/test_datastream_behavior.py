from datastream import DataStream
import asyncio
import pytest

@pytest.mark.asyncio
async def test_stream_is_iterable():
    stream = DataStream.from_iterable([1, 2, 3, 4])
    async for chunk in stream:
        print(chunk)

nums = [1, 5, 3, 2, 4, 2]

@pytest.mark.asyncio
async def test_stream_can_read_from_a_stream():
    stream1 = DataStream.from_iterable(nums, max_parallel=4)
    stream2 = DataStream.from_iterable(stream1, name='stream2')
    results = await stream2.to_list()
    print('result:', results)

