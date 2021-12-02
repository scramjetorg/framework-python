from scramjet.streams import DataStream
import asyncio

sample_words = [
    'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur',
    'adipiscing', 'elit,', 'sed', 'do', 'eiusmod', 'tempor',
    'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna',
    'aliqua.', 'Ut', 'enim', 'ad', 'minim', 'veniam,'
]


fruits = '🥑🍌🍒🍇🥝🍋🥭🍊🍍🍅🍓🍉'
# 1) wygeneruj listę 20 owoców, wybierając losowo ze stringa fruits.
async def make_fruits():
    pass

asyncio.run(make_fruits())


# 2) Połącz wszystkie słowa z listy sample_words w jeden string.
async def join_words():
    pass

asyncio.run(join_words())


# 3) Zapisz słowa z listy sample_words do pliku po 5 w linijce.
async def word_sets():
    pass

asyncio.run(word_sets())
