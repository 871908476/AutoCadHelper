'''auto cad 工具命令集'''
from abc import abstractmethod
import collections
from copy import deepcopy
import logging
import os
import re
import sys

from lib.acad_typing.acadApplication import AcadApplication
from lib.acad_typing.acadDocuments import AcadDocument
from lib.acad_typing.acadEntities import AcadBlockReference
from lib.acad_typing.acadEnums import acRegenType


sys.path.append('./lib')

import pandas as pd

import common_utils
from dataclasses import dataclass
import acad_utils

from typing import Dict, List, Tuple, Literal
from acad_typing.acadApplication import *
from acad_typing.acadEnums import *
from acad_typing.acadBlocks import *
from acad_typing.acadObjects import *


class Command:
    ''' 
    抽象命令类 
    
    '''

    def __init__(self, **kwargs) -> None:
        pass

    @abstractmethod
    def execute(self):
        pass



@dataclass(frozen=True, kw_only=True)
class CatalogStyle:
    """ 目录样式 
    
    Args:
        template_name: str 模板文件路径
        paper: str 打印图纸尺寸
        table_block_name: str   表格图块名称，默认为 'table'
        cell_block_name: str    单元格图块名称，默认为 'cell'


    """
    template_file: str
    paper: str = 'A1'
    table_block_name: str = 'table'
    cell_block_name: str = 'cell'


@dataclass(frozen=True, kw_only=True)
class BorderStyle:
    """
    图框样式

    Args:
        template_file: str  模板文件路径
        size: str  图纸尺寸
    """
    template_file: str
    size: str
    border_block_name: str
    signature_block_name: str


class CreateCatalog(Command):

    def __init__(self,
                 *,
                 application: AcadApplication,
                 catalog_data: Dict[str, List[Dict]],
                 catalog_style: CatalogStyle,
                 target_file: str,
                 update=True,
                 close=True,
                 **kwargs) -> None:
        """
        创建目录

        Args:
            application (AcadApplication): cad 应用
            catalog_data (Dict[str, List[Dict]]): 目录数据 (子项名称--子项目录)
                    子项目录的数据结构：单元格字典组成的数组
            catalog_style (CatalogStyle): 目录样式名称
            target_file (str): 创建到指定文件
            update (bool, optional): 对目录进行更新而不是重新插入表格. Defaults to True.
            close (bool, optional): 插入目录后关闭. Defaults to True.
        """
        self.__app = application
        self.__catalog_style = catalog_style
        self.__data = catalog_data
        self.__target = target_file
        self.__update = update
        self.__close = close
        """保存到目标文件"""
        super().__init__(**kwargs)

    def execute(self):
        # 检查目标文件并获取文档对象
        if not os.path.exists(self.__target):
            doc = self.__app.Documents.Add(self.__target)
            doc.SaveAs(self.__target)
        else:
            doc = acad_utils.open_file(self.__app, self.__target)

        # 删除原目录并重新创建布局
        if not self.__update:
            for ly in doc.Layouts:
                if ly.Name in self.__data.keys():
                    ly.Delete()
            # 清理文档
            doc.PurgeAll()

        # 创建布局并插入目录模板
        ly_names = [ly.Name for ly in doc.Layouts]
        catalog_block = doc.ModelSpace.InsertBlock(acad_utils.ORIGIN_POINT,
                                                   self.__catalog_style.template_file, 1, 1, 1, 0)
        for ly_name in self.__data.keys():
            if ly_name in ly_names:
                continue
            ly = acad_utils.create_layout(doc, ly_name, self.__catalog_style.paper)  # 创建布局
            # 插入模板到布局
            b = ly.Block.InsertBlock(acad_utils.ORIGIN_POINT, catalog_block.Name, 1, 1, 1, 0)
            b.Explode()  # 炸开为单个图形

        # 删除模板图块
        acad_utils.del_block_from_doc(doc, catalog_block.Name)
        doc.Regen(acRegenType.acAllViewports.value)


        # 更新表格数据
        for _ly_name, cell_list in self.__data.items():
            ly_name = _ly_name.replace('建筑物', '目录')
            cells: List[AcadBlockReference] = []
            for lb in doc.Layouts.Item(ly_name).Block:
                if lb.ObjectName == 'AcDbBlockReference' and lb.Name == self.__catalog_style.cell_block_name:
                    cells.append(lb)
            # 单元格排序
            cells.sort(key=lambda _: _.InsertionPoint[0])
            mid = len(cells) // 2
            left = cells[:mid]
            left.sort(key=lambda _: _.InsertionPoint[1], reverse=True)
            right = cells[mid:]
            right.sort(key=lambda _: _.InsertionPoint[1], reverse=True)
            cells = left + right
            # 依次修改单元格
            print(cells)
            for k, c in enumerate(cells):
                if k < len(cell_list):
                    acad_utils.modify_block_attr(c, cell_list[k])
                else:
                    acad_utils.modify_block_attr(c, None)
        doc.Save()
        if self.__close:
            doc.Close()
        return super().execute()


