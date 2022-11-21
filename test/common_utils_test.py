import unittest
import os
import sys

sys.path.append(os.path.abspath('./src'))

import common_utils
# from common_utils import *


class TestAddTemplate(unittest.TestCase):

    def test_make_dwg_excel_attr_map(self):
        list1 = ['name', 'info', 'age']
        list2 = ['class', 'age', 'address']
        tmp = common_utils.make_dwg_excel_attr_map(list1, list2)
        # self.as
        print(tmp)


if __name__ == '__main__':
    unittest.main()
