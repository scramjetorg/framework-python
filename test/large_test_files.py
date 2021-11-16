import os
import random
from string import ascii_uppercase, ascii_lowercase, digits

# make space 10 times likely than other characters
charset = ascii_uppercase + digits + ascii_lowercase + ' '*10
# Should be noticeably larger than unix pipe buffer (64k) and TCP buffer (128k)
filesize = 1000000

def ensure_exists(path, charset):
    if not os.path.isfile(path) or os.path.getsize(path) != filesize:
        with open(path, 'w') as f:
            f.write(''.join(random.choice(charset) for _ in range(filesize)))
    return os.path.abspath(path)

path_to_text_without_newlines = ensure_exists('./sample_text_1', charset)
path_to_text_with_newlines = ensure_exists('./sample_text_2', charset + '\n')
