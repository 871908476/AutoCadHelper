import json
import os.path
import pickle
import time
from collections import defaultdict
from dataclasses import dataclass, field, asdict

import yaml
from tkinter import filedialog, messagebox
from typing import *


@dataclass
class SystemConfig:
    temp_path: str = os.path.abspath('../temp')
    catalog_template_file: str = os.path.abspath('../template/border_style.template')
    border_template_file: str = os.path.abspath('../template/catalog_style.template')
    acad_version: int = 24


__CONFIG_DIR = '../conf/'
__SYS_CONFIG = None
__SYS_CONFIG_FILE = __CONFIG_DIR + 'config.yml'


def __get_config(path: str):
    """根据配置文件读取配置"""
    with open(path, 'r', encoding='utf-8') as rf:
        return yaml.load(rf, Loader=yaml.Loader)


def __save_config(path: str, conf: object):
    """保存配置文件"""
    with open(path, 'w', encoding='utf-8') as wf:
        yaml.dump(conf, wf, allow_unicode=True)


def set_default_sys_config():
    """默认系统设置"""
    global __SYS_CONFIG
    __SYS_CONFIG = SystemConfig()
    save_sys_config()


def _get_sys_config() -> SystemConfig:
    """获取系统配置"""
    global __SYS_CONFIG
    if not __SYS_CONFIG:
        if not os.path.exists(__SYS_CONFIG_FILE):
            set_default_sys_config()
        __SYS_CONFIG = __get_config(__SYS_CONFIG_FILE)
    return __SYS_CONFIG


def save_sys_config():
    """保存系统配置"""
    if __SYS_CONFIG:
        __save_config(__SYS_CONFIG_FILE, __SYS_CONFIG)


sys_config = _get_sys_config()
"""系统配置"""


@dataclass
class Plot:
    """打印设置"""
    plot_device: str = 'DWG To PDF.pc3'
    plot_style: str = 'monochrome.ctb'
    print_path: str = 'print'
    named_template: str = '<dwg_no>_<name>_<sub_project>.pdf'


@dataclass
class CatalogGenerator:
    """自动生成目录配置"""
    target_file: str = ''  # 生成目录保存的位置
    style: str = ''  # 目录模板样式名称
    suffix: str = ''  # 布局名称后缀
    prefix: str = ''  # 布局名称前缀
    update: bool = True  # 如果已存在布局将不进行修改
    close: bool = False  # 操作完成后是否关闭文件


@dataclass
class ProjectConfig:
    """项目配置"""
    name: str = ''  # 项目名称
    project_path: str = ''  # 项目文件目录
    excel_file: str = ''  # excel 配置文件路径
    plot: Plot = field(default=Plot())  # 打印设置
    catalog_generator: CatalogGenerator = field(default=CatalogGenerator())  # 自动生成目录配置


__PROJECT_CONFIG = defaultdict()


def get_all_project_config_names():
    return [_file.replace('.conf.yml', '') for _file in os.listdir(__CONFIG_DIR) if _file.endswith('.conf.yml')]


def get_project_config(name: str) -> ProjectConfig:
    """读取项目配置文件"""
    _res = __PROJECT_CONFIG.get(name, None)
    if not _res:
        _res = __get_config(f'{__CONFIG_DIR}{name}.conf.yml')
        __PROJECT_CONFIG.setdefault(name, _res)
    return _res


def save_project_config(conf: ProjectConfig):
    """保存项目配置文件"""
    name = conf.name
    if name not in __PROJECT_CONFIG:
        messagebox.showerror('error', f'没有找到项目 {name}, 点击新建项目。')
    else:
        __PROJECT_CONFIG[name] = conf
        __save_config(f'{__CONFIG_DIR}{name}.conf.yml', conf)


def create_project_config(conf: ProjectConfig):
    """新建项目配置"""
    name = conf.name
    if name in __PROJECT_CONFIG:
        messagebox.showerror('error', f'项目 {name} 已存在')
    else:
        __PROJECT_CONFIG.setdefault(name, conf)


@dataclass
class Template:
    name: str


@dataclass
class BorderStyle(Template):
    """图框样式"""
    size: str = 'A1'
    border_block_name: str = 'border'
    signature_block_name: str = 'signature'


