from TestFile import *
from os import walk


def test_directory(path):
    filenames = next(walk(path), (None, None, []))[2]
    out = ''
    for f in filenames:
        #print(f)
        lang = f.split('.')[1]
        if lang == 'c' or lang == 'java' or lang == 'py':
            out2 = test_file(f)
            if out2 != '':
                out += "*File: " + f + '\n'
                out += out2

    return out
