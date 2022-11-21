from __future__ import annotations

import os
import re
import sys

from win32com.universal import com_error

from lib.acad_typing.acadApplication import AcadApplication

sys.path.append(os.path.abspath('../lib'))

from lib.acad_typing.acadEnums import *
from functools import wraps
from typing import *
import win32com.client as win32
from win32com.client import VARIANT

import time
import logging

from common_utils import get_config


if TYPE_CHECKING:
    from lib.acad_typing.acadObjects import *
    from lib.acad_typing.acadApplication import *
    from lib.acad_typing.acadBlocks import *

_DELAY = 0.2  # seconds
_TIME = 10  # 重试次数

ORIGIN_POINT = VARIANT(5 | 8192, (0, 0, 0))


def point(x: float | Tuple[float, float, float], y: float = 0, z: float = 0):
    if type(x) is tuple:
        return VARIANT(5 | 8192, x)
    return VARIANT(5 | 8192, (x, y, z))


def _com_call_wrapper(f, *args, **kwargs):
    """
    COMWrapper support function. 
    Repeats calls when AttributeError, com_error exception occurs.
    """
    # Unwrap inputs
    args = [arg._wrapped_object if isinstance(arg, ComWrapper) else arg for arg in args]
    kwargs = dict([(key, value._wrapped_object) if isinstance(value, ComWrapper) else (key, value)
                   for key, value in dict(kwargs).items()])
    _retry = 0
    while True:
        try:
            result = f(*args, **kwargs)
        except (AttributeError, com_error) as e:
            t, v, trace = sys.exc_info()
            _retry += 1
            if _retry >= _TIME:
                raise
            if _retry == 1:
                logging.warning(f'{t} --> {v} --> retry...')
            time.sleep(_DELAY)
            continue
        break

    if isinstance(result, win32.CDispatch) or callable(result):
        return ComWrapper(result)
    return result


class ComWrapper(object):
    """
    Class to wrap COM objects to repeat calls when 'Call was rejected by callee.' exception occurs.
    """

    def __init__(self, wrapped_object):
        assert isinstance(wrapped_object, win32.CDispatch) or callable(wrapped_object)
        self.__dict__['_wrapped_object'] = wrapped_object

    def __getattr__(self, item):
        return _com_call_wrapper(self._wrapped_object.__getattr__, item)

    def __getitem__(self, item):
        return _com_call_wrapper(self._wrapped_object.__getitem__, item)

    def __setattr__(self, key, value):
        _com_call_wrapper(self._wrapped_object.__setattr__, key, value)

    def __setitem__(self, key, value):
        _com_call_wrapper(self._wrapped_object.__setitem__, key, value)

    def __call__(self, *args, **kwargs):
        return _com_call_wrapper(self._wrapped_object.__call__, *args, **kwargs)

    def __repr__(self):
        return 'ComWrapper<{}>'.format(repr(self._wrapped_object))


def com_call_wrapper(f):
    """COM对象方法装饰器"""

    @wraps(f)
    def _(*args, **kwargs):
        return _com_call_wrapper(f, *args, **kwargs)

    return _


@com_call_wrapper
def get_application(*, version=24, visible=True) -> AcadApplication:
    """
    获取应用实例 acadApplication 对象

    Args:
        visible (bool, optional): 控制可见性. Defaults to True.
        version (int, optional): cad 版本号. Defaults to 24.
            控制面板 -> 程序 可以查看版本号，例如 cad2020 版本号为 23.1.47.0, 此时 version = 23

    Returns:
        acadApplication: 应用实例
    """
    try:
        version = get_config().defaults().get('acad_version')
    except:
        ...

    __app = win32.Dispatch(f'AutoCAD.Application.{version}')
    __app.Visible = visible

    return __app


def get_color(*, color_index=7):
    version = "24"
    try:
        version = get_config().defaults().get('acad_version')
    except:
        ...
    color = get_application().GetInterfaceObject(f"AutoCAD.AcCmColor.{version}")
    color.ColorIndex = color_index


