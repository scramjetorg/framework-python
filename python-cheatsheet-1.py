# BASICS ----------------------------------------

# create an object of class Foo
f = Foo()

# writing asynchronous functions
async def foo():
    result = await bar()  # wait for result of another async function
    print(result)

# running asynchronous functions
import asyncio
asyncio.run(foo())


# FILES -----------------------------------------

path = 'test/sample_text_5.txt'

# reading from file (in text mode)
with open(path) as file:

    # read 20 characters
    data = file.read(20)
    print(data)

    # iterate over file contents:
    for line in file:
        print(line)

# writing to a file:
with open('another-file', 'w') as file:
    file.write("foo bar")



# MISC ------------------------------------------

# calculating length:
len("foo")   # -> 3
len([1, 2])  # -> 2

# splitting strings
"foo,bar,qux".split(',')  # -> ['foo', 'bar', 'qux']

# lambda functions:
foo = lambda x: "foo"+x
# is equivalent to:
def foo(x):
    return "foo"+x

# choosing a random item from an iterable
import random
random.choice('abcdefgh')  # -> 'c'
