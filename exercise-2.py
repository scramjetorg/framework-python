from scramjet.streams import DataStream
import asyncio

sample_words = [
    'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur',
    'adipiscing', 'elit,', 'sed', 'do', 'eiusmod', 'tempor',
    'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna',
    'aliqua.', 'Ut', 'enim', 'ad', 'minim', 'veniam,'
]


# 1) Wypisz długości słów z listy sample_words.
async def word_lengths():
    await DataStream.read_from(sample_words).print()

asyncio.run(word_lengths())


# 2) Wypisz ciąg kwadratów liczb parzystych od 0 do 29.
#    Oczekiwany wynik: 0 4 16 36 64 100 144 196 256 324 484 576 676 784
async def even_squares():
    pass

asyncio.run(even_squares())


# 3) W pliku fruits.csv znajdź słodkie owoce i wypisz ich nazwy.
#    Oczekiwany wynik: 'orange' 'strawberry' 'banana'
async def process_csv():
    pass

asyncio.run(process_csv())
