import collections
import configparser
import functools
import os
import os.path
import pickle
import tkinter as tk
from copy import deepcopy
from logging import root
from tkinter import END, W, BooleanVar, StringVar, Tk, Variable, filedialog, messagebox, ttk
from typing import Callable, Dict, List, Literal, Tuple

_CONFIG: configparser.ConfigParser | None = None
_CONFIG_DOC: Dict[str, Dict[str, List]] = collections.defaultdict(dict)
"""
存放配置文件注释:
        key--section_name, value--option_dict
             option_dict: key--option_name, value--list of docs
section 的注释 key=section
"""


def logging_except(fn: Callable):
    """打印函数中的异常"""

    @functools.wraps(fn)
    def _(*args, **kw):
        return fn(*args, **kw)

    return _


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
        _file = '../conf/config.ini'
        _CONFIG = configparser.ConfigParser(allow_no_value=True,
                                            interpolation=configparser.ExtendedInterpolation())
        _CONFIG.read(_file, encoding='utf-8')
        _read_config_doc(_file)  # 读取注释
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
        file = '../conf/config.ini'
        with open(file, 'w', encoding='utf-8') as f:
            _CONFIG.write(f)
        _write_config_doc(file)  # 写入注释


def save_template(template_name: str, template_type: Literal['catalog_style', 'border_style'],
                  src: str):
    """
    拷贝样式示例文件到模板文件
    """
    target = os.path.join(get_config().defaults().get('template_path'), f'{template_type}.template')
    with open(src, 'rb') as f:
        tmp = {f'{template_name}': f.read()}
        if os.path.exists(target):
            with open(target, 'rb') as tf:
                tmp.update(pickle.load(tf))
        with open(target, 'wb') as fw:
            pickle.dump(tmp, fw)
    messagebox.showinfo('result', f'成功保存模板 {template_type}.{template_name}')


def _make_ask_file_event(instance, ask_file_fun: Callable, **kwargs):
    """创建文件/文件夹弹窗对话框作为接受事件的函数"""

    def _(event: tk.Event):
        name = event.widget.winfo_name()
        s = ask_file_fun(**kwargs)
        if s != '':
            instance._data[name].set(s)

    return _


def _get_option_to_variable(section: configparser.SectionProxy,
                            options: List[str | Tuple[str, type]] = None,
                            _vars=None):
    """
    从 SectionProxy 对象获取属性值并转化为 Variable 类型数据

    Args:
        section (configparser.SectionProxy): _description_
        options (List[str | Tuple[str, type]] | None): 参数数据
            Tuple[str, type] 参数名称，参数数据类型
            str 等同于 (name, str)
            None 表示以 str 类型获取 section 所有选项值

    Returns:
        _type_: options 对应的字典
    """
    if _vars is None:
        _vars = {}
    _data: Dict[str, Variable] = {}
    if options is None:
        options = section.keys()  # type: ignore
    for _opt in options:
        if type(_opt) is str:
            k, _type = _opt, str
        else:
            k, _type = _opt  # type: ignore
        if _type is bool:
            _data[k] = tk.BooleanVar(value=section.getboolean(k, vars=_vars))
        elif _type is int:
            _data[k] = tk.IntVar(value=section.getint(k, vars=_vars))
        elif _type is float:
            _data[k] = tk.DoubleVar(value=section.getfloat(k, vars=_vars))
        else:
            _data[k] = tk.StringVar(value=section.get(k, vars=_vars))
    return _data


class StyleInfoLabelFrame(ttk.LabelFrame):
    """显示模板样式的属性信息"""

    def __init__(self, master, *, template_type: str, style_name_index: int = 0):
        """
        显示模板样式的属性信息

        Args:
            master (_type_): _description_
            template_type (str): 模板类型，根据类型自动从 Config 中获取样式名称
            style_name_index (int, optional): 样式名称序列下表. Defaults to 0.
        """
        self.template_type = template_type
        self.style_name_list = [
            n.replace(template_type + '.', '') for n in get_config().sections()
            if n.startswith(template_type)
        ]
        self.idx = style_name_index
        super().__init__(master, labelanchor='n')

        self.__data: Dict[str, Variable] = {}

        self.refresh()

        _style_name = self.template_type + '.' + self.style_name_list[self.idx]

        super().config(text=_style_name)

        for r, (k, v) in enumerate(self.__data.items()):
            ttk.Label(self, text=k).grid(column=0, row=r, sticky=W)
            ttk.Label(self, text=':').grid(column=1, row=r, sticky=W)
            ttk.Label(self, textvariable=v, padding=2).grid(column=2,
                                                            row=r,
                                                            sticky=W,
                                                            pady=2,
                                                            padx=2)

    def refresh(self, index=None):
        if index is not None:
            self.idx = index

        conf = get_config_without_default()
        _style_name = self.template_type + '.' + self.style_name_list[self.idx]

        for (k, v) in conf[_style_name].items():
            if k in self.__data.keys():
                self.__data[k].set(v)
            else:
                self.__data[k] = StringVar(self, value=v)