class InsertBorder(Command):

    def __init__(self,
                 *,
                 application: AcadApplication,
                 data: List[Tuple[str, str, BorderStyle]],
                 close=True,
                 **kwargs) -> None:
        """
        插入图框

        Args:
            data (List[Tuple]): 数据
                Tuple 数据结构:
                     -- file (str): 操作的cad文件
                     -- layout (str): 布局名称
                     -- border_style (BorderStyle): 图框样式
            close (bool): 插入图框后是否关闭文件
        """
        self._app = application
        self.__data = data
        self._close = close
        super().__init__(**kwargs)

    def execute(self):
        tmp = collections.defaultdict(list)
        # 按文件分类
        for (f, ly_name, border_style) in self.__data:
            tmp[f].append((ly_name, border_style))
        # 遍历文件
        for f, arr in tmp.items():
            try:
                doc = acad_utils.open_file(self._app, f)
                for ly_name, border_style in arr:
                    ly = doc.Layouts.Item(ly_name)
                    _, _n = os.path.split(border_style.template_file)
                    name, _ = os.path.splitext(_n)
                    acad_utils.del_block_ref_from_layout(ly, name)
                    bi = ly.Block.InsertBlock(acad_utils.ORIGIN_POINT, border_style.template_file,
                                              1, 1, 1, 0)
                    bi.Layer = '0'
                if self._close:
                    doc.Save()
                    doc.Close()
            except Exception as e:
                logging.error(f'InsertBorder Error --> {f} --> {ly_name} --> {e.args}')
                raise

        return super().execute()


def _read_excel(excel_file: str,
                dtype=str,
                check_na: List[str] = None,
                how_drop='any',
                result_key='file') -> Dict[str, List[Dict]]:
    """
    读取 excel 配置文件
    首行作为 dict 的键，忽略大小写，全部转化为小写

    Args:
        excel_file (str): excel 路径
        dtype (_type_, optional): excel 单元格数据格式. Defaults to str.
        check_na (List[str], optional): 检查非空的列. Defaults to None.
        how_drop (str, optional): 删除空单元方式. Defaults to 'any'.
        result_key (str, optional): 作为返回字典的键的 excel 表头. Defaults to 'file'.        

    Returns:
        Dict[str, List[Dict]]: 
            键 --> 文件名
            值 --> 每一行数据形成的 Dict, 并新增 sub_project = sheet_name 项
    """
    # 读取图签信息
    _: Dict[str, pd.DataFrame] = pd.read_excel(excel_file, sheet_name=None, dtype=dtype)
    # 按文件分类
    # 文件路径作为键，该文件对应的图纸列表作为值
    file_infos_dict: Dict[str, List[Dict]] = collections.defaultdict(list)
    check_na.append(result_key)
    for sub_name, df in _.items():
        df.dropna(subset=check_na, how=how_drop, inplace=True)
        df.columns = [col.lower() for col in df.columns]  # 列名转为小写
        for info in df.to_dict(orient='index').values():
            info['sub_project'] = sub_name  # 添加子项名称
            file_infos_dict[info.get(result_key)].append(info)
    return file_infos_dict


class FreezeLayer(Command):
    """冻结图层"""

    def __init__(self,
                 document: AcadDocument,
                 *,
                 name_pattern: str = None,
                 name_ex_pattern: str = None,
                 unfreeze=False,
                 **kwargs) -> None:
        """
        冻结图层

        注意：
            图层名匹配方式为 fullmatch
            * 为通配符
            多个图层名称使用 | 分隔

        Args:
            document (AcadDocument): 需要操作的文档
            name_pattern (str, optional): 需要冻结的图层名称. Defaults to None.
            name_ex_pattern (str, optional): 不需要冻结的图层名称. Defaults to None.
            unfreeze (bool, optional): 未指定为冻结的图层是否全部取消冻结. Defaults to False.
        """
        super().__init__(**kwargs)
        self.doc = document
        self.unfreeze = unfreeze
        self.pattern = re.compile(name_pattern.replace('*', '.*'),
                                  re.IGNORECASE) if name_pattern is not None else None
        self.ex_pattern = re.compile(name_ex_pattern.replace('*', '.*'),
                                     re.IGNORECASE) if name_ex_pattern is not None else None

    def execute(self):
        for ly in self.doc.Layers:
            name = ly.Name
            if self.pattern is not None and self.pattern.fullmatch(name) and (
                    self.ex_pattern is None or not self.pattern.fullmatch(name)):
                ly.Freeze = True
            elif self.unfreeze and ly.Freeze:
                ly.Freeze = False