def open_file(app: AcadApplication, file: str) -> AcadDocument | None:
    """
    _summary_

    Args:
        app (AcadApplication): _description_
        file (str): _description_

    Raises:
        FileNotFoundError: _description_
        Exception: _description_

    Returns:
        AcadDocument | None: _description_
    """

    # 遍历查找 doc
    file = os.path.abspath(file)
    for doc in app.Documents:
        if file == os.path.abspath(doc.FullName) and not doc.ReadOnly:
            doc.Activate()
            return doc

    # 没有找到则打开文件
    try:
        return app.Documents.Open(file)
    except:
        raise


def get_block_ref_from_layout(ly: AcadLayout, block_ref_name: str) -> List[AcadBlockReference]:
    """
    从布局中选择指定的图块实例

    Args:
        ly (AcadLayout): 布局对象
        block_ref_name (str): 图块名称
    """
    res = []
    for obj in ly.Block:
        if obj.ObjectName == 'AcDbBlockReference' and obj.Name == block_ref_name:
            res.append(obj)

    return res  # type: ignore


def get_block_ref_from_doc(doc: AcadDocument, block_ref_name: str) -> List[AcadBlockReference]:
    """
    从文档中获取指定图块

    Args:
        doc (AcadDocument): 文档
        block_ref_name (str): 图块名

    Returns:
        List[AcadBlockReference]: 图块实例集合
    """
    res = []
    for ly in doc.Layouts:
        res.extend(get_block_ref_from_layout(ly, block_ref_name))
    return res


def del_block_ref_from_layout(ly: AcadLayout, block_ref_name: str):
    """
    从布局中删除指定图块

    Args:
        ly (AcadLayout): 布局对象   
        block_ref_name (str): 图块名称
    """
    for b in get_block_ref_from_layout(ly, block_ref_name):
        b.Delete()


def del_block_from_doc(doc: AcadDocument, block_name: str):
    """
    从文档中删除指定图块

    Args:
        doc (AcadDocument): 文档
        block_name (str): 图块名
    """
    for b in get_block_ref_from_doc(doc, block_name):
        b.Delete()
    doc.Blocks.Item(block_name).Delete()


def flatten_block_reference(doc: AcadDocument,
                            block_obj: AcadBlockReference) -> Sequence[AcadBlockReference]:
    """
    获取嵌套图块内部所有图块

    Args:
        doc (AcadApplication): 图块所在的 AcadDocument 文档
        block_obj (str): 最外层的图块对象

    Returns:
        Sequence['AcadBlock']: 所有图块组成的序列
    """

    if block_obj.ObjectName != 'AcDbBlockReference':
        return []
    else:
        res = [block_obj]
        i = 0
        # 遍历集合，获取块对象的嵌套块
        while i < len(res):
            # 从 cad 文档获取图块定义
            b = doc.Blocks.Item(res[i].Name)
            # 遍历图块内部的图形
            for j in range(b.Count):
                # 将内部图块添加的 res 集合
                if b.item(j).ObjectName == 'AcDbBlockReference':
                    res.append(b.item(j))
            i += 1
        return res


def get_bloct_attr_tags(doc: AcadDocument, block_name: str) -> List[str]:
    """
    获取指定图块的属性名称

    Args:
        doc (AcadDocument): 文档
        block_name (str): 图块名称

    Returns:
        List[str]: 属性名称数组
    """

    res = []
    block = doc.Blocks.Item(block_name)
    for itm in [block.Item(i) for i in range(block.Count)]:
        if itm.ObjectName == 'AcDbAttributeDefinition':
            res.append(itm.TagString)
    return res


def modify_block_attr(block: 'AcadBlockReference', kv_pair: Dict[str, str] = None):
    """
    修改图块内部属性值

    Args:
        block (AcadBlock): 被修改的属性块对象
        kv_pair (Dict[str, str]): 属性名称(忽略大小写) ：修改为指定值
            当 kv_pair 为 None 时，清空属性值
    """

    if block.HasAttributes:
        if kv_pair is None:
            for attr in block.GetAttributes():
                attr.TextString = ''
        else:
            KV = {}
            for k, v in kv_pair.items():
                KV[k.upper()] = v
            # 筛选出需要改名的属性
            attrs = [a for a in block.GetAttributes() if a.TagString.upper() in KV.keys()]
            # 遍历属性
            for attr in attrs:
                attr.TextString = KV.get(attr.TagString.upper())