class ModifyConfig(Tk):

    def __init__(self,
                 *,
                 section_name: str,
                 options: List[str | Tuple[str, type]],
                 **kw) -> None:
        """
        修改配置参数

        Args:
            section_name (str): 配置节标签
            options (List[str | Tuple[str, type]]): 参数数据
                Tuple[str, type] 参数名称，参数数据类型
                str 等同于 (name, str)
        """
        super().__init__(**kw)

        _root = ttk.Frame(self, padding=10, name='root')

        # 绑定数据
        _config = get_config()
        self._section = _config[section_name]
        self._data: Dict[str, Variable] = _get_option_to_variable(self._section, options)

        # 组件
        _main_container = ttk.Frame(_root)  # 主要部件容器
        _main_container.pack()
        _info_container = ttk.Frame(_root)  # 模板信息容器
        _info_container.pack(fill='both')
        _footer_container = ttk.Frame(_root)  # 底部容器
        _footer_container.pack()

        # 检查模板样式
        self.__template_style: Dict[str, StyleInfoLabelFrame] = {}
        """模板样式 key--配置名  value--模板样式"""
        for k in (n for n in self._data.keys() if n.endswith('_style')):
            try:
                self.__template_style[k] = StyleInfoLabelFrame(_info_container,
                                                               template_type=k,
                                                               style_name_index=0)
            except:
                ...
        # 显示模板信息
        for style_info in self.__template_style.values():
            style_info.pack(fill='both')
        # 绑定组件
        self.buttons: List[ttk.Button] = []
        for r, (k, v) in enumerate(self._data.items()):
            # 显示配置项名称
            ttk.Label(_main_container, text=k).grid(column=0, row=r, sticky=W)
            # 显示配置项值
            if type(v) is BooleanVar:
                _mid: ttk.Widget = ttk.Frame(_main_container)
                ttk.Radiobutton(_mid, text='yes', variable=v, value=True).grid(column=0,
                                                                               row=0,
                                                                               pady=2,
                                                                               padx=2)
                ttk.Radiobutton(_mid, text='no', variable=v, value=False).grid(column=1,
                                                                               row=0,
                                                                               pady=2,
                                                                               padx=2)
            elif k in self.__template_style.keys():
                # 模板样式使用 Combobox 组件
                _mid = ttk.Combobox(_main_container,
                                    values=self.__template_style.get(k).style_name_list,
                                    state='readonly',
                                    textvariable=v,
                                    width=30,
                                    name=k)
                _mid.bind('<<ComboboxSelected>>', self.__style_select)
                self._style_combobox = _mid
            else:
                _mid = ttk.Entry(_main_container, justify='left', textvariable=v,
                                 width=50)  # type: ignore
            _mid.grid(column=1, row=r, pady=2, padx=2, sticky=W)
            # 文件选择时添加按钮
            if k.endswith(('_file', '_path')):
                _mid.state(('readonly',))  # 文本框设置为不可修改
                _btn = ttk.Button(_main_container, width=5, text="...", name=k)
                _btn.grid(column=2, row=r, pady=2, padx=2)
                if k.endswith('_path'):
                    _btn.bind(
                        '<ButtonPress>',
                        _make_ask_file_event(self,
                                             ask_file_fun=filedialog.askdirectory,
                                             initialdir=self._data[k].get()))
                else:
                    _btn.bind(
                        '<ButtonPress>',
                        _make_ask_file_event(self,
                                             ask_file_fun=filedialog.askopenfilename,
                                             initialfile=self._data[k].get()))
                self.buttons.append(_btn)

        ttk.Button(_footer_container, text="Ok", command=self.__submit).grid(column=0,
                                                                             row=0,
                                                                             padx=10,
                                                                             pady=5)
        ttk.Button(_footer_container, text="Exit", command=self.destroy).grid(column=1,
                                                                              row=0,
                                                                              padx=10,
                                                                              pady=5)

        _root.pack()

    def __style_select(self, event):
        widget: ttk.Combobox = event.widget
        self.__template_style.get(widget._name).refresh(widget.current())
        self.children['root'].pack()

    def __submit(self):
        _: Dict[str, str] = {}
        for k, v in self._data.items():
            _.setdefault(k, str(v.get()))
        self._section.update(_)
        save_config()
        self.destroy()


