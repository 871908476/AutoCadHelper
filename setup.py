"""
安装及初始化程序
"""

import os
import pickle
import shutil

import sys

sys.path.append('./src')
from src.common_utils import get_config, save_config

def _create_ini():
    """创建配置文件"""
    conf_file = './conf/config.ini'
    if not os.path.exists('./conf/'):
        os.makedirs('./conf/')
    shutil.copy('./res/config.ini', conf_file)
    config = get_config()
    # 默认项
    config['DEFAULT'].update({
        'template_path': os.path.abspath('./template'),
        'temp_path': os.path.abspath('./temp'),
        'log_path': os.path.abspath('./log')
    })
    # 自动生成目录
    config['catalog'].update({'target_file': os.path.abspath('./catalog.dwg')})
    # 自动插入图框
    config['border'].update({'target_path': os.path.abspath('.')})

    save_config()


def _copy_template():
    """
    拷贝样式示例文件到模板文件

    Args:
        name (str): 样式名称， 读取 res 文件夹下的 {name}.dwg 文件
        type (Literal): 样式类型， 创建 template 文件夹下的 {type}_style.template 模板文件
    """
    for file, name, type in ((r'res\border_style_example.dwg', 'border_style_example',
                              'border_style'), (r'res\catalog_style_example.dwg',
                                                'catalog_style_example', 'catalog_style')):
        with open(file, 'rb') as f:
            tmp = {f'{name}': f.read()}
            with open(f'./template/{type}.template', 'wb') as fw:
                pickle.dump(tmp, fw)


def _create_lisp():
    """创建 lisp 文件"""
    ...


if __name__ == '__main__':
    print('start setup...')
    _create_ini()
    _copy_template()