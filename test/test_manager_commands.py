import unittest
import unittest
from collections import defaultdict

import tkinter as tk
from src.manager_commands import Setting
from tkinter.ttk import Notebook, Frame, Button


class MyTestCase(unittest.TestCase):

    def test_modify_project_config(self):
        Setting('template').execute()

    def test_paned_window(self):
        pw = tk.PanedWindow(orient='vertical', showhandle=True, sashrelief='sunken')
        pw.pack(fill='both', expand=1)

        top = tk.Label(pw, text='top label', bg='red')
        bottom = tk.Label(pw, text='bottom label', bg='green')

        pw.add(top)
        pw.add(bottom)

        pw.mainloop()

    def test_notebook(self):
        nb = Notebook(padding=10)

        frm1 = Frame(nb)
        frm2 = Frame(nb)

        btn1 = Button(frm1, text='btn1')
        btn2 = Button(frm2, text='btn2')
        btn1.pack()
        btn2.pack()

        nb.add(frm1, text='frm1')
        nb.add(frm2, text='frm2')
        nb.pack(fill='both', expand=1)
        nb.mainloop()


if __name__ == '__main__':
    unittest.main()