def modify_project_config():
    """修改项目配置信息"""
    ModifyConfig(
        section_name='project',
        options=[
            'project_path',
            'excel_file',
        ],
    ).mainloop()
    return get_config()['project']


def modify_plot_config():
    """修改打印配置"""
    ModifyConfig(
        section_name='plot',
        options=[
            'print_path',
            'named_template',
            'plot_device',
            'plot_style',
        ],
    ).mainloop()
    return get_config()['plot']


def modify_catalog_config():
    """修改创建图纸目录的配置文件 """
    dialog = ModifyConfig(
        section_name='catalog',
        options=[
            'target_file', 'excel_file', 'catalog_style', 'suffix', 'prefix', ('update', bool),
            ('close', bool)
        ],
    )
    # 修改绑定按钮
    for btn in dialog.buttons:
        btn_name = btn.winfo_name()
        if btn_name == 'target_file':
            btn.bind(
                '<ButtonPress>',
                _make_ask_file_event(dialog,
                                     ask_file_fun=filedialog.asksaveasfilename,
                                     initialfile=dialog._data[btn_name].get(),
                                     defaultextension='.dwg',
                                     filetypes=[('图形', '.dwg'), ('标准', '.dwt')]))

    dialog.mainloop()
    return get_config()['catalog']


def modify_border_config():
    """修改图框配置"""

    ModifyConfig(root,
                 section_name='border',
                 options=['project_path', 'excel_file', 'target_path', ('close', bool)]).mainloop()
    return get_config()['border']


def _add_catalog_template():
    """修改图框配置"""
    AddTemplate(style_type='catalog_style',
                info={
                    'size': '目录图纸大小',
                    'table_block_name': '表格图块名称',
                    'cell_block_name': '单元格图块名称'
                }).mainloop()