@dataclass
class CatalogStyle(Template):
    """
    目录样式

        name: 模板名称

        size: str 打印图纸尺寸

        table_block_name: str   表格图块名称，默认为 'table'

        cell_block_name: str    单元格图块名称，默认为 'cell'
    """
    size: str = 'A1'
    table_block_name: str = 'table'
    cell_block_name: str = 'cell'


__TEMPLATE_CONFIG = {
    'catalog': defaultdict(),
    'border': defaultdict()
}
__TEMPLATE_CONFIG_FILE = {
    'catalog': __CONFIG_DIR + 'catalog_template.config.yml',
    'border': __CONFIG_DIR + 'border_template.config.yml',
}


def __get_template_config(_type: Literal['catalog', 'border'],
                          style_name: str = None):
    """
    获取模板配置
    @param _type: 模板类型
    @param style_name: 模板名称
    @return: 模板对象或集合
    """
    if not __TEMPLATE_CONFIG[_type] and os.path.exists(__TEMPLATE_CONFIG_FILE[_type]):
        _res: List[CatalogStyle | BorderStyle] = __get_config(__TEMPLATE_CONFIG_FILE[_type])
        if _res:
            for _ in _res:
                __TEMPLATE_CONFIG[_type].setdefault(_.name, _)

    if style_name is not None:
        if style_name not in __TEMPLATE_CONFIG[_type]:
            return None
        return __TEMPLATE_CONFIG[_type][style_name]
    else:
        return __TEMPLATE_CONFIG[_type].values()


def __modify_template_config(_type: Literal['catalog', 'border'], style_name: str, _opt: Dict):
    """添加或修改目录模板配置"""
    if not __get_template_config(_type, style_name):
        __TEMPLATE_CONFIG[_type][style_name] = CatalogStyle(style_name)
    _style: CatalogStyle = __TEMPLATE_CONFIG[_type][style_name]
    for k, v in filter(lambda _itm: hasattr(_style, _itm[0]), _opt.items()):
        setattr(_style, k, v)
    # 如果修改模板名，对应修改字典中的键名，使键名与模板名称一致
    if 'name' in _opt and style_name != _opt.get('name'):
        __TEMPLATE_CONFIG[_type][_opt['name']] = __TEMPLATE_CONFIG[_type][style_name]
        __TEMPLATE_CONFIG[_type].pop(style_name)


def __delete_template(_type: Literal['catalog', 'border'], name: str):
    __TEMPLATE_CONFIG[_type].pop(name)


def __save_template(_type: Literal['catalog', 'border']):
    """保存模板配置"""
    __save_config(__TEMPLATE_CONFIG_FILE[_type], list(__TEMPLATE_CONFIG[_type].values()))


def get_all_catalog_template_config() -> List[CatalogStyle]:
    """获取所有的目录模板配置"""
    return __get_template_config('catalog')


def get_catalog_template_config(name: str) -> CatalogStyle:
    return __get_template_config('catalog', name)


def modify_catalog_template_config(name: str, _opt: Dict = None):
    """添加或修改目录模板配置"""
    __modify_template_config('catalog', name, _opt)


def delete_catalog_template_config(name: str):
    """删除目录模板配置"""
    __delete_template('catalog', name)


def save_catalog_template_config():
    """保存目录模板配置"""
    __save_template('catalog')


__TEMPLATE: Dict[str, defaultdict] = None

__TEMPLATE_FILE: Dict[str, str] = None


def __init_template(fn):
    """初始化 .template 文件"""
    global __TEMPLATE, __TEMPLATE_FILE
    if __TEMPLATE is None:
        __TEMPLATE_FILE: Dict[str, str] = {
            'catalog': sys_config.catalog_template_file,
            'border': sys_config.border_template_file
        }
        __TEMPLATE = defaultdict()

        for _type in ('catalog', 'border'):
            with open(__TEMPLATE_FILE[_type], 'rb') as rf:
                __TEMPLATE[_type] = pickle.load(rf)

    def _(*args, **kwargs):
        fn(*args, **kwargs)

    return _


@__init_template
def get_template(_type: Literal['catalog', 'border'], name: str):
    return __TEMPLATE[_type].get(name)

@__init_template
def modify_template(_type: Literal['catalog', 'border'], name: str, opt: Dict):
    return __TEMPLATE[_type][name].update(opt)
