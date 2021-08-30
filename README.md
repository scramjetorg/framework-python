IFCA implementation in Python
=============================

Environment setup
-----------------

_Tested with Python 3.8.10 and Ubuntu 20.04._

Check Python version:

    $ python3 --version
    Python 3.8.10


Usage
-----

Run test cases:

    python3 test-cases.py

Run with debug output and 10x faster:

    PYFCA_DEBUG=1 python3 test-cases.py 0.1


Proof of correctness
--------------------

`pts.py` demonstrates the correctness of the algorithm.

The input sequence for the test is a list of dictionaries, each containing an
`id` key which matches the order of the item in the sequence.

The transformation consists of two functions:
- the first one returns immediately for inputs with even `id` but has a delay
  for inputs with odd `id`,
- the second one is synchronous and returns immediately.

The soft limit for number of items processed in parallel is 4.

To perform the test, run:

    PYFCA_DEBUG=1 python3 pts.py

The following happens:

1. Six items are written.
1. First 3 writes resolve immediately, because processing queue is initially
   empty.
1. Next 3 writes return a pending Future object, which get resolved as previous
   items are processed.
1. First transformation is performed on the items in the order matching their
   `id`s.
1. Second transformation is performed as soon as items become available. This
   means that it's performed on the elements with even `id`s first, because
   they are ready for processing earlier than the elements with odd `id`s.
1. However, the ordering of the results matches the input order.
