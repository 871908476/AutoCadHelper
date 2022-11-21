import sys

sys.path.append('./lib')

from tkinter import messagebox

from acad_typing.acadEnums import *

if __name__ == '__main__':
    arr = []
    arr.append({'age': 10})
    arr.append({'age': 5})
    print(arr)
    arr.sort(key=lambda a: a['age'])
