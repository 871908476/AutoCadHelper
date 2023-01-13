import tkinter
from tkinter import Variable
from unittest import TestCase


from src.config import ProjectConfig


class Test(TestCase):
    def test_convert_to_variable(self):
        # convert_to_variable(None,sys_config)
        # convert_to_variable(None,ProjectConfig())
        tk = tkinter.Tk()
        a = Variable(tk, ProjectConfig)
        print(type(a.get()))
        print(a.get())
        a.set(False)
        print(type(a.get()))
        print(a.get())
