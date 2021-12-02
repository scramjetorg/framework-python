from scramjet.streams import DataStream
import asyncio

sample_words = [
    'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur',
    'adipiscing', 'elit,', 'sed', 'do', 'eiusmod', 'tempor',
    'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna',
    'aliqua.', 'Ut', 'enim', 'ad', 'minim', 'veniam,'
]



# ---------------------------------------------------------

# Chcesz stworzyć strumień. W jaki sposób to robisz?

# 1) Utwórz strumień z listy sample_words.

# 2) Utworz strumień z ciągiem liczb wygenerowanym przez range(100).

# 3) Utwórz strumień z pliku test/sample_text_5.txt.






# Który sposób tworzenia strumienia jest najbardziej naturalny?
DataStream(sample_words)                # (a)
DataStream().some_method(sample_words)  # (b)
DataStream.some_method(sample_words)    # (c)

# ...a w przypadku gdy chcemy ustawić jakieś opcje?
DataStream(sample_words, concurrency=8)                      # (a)
DataStream(concurrency=8).some_method(sample_words)          # (b)
DataStream.some_method(sample_words, concurrency=8)          # (c)
DataStream.some_method(sample_words).options(concurrency=8)  # (d)



# Który sposób tworzenia strumienia z pliku jest najbardziej intuicyjny?
file_path = "blah"

DataStream.some_method(file_path)  # (a)

file = open(file_path)             # (b)
DataStream.some_method(file)

file = open(file_path)             # (c)
stream = DataStream()
for chunk in file:
    stream.some_method(chunk)



# ---------------------------------------------------------

# W jaki sposób zapisywał(a)byś dane ze strumienia?

# 4) Zapisz strumień z ciągiem liczb do listy.

# 5) Zapisz strumień słów z listy sample_words do pliku 'output.txt'.






# Który sposób zapisywania danych ze strumienia jest najbardziej intuicyjny?
target = open('somefile')

stream.some_method(target)               # (a)

DataStream.some_method(stream, target)   # (b)

for chunk in stream:                     # (c)
    target.write(chunk)



# co w przypadku innych obiektów niż plik?

async def tcp_streaming():
    reader, writer = await asyncio.open_connection('localhost', 8888)
    stream = DataStream.some_method(reader)
    # ...
    stream.another_method(writer)




# ---------------------------------------------------------

# Jak sądzisz, w jaki sposób plik będzie podzielony na chunki?

# Czego się spodziewasz przy czytaniu z pliku niepodzielonego na linie?
# A przy czytaniu z połączenia TCP?

# Jak byś wczytywał do strumienia plik w kawałkach po X znaków?



# ---------------------------------------------------------

# Co dzieje się ze streamem po zapisaniu?
# Czy można go dalej przetwarzać/zapisać gdzie indziej?
stream.map(...).filter(...).map(...).write_to(...)


# Co się powinno dziać po wywołaniu takiego kodu?
# Czy powinny się wykonać obliczenia? Jeśli tak, to gdzie są wyniki?
s = DataStream.read_from(sample_words).map(...).filter(...).map(...)



# ---------------------------------------------------------

# uruchamianie funkcji asynchronicznej
async def process():
    pass

asyncio.run(process())