def insert_block_to_layout(*,
                           doc: AcadDocuments,
                           layout_name: str,
                           block_name: str,
                           point: VARIANT = VARIANT(5 | 8192, (0, 0, 0)),
                           layer_name: str = None,
                           scale: Tuple = (1, 1, 1),
                           rotation=acPlotRotation.ac0degrees) -> AcadBlockReference | None:
    """
    向指定布局中插入块

    Args:
        doc: 被操作的文档
        point: 插入位置
        layout_name: 布局名称
        block_name: 被插入图块名或者全路径名
        layer_name: 插入到指定图层，默认为当前图层
        scale: 缩放比例 (x,y,z)
        rotation: 旋转角度

    Returns: 新插入的图块

    """
    ly = doc.Layouts.Item(layout_name)
    if ly:
        bi = ly.Block.InsertBlock(point, block_name, scale[0], scale[1], scale[2], rotation.value)
        if layer_name is not None:
            try:
                doc.Layers.Add(layer_name)
                bi.Layer = layer_name
            except Exception as e:
                print(e)
        return bi
    return None


def create_layout(doc: AcadDocument,
                  paper_name: str,
                  paper: str,
                  plot_style_name: str = 'monochrome.ctb'):
    """
    创建图纸布局

    Args:
        doc (AcadDocument): 操作所在文档
        paper_name (str): 设置图纸布局名称
        paper (str): 设置图纸尺寸名称
        plot_style_name (str, optional): 设置打印样式. Defaults to 'monochrome.ctb'.
    """

    ly = doc.Layouts.Add(paper_name)
    ly.RefreshPlotDeviceInfo()
    # 设置打印机
    ly.ConfigName = 'DWG To PDF.pc3'
    # 设置图纸大小
    pat = re.compile('[\s]+')
    ly.CanonicalMediaName = pat.sub('_', paper)
    # 设置单位和比例
    ly.PaperUnits = acPlotPaperUnits.acMillimeters.value
    ly.SetCustomScale(1, 1)
    # 设打印样式
    ly.StyleSheet = plot_style_name
    # 横向布局
    ly.PlotRotation = acPlotRotation.ac0degrees.value

    doc.Regen(acRegenType.acActiveViewport.value)  # 重生成
    return ly


def print_layout(doc: AcadDocument, layout_name: str, target_file: str, **kw) -> bool:
    """
    _summary_

    Args:
        doc (AcadDocument): _description_
        layout_name (str): _description_
        **kw: 打印设置
            plot_device: 打印机
            plot_style: 打印样式

    Returns:
        bool: _description_
    """
    path = os.path.split(target_file)[0]
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        ly = doc.Layouts.Item(layout_name)
        ly.Document.ActiveLayout = ly
        # 前台打印
        ly.Document.SetVariable("BACKGROUNDPLOT", 0)
        return doc.Plot.PlotToFile(target_file)
    except Exception as e:
        logging.warning(e)
        return False


def select_by_rectangle(doc: AcadDocument, mode: int | AcSelect = 0) -> AcadSelectionSet:
    p1 = doc.Utility.GetPoint()
    p2 = doc.Utility.GetCorner(point(p1), '指定对角点:')
    ss = doc.ActiveSelectionSet
    ss.Highlight(True)
    ss.Clear()
    ss.Select(mode, point(p1), point(p2))
    return ss


def _create_toolbar():
    """在 cad 中创建工具栏"""
    """
    app = get_application(version=24)

    mgs = app.MenuGroups
    mg = mgs.Item('天正快捷菜单')
    print(mg.Name)
    print(mg.MenuFileName)

    print('*' * 20)
    tbar = mg.Toolbars.Item(0)

    # tbar.Item(0).Delete
    # tbar.Item(0).Delete

    tbar.AddToolbarButton(0, 'TestItm3', 'this is a test button', 'Add\r')

    # itm = tbar.Item(0)
    # print(itm.Macro)
    # print(itm.Name)
    # print(itm.HelpString)

    """


if __name__ == '__main__':
    ...
    # app = get_application(version=24)
    # open_file(app, r'C:\Users\shun\Desktop\test\xref-CATALOG.dwg')
    # tk = r'C:\Users\shun\Desktop\test\xref-TK-A1.dwg'

    # insert_block_to_layout(doc, 'test_layout', tk, layer_name='000')
