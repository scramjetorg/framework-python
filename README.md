Scramjet in Python
==================

<p align="center">
    <a><img src="https://img.shields.io/github/license/scramjetorg/framework-python?color=green&style=plastic" alt="GitHub license" /></a>
    <a><img src="https://img.shields.io/github/v/tag/scramjetorg/framework-python?label=version&color=blue&style=plastic" alt="version" /></a>
    <a><img src="https://img.shields.io/github/stars/scramjetorg/framework-python?color=pink&style=plastic" alt="GitHub stars" /></a>
    <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=7F7V65C43EBMW">
        <img src="https://img.shields.io/badge/Donate-PayPal-green.svg?color=yellow&style=plastic" alt="Donate" />
    </a>
</p>
<p align="center">⭐ Star us on GitHub — it motivates us a lot! 🚀 </p>
<p align="center">
    <img src="https://assets.scramjet.org/images/framework-logo-256.svg" width="420" alt="Scramjet Framework">
</p>

Scramjet is a simple reactive stream programming framework. The code is written
by chaining functions that transform the streamed data, including well known
map, filter and reduce.

The main advantage of Scramjet is running asynchronous operations on your data
streams concurrently. It allows you to perform the transformations both
synchronously and asynchronously by using the same API - so now you can "map"
your stream from whatever source and call any number of API's consecutively.

[Originally written](https://github.com/scramjetorg/scramjet) on top of node.js
object streams, Scramjet is now being ported into Python. This is what is
happening in this repository.

>_Tested with Python 3.8.10 and Ubuntu 20.04._
## Table of contents

- [Installation](#installation)
- [Quick start](#quick-start)
- [Usage](#usage)
- [Requesting features](#requesting-features)
- [Reporting bugs](#reporting-bugs)
- [Contributing](#contributing)
- [Development Setup](#development-setup)

## Installation

Scramjet Framework is available on PyPI, You can install it with simple pip command:

```bash
pip install scramjet-framework-py
```
## Quick start

Let's say we have a `fruits.csv` file like this:

```csv
orange,sweet,1
lemon,sour,2
pigface,salty,5
banana,sweet,3
cranberries,bitter,6
```

and we want to write the names of the sweet fruits to a separate file.
To do this, write an async function like this:


```python

from scramjet import streams
import asyncio


async def sweet_stream():
    with open("fruits.csv") as file_in, open("sweet.txt", "w") as file_out:
        await (
            streams.Stream
            .read_from(file_in)
            .map(lambda line: line.split(','))
            .filter(lambda record: record[1] == "sweet")
            .map(lambda record: f"{record[0]}\n")
            .write_to(file_out)
        )

asyncio.run(sweet_stream())
```

output saved in sweet.txt:

```
orange
banana
```

and that's it!

## Usage

Basic building block of Scramjet is the `Stream` class. It reads input in
chunks, performs operations on these chunks and produces an iterable output
that can be collected and written somewhere.

**Creating a stream** is done using `read_from` class method. It accepts
any iterable or an object implementing .read() method as the input, and returns
a `Stream` instance.

**Transforming a stream:**

* `map` - transform each chunk in a stream using specified function.
* `filter` - keep only chunks for which specified function evaluates to `True`.
* `flatmap` - run specified function on each chunk, and return all of its results as separate chunks.
* `batch` - convert a stream of chunks into a stream of lists of chunks.

Each of these methods return the modified stream, so they can be chained like
this: `some_stream.map(...).filter(...).batch(...)`

**Collecting data** from the stream (asynchronous):

* `write_to` - write all resulting stream chunks into a target.
* `to_list` - return a list with all stream chunks.
* `reduce` - combine all chunks using specified function.


Examples :books:
--------

You can find more examples in [`hello_datastream.py`](./hello_datastream.py)
file. They don't require any additional dependencies, just the standard library,
so you can run them simply with:

```bash
python hello_datastream.py
```

## Requesting Features

Anything missing? Or maybe there is something which would make using Scramjet Framework much easier or efficient? Don't hesitate to fill up a [new feature request](https://github.com/scramjetorg/framework-python/issues/new)! We really appreciate all feedback.

## Reporting bugs

If you have found a bug, inconsistent or confusing behavior please fill up a [new bug report](https://github.com/scramjetorg/framework-python/issues/new).

## Contributing

You can contribute to this project by giving us feedback ([reporting bugs](#reporting-bugs) and [requesting features](#reporting-features)) and also by writing code yourself!

The easiest way is to [create a fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) of this repository and then [create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) with all your changes. In most cases, you should branch from and target `main` branch.

Please refer to [Development Setup](#development-setup) section on how to setup this project.

## Development Setup

1. Install Python3 interpreter on your computer. Refer to [official docs](https://wiki.python.org/moin/BeginnersGuide/Download).

2. Install `git` version control system. Refer to [official docs](https://git-scm.com/downloads).

3. Clone this repository:

```bash
git clone git@github.com:scramjetorg/framework-python.git
```
4. Create and activate a virtualenv:

```bash
sudo apt install python3-virtualenv
virtualenv -p python3 venv
.venv/bin/activate
```

5. Check Python version:

```bash
$ python --version
Python 3.8.10
```

6. Install dependencies:

```bash
pip install -r dev-requirements.txt
```

7. Run test cases (with activated virtualenv):

```bash
pytest
```

> :bulb: **HINT:** add a filename if you want to limit which tests are run


8. If you want to enable detailed debug logging, set one of the following env variables:

```bash
PYFCA_DEBUG=1       # debug pyfca
DATASTREAM_DEBUG=1  # debug datastream
SCRAMJET_DEBUG=1    # debug both
```