class ModifyLayerLineweight(Command):
    """修改图层线宽"""

    def __init__(self,
                 document: AcadDocument,
                 *,
                 default=True,
                 heavy_pattern='wall|column',
                 middle_pattern='window|door_fire|roof|curtwall',
                 thin_pattern='*',
                 heavy_ex_pattern=None,
                 middle_ex_pattern='pub_hatch',
                 heavy=30,
                 middle=15,
                 thin=5,
                 **kwargs) -> None:
        """
        修改图层显宽

        注意：
            图层名匹配方式为 fullmatch
            * 为通配符
            多个图层名称使用 | 分隔

        Args:
            document (AcadDocument): 需要修改的文档
            default (True): 是否将所有图层设置为默认线宽
            heavy_pattern (str, optional): 修改为粗线的图层名. Defaults to 'wall|column'.
            middle_pattern (str, optional): 修改为中粗线的图层名. Defaults to 'window|door_fire|stair|dim*|pub*'.
            thin_pattern (str, optional): 修改为细线的图层名. Defaults to '*'.
            heavy_ex_pattern (_type_, optional): 不修改为粗线的图层名. Defaults to None.
            middle_ex_pattern (str, optional): 不修改为中粗线的图层名. Defaults to 'pub_hatch'.
            heavy (int, optional): 粗线. Defaults to 0.30.
            middle (int, optional): 中粗线. Defaults to 0.15.
            thin (int, optional): 西线. Defaults to 0.05.
        """

        self.default = default

        self.heavy_pattern = re.compile(heavy_pattern.replace('*', '.*'),
                                        re.IGNORECASE) if heavy_pattern is not None else None
        self.middle_pattern = re.compile(middle_pattern.replace('*', '.*'),
                                         re.IGNORECASE) if middle_pattern is not None else None
        self.thin_pattern = re.compile(thin_pattern.replace('*', '.*'),
                                       re.IGNORECASE) if thin_pattern is not None else None
        self.heavy_ex_pattern = re.compile(heavy_ex_pattern.replace('*', '.*'),
                                           re.IGNORECASE) if heavy_ex_pattern is not None else None
        self.middle_ex_pattern = re.compile(middle_ex_pattern.replace(
            '*', '.*'), re.IGNORECASE) if middle_ex_pattern is not None else None

        self.heavy = heavy
        self.middle = middle
        self.thin = thin

        self.layers = {}
        for idx in range(0, document.Layers.Count):
            ly: AcadLayer = document.Layers.Item(idx)
            self.layers[ly.Name] = ly
        super().__init__(**kwargs)

    def execute(self):
        for name, ly in self.layers.items():
            ly_n = name.split('|')[-1]
            if self.heavy_pattern and self.heavy_pattern.fullmatch(ly_n) and (
                    self.heavy_ex_pattern is None or not self.heavy_ex_pattern.fullmatch(ly_n)):
                ly.Lineweight = self.heavy
            elif self.middle_pattern and self.middle_pattern.fullmatch(ly_n) and (
                    self.middle_ex_pattern is None or not self.middle_ex_pattern.fullmatch(ly_n)):
                ly.Lineweight = self.middle
            elif self.thin_pattern and self.thin_pattern.fullmatch(ly_n):
                ly.Lineweight = self.thin
            elif self.default:
                ly.Lineweight = -3


class ModifyLayerAttr(Command):

    def __init__(self, *, document: AcadDocument,
                 name_attrs_dicts: Dict[str, List[Tuple[str, ...]]], **kwargs) -> None:
        self.name_attrs = name_attrs_dicts
        self.layers = {}
        for idx in range(0, document.Layers.Count):
            ly: AcadLayer = document.Layers.Item(idx)
            self.layers[ly.Name] = ly
        super().__init__(**kwargs)

    def _run(self, layer_name):
        ly = self.layers.get(layer_name)
        if ly:
            for (attr_name, *args) in self.name_attrs.get(layer_name):
                if hasattr(ly, attr_name):
                    attr = getattr(ly, attr_name)
                    if callable(attr):
                        attr(*args)
                    elif len(args) > 0:
                        setattr(ly, attr_name, args[0])

    def execute(self):
        for name in self.name_attrs.keys():
            try:
                if name.find('*') > -1:
                    for ly_n in self.layers.keys():
                        if re.compile(name.replace('*', '.*'), re.IGNORECASE).match(ly_n):
                            self._run(ly_n)
                else:
                    self._run(ly_n)
            except:
                ...

        return super().execute()
class InsertSignatureAndPlot(Command):
    """插入图签并打印"""

    def __init__(self, *, signature_file, **kwargs) -> None:
        # 获取参数
        _ver = common_utils.get_config()['DEFAULT'].getint('acad_version', 23)
        self.__app = acad_utils.get_application(version=_ver)
        self.__sign = signature_file

    def execute(self):
        doc = self.__app.ActiveDocument
        ly = doc.Layouts.Item('F09门窗表')


