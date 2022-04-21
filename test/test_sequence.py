from scramjet.streams import Stream
import scramjet.utils as utils
from scramjet.ansi_color_codes import *
import pytest

log = utils.LogWithTimer.log
fmt = utils.print_formatted

@pytest.mark.asyncio
async def test_sequencing_text_into_lines():
    data = ["foo\nbar", " ", "b", "az", "\nqux\n", "plox"]
    result = await (
        Stream
            .from_iterable(data, max_parallel=2)
            .sequence(lambda part, chunk: (part+chunk).split('\n'), "")
            .to_list()
    )
    print(result)
    assert result == ['foo', 'bar baz', 'qux', 'plox']

# I know, this could be done using flatmap+batch
@pytest.mark.asyncio
async def test_sequencing_lists_into_batches():
    data = [[1, 2, 3], [4, 5], [6, 7, 8, 9, 10]]
    def split_into_pairs(part, li):
        new_list = part + li
        every_2nd_index = range(0, len(new_list), 2)
        return [new_list[i:i+2] for i in every_2nd_index]
    result = await (
        Stream
            .from_iterable(data, max_parallel=2)
            .sequence(split_into_pairs, [])
            .to_list()
    )
    print(result)
    assert result == [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]


@pytest.mark.asyncio
async def test_sequencing_text_into_lines_with_coroutine_sequencer():
    data = ["foo\nbar", " ", "b", "az", "\nqux\n", "plox"]
    async def sequencer(part, chunk):
        return (part+chunk).split('\n')
    result = await (
        Stream
            .from_iterable(data, max_parallel=2)
            .sequence(sequencer, "")
            .to_list()
    )
    print(result)
    assert result == ['foo', 'bar baz', 'qux', 'plox']
