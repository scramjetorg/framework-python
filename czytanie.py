from multiprocessing import Process
import time
from ansi_color_codes import *

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
            for chunk in data:
                time.sleep(self.delay)
                print(f'{yellow}Write into pipe{reset}:', repr(chunk))
                pipe.write(chunk)
                pipe.flush()



data = ['f', 'oo', '\n', 'bar baz', ' ', 'bax\nqux']
pipe_path = 'test_pipe'
regular_file = './sample_text_1.txt'

print("\nregular file - text mode")
with open(regular_file) as file:
    for item in file:
        print("Got:", repr(item))

print("\nregular file - raw mode")
with open(regular_file, 'rb', buffering=0) as file:
    for item in iter(lambda: file.read(8), b''):
        print("Got:", repr(item))

# print("\npipe - text mode")
# with WriteInIntervals(pipe_path, data):
#     with open(pipe_path) as file:
#         for item in file:
#             print("Got:", repr(item))

# print("\npipe - raw mode")
# with WriteInIntervals(pipe_path, data):
#     with open(pipe_path, 'rb', buffering=0) as file:
#         for item in iter(lambda: file.read(8), b''):
#             print("Got:", repr(item))
