import collections
import configparser
import os
import os.path
from copy import deepcopy

from typing import *

_CONFIG: configparser.ConfigParser | None = None
_CONFIG_DOC: Dict[str, Dict[str, List]] = collections.defaultdict(dict)
"""
存放配置文件注释:
        key--section_name, value--option_dict
             option_dict: key--option_name, value--list of docs
section 的注释 key=section
"""

_CONF_FILE = '../conf/config.ini'


def _read_config_doc(file: str):
    global _CONFIG_DOC

    with open(file, encoding='utf-8') as f:
        _doc = []  # 保存注释
        _cur_sect = None  # 当前节
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            elif line.startswith((';', '#')):
                _doc.append(line)
            elif line.startswith('['):
                _cur_sect = line
                _CONFIG_DOC[line][line] = _doc
                _doc = []
            else:
                line = line.split('=')[0].strip()
                _CONFIG_DOC[_cur_sect][line] = _doc
                _doc = []
    return _CONFIG_DOC


def _write_config_doc(file: str):
    global _CONFIG_DOC
    _lines: List[str] = []
    with open(file, 'r', encoding='utf-8') as f:
        _doc = []  # 保存注释
        _cur_sect = None  # 当前节
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                _lines.append(os.linesep)
            elif line.startswith((';', '#')):
                _doc.append(line)
            else:
                if line.startswith('['):
                    _opt = line
                    _cur_sect = line
                else:
                    _opt = line.split('=')[0].strip()

                if _CONFIG_DOC.get(_cur_sect, None) is not None:
                    _ = _CONFIG_DOC.get(_cur_sect, None).get(_opt, None)
                    if _ is not None:
                        _lines.extend(_)

                if len(_doc) > 0:
                    _lines.extend(_doc)
                    _doc = []
                _lines.append(line)
    with open(file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(_lines))


def get_config():
    global _CONFIG
    """获取配置文件"""
    if _CONFIG is None:
        _CONFIG = configparser.ConfigParser(allow_no_value=True,
                                            interpolation=configparser.ExtendedInterpolation())
        _CONFIG.read(_CONF_FILE, encoding='utf-8')
        _read_config_doc(_CONF_FILE)  # 读取注释
    return _CONFIG


def get_config_without_default():
    """返回不包含 default 的配置文件副本"""
    conf = deepcopy(get_config())  # 辅助配置副本，删除默认项
    for k in list(conf.defaults().keys()):
        conf.remove_option('DEFAULT', k)
    return conf


def save_config():
    """保存对 config 的修改"""
    if _CONFIG is not None:
        with open(_CONF_FILE, 'w', encoding='utf-8') as f:
            _CONFIG.write(f)
        _write_config_doc(_CONF_FILE)  # 写入注释