class ModifySignatureAndPlot(Command):
    """修改图签信息并打印"""

    def __init__(self, *, plot=True, close=True, **kwargs) -> None:
        """
        修改图签信息并打印

        Args:
            plot (bool, optional): 修改信息同时打印图纸. Defaults to True.
            close (bool, optional): 修改完成后关闭文档. Defaults to True.
         """
        # 获取参数
        _ver = common_utils.get_config()['DEFAULT'].getint('acad_version', 23)
        self.__app = acad_utils.get_application(version=_ver)

        self.__plot = plot
        self.__close = close

        # 项目配置
        _sect = common_utils.modify_project_config()
        self.__project_path = _sect.get('project_path')
        self.__excel_file = _sect.get('excel_file')

        # 图签属性与 excel 表头映射关系
        self.__attr_map: Dict[str, str] | None = None

        # 获取打印配置
        if self.__plot:
            _sect = common_utils.modify_plot_config()
            self.__named_template = _sect.get('named_template')
            self.__print_path = _sect.get('print_path')

    def execute(self):
        # 获取 excel 数据
        _data = _read_excel(self.__excel_file, check_na=['file', 'layout'])
        # 遍历文件修改打印
        for file, info_list in _data.items():
            # 根据图块模板添加图签图块名
            for info in info_list:
                info['block_name'] = common_utils.get_config(
                )[f'border_style.{info["border_style"]}'].get('signature_block_name', 'signature')
            # 如果 file 不是文件则添加项目路径为根路径
            if self.__project_path is not None and not os.path.isfile(file):
                file = os.path.join(self.__project_path, file)
            # 文件类型检查
            if os.path.exists(file) and not file.endswith('.dwg'):
                logging.warning(f'{file} 不是 .dwg 文件')
                continue
            # 打开文件，遍历图签信息
            doc = acad_utils.open_file(self.__app, os.path.abspath(file))
            for info in info_list:
                if self.__attr_map is None:
                    self.__attr_map = common_utils.make_dwg_excel_attr_map(
                        acad_utils.get_bloct_attr_tags(doc, info['block_name']), list(info.keys()))

                layout_name: str = info.get('layout', None)
                if layout_name is None: continue
                logging.info(f'正在修改 {file} 文件的 {layout_name} 布局')
                try:
                    ly = doc.Layouts.Item(layout_name)
                    for b in acad_utils.get_block_ref_from_layout(ly, info['block_name']):
                        dic = deepcopy(self.__attr_map)
                        for k, v in self.__attr_map.items():
                            dic[k] = info.get(v)
                        acad_utils.modify_block_attr(b)
                        acad_utils.modify_block_attr(b, dic)
                    if self.__plot:
                        # 根据模板获取打印文件名, 默认为布局名
                        print_file: str = self.__named_template
                        if print_file is None:
                            name, _ = os.path.splitext(os.path.basename(file))[0]
                            print_file = name + '_' + layout_name + '.pdf'
                        else:
                            for k, v in info.items():
                                print_file = print_file.replace(f'<{k}>', v)
                        print_file = os.path.join(self.__print_path, print_file)
                        if not acad_utils.print_layout(doc, layout_name, print_file):
                            logging.warning(f'{file} 文件的 {layout_name} 布局打印失败')
                except Exception as e:
                    logging.warning(e)

            if self.__close:
                doc.Close(True)


class AddCatalogTemplate(Command):
    """添加目录模板"""
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._frm = common_utils.AddTemplate(style_type='catalog_style')

    def execute(self):
        self._frm.mainloop()

if __name__ == '__main__':
    print('*' * 20)
    # app = acad_utils.get_application()
    # # doc = acad_utils.get_application().ActiveDocument
    # for f in askopenfiles(filetypes=[('Autocad 文件', '*.dwg')]):
    #     doc = acad_utils.open_file(app, f.name)
    #     ModifyLayerLineweight(doc,
    #                           heavy_pattern='*a-wall*|*wall|*col*',
    #                           heavy_ex_pattern='*wall*隔墙|*elve*wall',
    #                           middle_pattern='*wind*|*roof',
    #                           middle_ex_pattern='*wind*(text|编号|open)').execute()
    #     # doc.Save()
    #     print(doc.ReadOnly)
    #
    #     break

    # FreezeLayer(doc, name_pattern='*window_text|door_*text', unfreeze=True).execute()

    # color = acad_utils.get_application().GetInterfaceObject("AutoCAD.AcCmColor.24")
    # print(app.GetInterfaceObject("AutoCAD.AcLineWeight.24")._wrapped_object)
    # print(color._wrapped_object.SetRGB)
    # ModifySignatureAndPlot(plot=True, close=True).execute()
    ModifySignatureAndPlot().execute()
