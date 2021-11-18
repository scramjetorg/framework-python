from multiprocessing import Process
import time

yellow="\033[33m"
strong="\033[97;1m"
reset="\033[0m"

def header(text):
    print(f'\n{strong}{text}{reset}')

class WriteInIntervals():
    def __init__(self, path, data, delay=0.01):
        self.path, self.data, self.delay = path, data, delay
        self.writer = Process(target=self.write)

    def __enter__(self):
        self.writer.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.writer.join()

    def write(self):
        with open(self.path, 'w') as pipe:
            for chunk in self.data:
                time.sleep(self.delay)
                print(f'{yellow}Write into pipe{reset}:', repr(chunk))
                pipe.write(chunk)
                pipe.flush()


def plain_loop(path, binary_mode=False):
    mode = 'rb' if binary_mode else 'r'
    with open(path, mode) as file:
        for item in file:
            print("Got:", repr(item))

def iterate_in_text_mode(path, *args):
    with open(path, 'r') as file:
        for item in iter(lambda: file.read(*args), ''):
            print("Got:", repr(item))

def iterate_in_binary_mode(path, *args):
    with open(path, 'rb') as file:
        for item in iter(lambda: file.read(*args), b''):
            print("Got:", repr(item))


data = ['f', 'oo', '\n', 'bar baz', ' ', 'bax\nqux']
multibyte_data = ['b', 'ą', 'c', 'z', 'e', 'k']
pipe_path = 'test_pipe'
regular_file = './sample_text_1.txt'


header("regular file - text mode, loop")
plain_loop(regular_file)

header("regular file - text mode, read(8)")
iterate_in_text_mode(regular_file, 8)

header("regular file - raw mode, read(8)")
with open(regular_file, 'rb', buffering=0) as file:
    for item in iter(lambda: file.read(8), b''):
        print("Got:", repr(item))

header("multibyte file - text mode, read(2)")
iterate_in_text_mode('multibyte.txt', 2)

header("multibyte file - bin mode, read(2)")
iterate_in_binary_mode('multibyte.txt', 2)

header("pipe - text mode, loop")
with WriteInIntervals(pipe_path, data):
    plain_loop(pipe_path)

header("pipe - text mode, read()")
with WriteInIntervals(pipe_path, data):
    iterate_in_text_mode(pipe_path)

# header("pipe - raw mode")
# with WriteInIntervals(pipe_path, data):
#     with open(pipe_path, 'rb', buffering=0) as file:
#         for item in iter(lambda: file.read(8), b''):
#             print("Got:", repr(item))

header("pipe - text mode, but underlying buffer uses read1")
with WriteInIntervals(pipe_path, data):
    with open(pipe_path) as file:
        file.buffer.read = file.buffer.read1
        for item in iter(lambda: file.read(), ''):
            print("Got:", repr(item))