class AddTemplate(Tk):

    def __init__(self,
                 *,
                 style_type: Literal['catalog_style', 'border_style'],
                 info: Dict[str, str] = {},
                 **kw) -> None:
        super().__init__(**kw)
        self._style_names = None
        self._data = None
        self.resizable(False, False)

        self._style_type = style_type
        self._info = {'name': '模板名称'}
        self._info.update(info)
        self._new_template: List[Dict[str, Variable]] = []

        self._conf = get_config_without_default()

        # 绑定组件
        _main_container = ttk.Frame(self, name='_main_container', padding=10)
        _main_container.pack()
        _footer_container = ttk.Frame(self, name='_footer_container', padding=10)
        _footer_container.pack()

        self._table_update()

        _btn = [('Add', self._add), ('Ok', self._submit), ('Exit', self.destroy)]
        for i, v in enumerate(_btn):
            ttk.Button(_footer_container, text=v[0], command=v[1]).grid(column=i, row=0, padx=10)

    def _add(self):
        tb: ttk.Treeview = self.children['_main_container'].children['table']  # type: ignore
        header = tb['columns']
        itm = tb.insert('', END, values=[*header])

        # 定义输入框覆盖单元格
        val_dict: Dict[str, Variable] = {}
        self._new_template.append(val_dict)  # 将数据添加到组件
        entry_dict: Dict[str, Tuple[ttk.Entry, int, int, int, int]] = {}

        def _fn(event: tk.Event):
            if event.keycode == 13:
                # 检查重名
                _i = int(event.widget._name)
                if header[_i] == 'name':
                    ...
                    # _sect_names = [n.replace for n in self._conf.sections() if n.startswith(self._style_type)]

                entry_dict.get(header[_i])[0].place_forget()  # 隐藏单元格输入框
                tb.item(itm, values=[v.get() for v in val_dict.values()])  # 更新表格
                if _i < len(header) - 1:
                    # 显示下一个单元格输入框
                    _entry, _x, _y, _w, _h = entry_dict.get(header[_i + 1])
                    _entry.place(x=_x, y=_y, width=_w, height=_h)
                    _entry.focus()

        for i, k in enumerate(header):
            val_dict.setdefault(k, StringVar(tb, value=k))
        for i, k in enumerate(header):
            entry = ttk.Entry(tb, textvariable=val_dict.get(k), name=str(i))
            x, y, w, h = tb.bbox(itm, i)
            entry_dict.setdefault(k, (entry, x, y, w, h))
            entry.bind('<KeyPress>', _fn)
            if i == 0:
                entry.place(x=x, y=y, width=w, height=h)
                entry.focus()

    def _table_update(self):
        _sect_names = [n for n in self._conf.sections() if n.startswith(self._style_type)]
        _tb_header = None
        tb = ttk.Treeview(self.children['_main_container'], show='headings', name='table')
        tb.pack()
        for sect_name in _sect_names:
            sect = self._conf[sect_name]
            sect.setdefault('name', sect_name.replace(self._style_type + '.', ''))
            # 设置表头
            if _tb_header is None:
                _tb_header = [k for k in self._info if k in sect.keys()]
                _tb_header.extend((k for k in sect.keys() if k not in _tb_header))
                tb.configure(columns=_tb_header)
                for v in _tb_header:
                    tb.heading(v, text=self._info.get(v, v))
                    tb.column(v, anchor='center')
            tb.insert('', END, values=[sect.get(k, k) for k in _tb_header])

    def _submit(self):
        style_name = self._data[self._style_type].get()
        file: str = self._data['template_file'].get()
        if style_name in self._style_names:
            messagebox.showerror(title='错误', message='该样式名称已存在，请重新输入！')
        elif not os.path.exists(file) and file.lower().endswith('.dwg'):
            messagebox.showerror(title='错误', message=file + '文件不存在！')
        else:
            save_template(style_name, self._style_type, src=file)
            sect_name = self._style_type + '.' + style_name
            self._style_names.append(style_name)
            _widget: ttk.Combobox = self.children['root'].children['_main_container'].children[
                self._style_type]  # type: ignore
            _widget.config(values=self._style_names)
            for k, v in self._data.items():
                if k != self._style_type and k != 'template_file':
                    if not get_config().has_section(sect_name):
                        get_config().add_section(sect_name)
                    get_config().set(sect_name, k, v.get())
            save_config()

    def __style_select(self, event):
        widget: ttk.Combobox = event.widget
        sn = self._style_names[widget.current()]
        sect = self._conf[self._style_type + '.' + sn]
        for k, v in self._data.items():
            if k != self._style_type:
                v.set(sect.get(k, fallback=''))


# 创建 dwg 属性与 excel 表头的映射
def make_dwg_excel_attr_map(dwg_attrs: List[str], excel_attrs: List[str]) -> Dict[str, str]:
    """
    创建 dwg 属性与 excel 表头的映射

    Args:
        dwg_attrs (List[str]): dwg 图块属性名称列表
        excel_attrs (List[str]): excel 表头名称列表

    Returns:
        Dict[str,str]: key --> dwg 属性名称, value --> excel 表头名称
    """
    _tk = Tk()
    _tk.title('make_dwg_excel_attr_map')

    res: Dict[str, Variable] = {}
    _dwg_attrs = set(tmp.lower() for tmp in dwg_attrs)
    for tmp in _dwg_attrs:
        res.setdefault(tmp, StringVar(_tk, value=tmp if tmp in excel_attrs else ''))

    frm = ttk.Frame(_tk, padding=10)
    frm.pack()
    for i, (attr, v) in enumerate(res.items()):
        ttk.Label(frm, text=attr).grid(sticky=W, column=0, row=i, padx=5, pady=2)
        ttk.Combobox(frm, values=excel_attrs, textvariable=v).grid(column=1, row=i, padx=5, pady=2)

    footer = ttk.Frame(_tk)
    footer.pack()
    ttk.Button(footer, text="Ok", command=_tk.destroy).grid(column=0, row=0, padx=10, pady=5)
    _tk.mainloop()

    return dict((k, v.get()) for k, v in res.items() if not v.get().strip() == '')
