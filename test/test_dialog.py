import unittest
import os
import sys

sys.path.append(os.path.abspath('../src'))

from common_utils import get_config_without_default
from dialog import AddTemplate


class TestDialog(unittest.TestCase):

    def test_add_template(self):
        tdata = [{'name': 'zhangsan', 'age': 18}]
        theader = {'name': '姓名', 'age': '年龄'}
        AddTemplate(title='test add template', tree_data=tdata, tree_header=theader).mainloop()

    def test_add_catalog_temlate(self):
        _conf = get_config_without_default()
        _tree_data = []
        for _sect_name in _conf.sections():
            if _sect_name.startswith('catalog_style.'):
                dic = dict(_conf.items(_sect_name))
                dic.setdefault('name', _sect_name.replace('catalog_style.', ''))
                _tree_data.append(dic)
        _tree_header = {
            'name': '目录模板名称',
            'size': '目录图纸大小',
            'table_block_name': '表格图块名称',
            'cell_block_name': '单元格图块名称'
        }
        AddTemplate(title='添加图纸目录模板', tree_data=_tree_data, tree_header=_tree_header).mainloop()


if __name__ == '__main__':
    print('test dialog')
    # unittest.main()
    TestDialog().test_add_catalog_temlate()
