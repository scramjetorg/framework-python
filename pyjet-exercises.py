from scramjet.streams import DataStream
import asyncio

sample_text = [
    'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing',
    'elit,', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore',
    'et', 'dolore', 'magna', 'aliqua.', 'Ut', 'enim', 'ad', 'minim', 'veniam,',
    'quis', 'nostrud', 'exercitation', 'ullamco', 'laboris', 'nisi', 'ut',
    'aliquip', 'ex', 'ea', 'commodo', 'consequat.'
]

# 1) Policz długości słów z listy sample_text
async def word_lengths(data):
    pass

asyncio.run(word_lengths(sample_text))


# 2) Wypisz ciąg kwadratów liczb od 0 do 100
async def squares(max=100):
    pass

asyncio.run(squares())


# 3) Wypisz ciąg kwadratów liczb parzystych od 0 do 100
async def even_squares(max=100):
    pass

asyncio.run(even_squares())


# 4) Otwórz plk sample_csv i znajdź wszystkie linie, w których
#    w 3. kolumnie jest wartość większa niż 100.
async def select_csv():
    pass

asyncio.run(select_csv())


# 5) Wybierz z sample_text słowa dłuższe niż 5 znaków i zapisz je do pliku.
async def words_to_file():
    pass

asyncio.run(words_to_file())


# 6) połącz wszystkie słowa z sample_text w jeden string i zapisz do pliku.
async def join_words():
    pass

asyncio.run(join_words())


fruits = {
    'a': '🥑', 'b': '🍌', 'c': '🍒', 'e': '🍆', 'g': '🍇', 'k': '🥝', 'l': '🍋',
    'm': '🥭', 'o': '🍊', 'p': '🍍', 't': '🍅', 's': '🍓', 'w': '🍉',
}
# 7) wygeneruj ciąg losowych liter, zamień je na owocki i zapisz do pliku.
async def make_fruits():
    pass

asyncio.run(make_fruits())


# 8) jak powyżej, ale zapisuj po 5 owocków w linijce.
async def make_sets_of_fruits():
    pass

asyncio.run(make_sets_of_fruits())


# 9) Policz długości słów z pliku test/sample_text_4.txt.
async def word_lengths_2():
    pass

asyncio.run(word_lengths_2())


# 10) wykonaj funkcję square_with_delay na lczbach od 0 do 20, po 4 naraz.
async def square_with_delay(x):
    print(f"Calculation start: {x}")
    await asyncio.sleep(1)
    print(f"Calculation end: {x} -> {x**2}")
    return x**2

async def concurrent_computing():
    pass

asyncio.run(concurrent_computing())


# 11) Przeczytaj plik test/sample_text_3.txt w kawałkach po 50 znaków,
#     a następnie przekształć strumień tak, żeby jego elementami były
#     zdania (kończące się kropką).
async def change_into_sentences():
    pass

asyncio.run(change_into_sentences())


# 12) Przeczytaj słowa z pliku test/sample_text_3.txt i dodaj na koniec
#     każdego wykrzyknik (zamieniając inne znaki interpunkcyjne). Zapisz
#     wynik do pliku.
async def exclamation_marks():
    pass

asyncio.run(exclamation_marks())


urls = [
    'https://en.wikipedia.org//wiki/Crustacean'
    'https://en.wikipedia.org//wiki/1991'
    'https://en.wikipedia.org//wiki/Wikipedia'
    'https://en.wikipedia.org//wiki/Seabird'
    'https://en.wikipedia.org//wiki/Main_Page'
    'https://en.wikipedia.org//wiki/Encyclopedia'
    'https://en.wikipedia.org//wiki/English_language'
    'https://en.wikipedia.org//wiki/COVID-19_pandemic'
    'https://en.wikipedia.org//wiki/Musical_theatre'
    'https://en.wikipedia.org//wiki/Elizabeth_I'
    'https://en.wikipedia.org//wiki/Elizabeth_II'
    'https://en.wikipedia.org//wiki/Baseball'
]
# 13) Ściągnij urle z listy, pobierając po 4 równolegle.
async def download():
    pass

asyncio.run(download())
