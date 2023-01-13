import collections
import os
import os.path
import pickle
from abc import abstractmethod
from collections import defaultdict
from dataclasses import asdict
from itertools import chain

from typing import Dict, List, Tuple
from typing import Literal

import tkinter.filedialog
import yaml
from tkinter import messagebox, BooleanVar, IntVar, DoubleVar, YES, Menu
from tkinter import W, Tk, Variable, filedialog, ttk, StringVar
from tkinter.ttk import Radiobutton, Notebook, Frame, Button, LabelFrame, Label, Entry, Combobox, Widget, Style, \
    Menubutton
from .acad_utils import get_application, open_file
from .config import *


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


class ISubmit:
    @abstractmethod
    def submit(self):
        """提交修改"""
        pass


class SettingFrame(Tk, ISubmit):
    def __init__(self, select: str = None, **kw):
        super().__init__(**kw)
        self.title('Setting')
        self._note_boot = Notebook(self, padding=10, name='root', width=600)

        self.__add_frame(SystemFrame, '系统设置', 'system')
        self.__add_frame(ProjectFrame, '项目设置', 'project')
        self.__add_frame(TemplateFrame, '模板设置', 'template')

        self._note_boot.pack(fill='both')
        if select and select in self._note_boot.children.keys():
            self._note_boot.select('.root.' + select)
        self.bind("<<NotebookTabChanged>>", self.__tab_changed)

        self._bottom = Frame(self)
        Button(self._bottom, text='应用', command=self.submit).pack()
        self._bottom.pack(pady=(0, 10))

        self.resizable(False, False)

    def submit(self):
        _i = self._note_boot.index("current")
        _itm = [*self._note_boot.children.values()][_i]
        _itm.submit()
        # self.destroy()

    def __tab_changed(self, event):
        print(self._note_boot.select())

    def __add_frame(self, frame: type, text: str, name: str):
        self._note_boot.add(frame(self._note_boot, padding=10, name=name), text=text)


class SystemFrame(Frame, ISubmit):
    """系统设置"""
    __ver = {
        24: 'AutoCad2021',
        23: 'AutoCad2020'
    }

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        # 设置关联变量
        self._var: Dict[str, Variable] = {}
        for k, v in sys_config.__dict__.items():
            if k == 'acad_version':
                self._var.setdefault(k, StringVar(self, self.__acad_version_convert(v)))
            else:
                self._var.setdefault(k, StringVar(self, v))

        _frm1 = LabelFrame(self, text='系统配置')

        # 存放网格布局元素的二维列表
        _children = []
        for _r, (k, info) in enumerate((('temp_path', '临时文件保存路径'),
                                        ('catalog_template_file', '目录模板文件路径'),
                                        ('border_template_file', '图框模板文件路径'))):
            _btn = Button(_frm1, text='...', width=5, name=k)
            _btn.bind('<Button-1>', self.__btn_bind(k))
            _children.append([
                Label(_frm1, text=info),
                Entry(_frm1, justify='left', textvariable=self._var.get(k)),
                _btn
            ])

        _children.append([
            Label(_frm1, text='AutoCAD 版本'),
            Combobox(_frm1, justify='left', textvariable=self._var.get('acad_version'), state='readonly',
                     values=['AutoCad2020', 'AutoCad2021'])
        ])
        # 网格布局
        _frm1.grid_columnconfigure(1, weight=1)
        for _r, _lst in enumerate(_children):
            for _c, _itm in enumerate(_lst):
                _itm.grid(column=_c, row=_r, sticky='nsew', padx=3, pady=2)

        _frm1.pack(fill='both')

    def __btn_bind(self, name: str):
        """产生 Button 绑定函数"""

        def _(event):
            if name == 'temp_path':
                self._var.get(name).set(filedialog.askdirectory())
            else:
                self._var.get(name).set(filedialog.askopenfilename(filetypes=[('模板文件', '.template')]))

        return _

    def __acad_version_convert(self, _ver: int | str):
        if isinstance(_ver, int):
            return SystemFrame.__ver.get(_ver)
        else:
            _dic = {v: k for k, v in SystemFrame.__ver.items()}
            return _dic.get(_ver)

    def submit(self):
        for k, v in self._var.items():
            if k == 'acad_version':
                setattr(sys_config, k, self.__acad_version_convert(v.get()))
            else:
                setattr(sys_config, k, v.get())
        save_sys_config()


class ProjectFrame(Frame, ISubmit):
    """项目配置"""

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self._saved = True
        self._project_name_list: List[str] = ['创建新项目...', *get_all_project_config_names()]

        # 基本信息可变量
        self._var: Dict[str, Variable] = defaultdict(self.__var_factory)
        # 打印信息
        self._plot_var: Dict[str, Variable] = defaultdict(self.__var_factory)
        # 目录生成器
        self._catalog_var: Dict[str, Variable] = defaultdict(self.__var_factory)

        # 初始化
        self._conf = ProjectConfig()
        self.__set_config(self._conf)

        # 基本信息
        self.__init_info_label_frame().pack(fill='both')
        # 打印设置
        self.__init_plot_label_frame().pack(fill='both', pady=5)
        # 自动生成目录配置
        self.__init_catalog_frame().pack(fill='both')

    def __var_factory(self, val=None):
        """可变量默认值"""
        if val is None:
            _var = Variable(self, '')
        elif isinstance(val, int):
            _var = IntVar(self, val)
        elif isinstance(val, float):
            _var = DoubleVar(self, val)
        elif isinstance(val, str):
            _var = StringVar(self, val)
        elif isinstance(val, bool):
            _var = BooleanVar(self, val)
        else:
            _var = Variable(self, val)
        _var.trace_add('write', self.__entry_change)
        return _var

    def __set_config(self, conf: ProjectConfig):
        self._conf = conf
        # 基本信息可变量
        for k, v in asdict(self._conf).items():
            self._var[k].set(v)
        # 打印信息
        for k, v in asdict(self._conf.plot).items():
            self._plot_var[k].set(v)
        # 目录生成器
        for k, v in asdict(self._conf.catalog_generator).items():
            self._catalog_var[k].set(v)
        # 当前状态：已保存、修改未保存
        self._saved = True

    def __var_convert_to_config(self):
        """根据界面可变量创建配置类"""
        _plt = Plot(**{k: v.get() for k, v in self._plot_var.items()})
        _clg = CatalogGenerator(**{k: v.get() for k, v in self._catalog_var.items()})
        self._conf = ProjectConfig(**{k: v.get() for k, v in self._var.items()})
        self._conf.plot = _plt
        self._conf.catalog_generator = _clg
        return self._conf

    def __create(self):
        create_project_config(self.__var_convert_to_config())
        self._project_name_list.append(self._conf.name)

    def __name_box_change(self, event):
        """项目名称选择事件"""
        if self._project_name_list[0] == self._var.get('name').get():
            event.widget.config(state='normal')
            self._conf = ProjectConfig(name=self._var.get('name').get())
            self.__set_config(self._conf)
            # self._saved = False
        else:
            event.widget.config(state='readonly')
            self.__set_config(get_project_config(self._var.get('name').get()))

    def __name_box_post_select(self, _frm):
        """项目名称选择前的回调函数"""
        if not self._saved:
            if messagebox.askokcancel('warning', '当前项目没有保存，是否保存？'):
                self.submit()
        _frm.children['project_name']['values'] = self._project_name_list

    def submit(self):
        if not self._var.get('name').get() or self._var.get('name').get() == self._project_name_list[0]:
            messagebox.showwarning('warning', '输入项目名称')
            return
        elif self._var.get('name').get() not in self._project_name_list:
            if not messagebox.askokcancel('info', f'是否创建项目 {self._var.get("name").get()} ？'):
                return
            self.__create()
        save_project_config(self.__var_convert_to_config())
        self._saved = True

    def __entry_change(self, *args):
        """标记已修改待保存"""
        self._saved = False

    def __init_info_label_frame(self):
        _frm = LabelFrame(self, text='项目信息')

        # 存放网格布局元素的二维列表
        _children = [[
            Label(_frm, text='项目名称'),
            Combobox(_frm, values=self._project_name_list,
                     postcommand=lambda: self.__name_box_post_select(_frm),
                     state='readonly',
                     textvariable=self._var.get('name'), name='project_name'),
        ]]
        _children[0][1].bind("<<ComboboxSelected>>", self.__name_box_change)
        for k, info, fn in [('project_path', '项目根目录', self.__askdirectory(self._var.get('project_path'))),
                            ('excel_file', '配置文件路径',
                             self.__askopenfilename(self._var.get('excel_file'), filetypes=[('excel 配置文件', '.xlsx')]))]:
            itm = [
                Label(_frm, text=info),
                Entry(_frm, justify='left', textvariable=self._var.get(k)),
                Button(_frm, text='...', width=5, command=fn)
            ]
            _children.append(itm)
        # 网格布局
        _frm.grid_columnconfigure(1, weight=1)
        self.__grid(_children)
        return _frm

    def __init_plot_label_frame(self):
        frame_text = '打印配置'
        _data = [('plot_device', '打印设备'), ('plot_style', '打印样式'), ('print_path', '输出到文件夹'),
                 ('named_template', '输出命名模板')]
        _children = []
        _frm = LabelFrame(self, text=frame_text, name='plot_frame')
        for k, info in _data:
            lst = [
                Label(_frm, text=info),
                Entry(_frm, justify='left', textvariable=self._plot_var.get(k)),
            ]
            if k == 'print_path':
                lst.append(Button(_frm, text='...', width=5, command=self.__askdirectory(self._plot_var.get(k))))
            _children.append(lst)
        # 网格布局
        _frm.grid_columnconfigure(1, weight=1)
        self.__grid(_children)
        return _frm

    def __init_catalog_frame(self):
        frame_text = '自动生成目录配置'
        _data = [('target_file', '保存到文件'), ('style', '目录模板样式'), ('suffix', '布局名称后缀'), ('prefix', '布局名称前缀'),
                 ('update', '仅更新'), ('close', '完成后关闭')]
        _frm = LabelFrame(self, text=frame_text, name='catalog_frame')
        _children = []
        for k, info in _data:
            _itm = [
                Label(_frm, text=info),
                Entry(_frm, justify='left', textvariable=self._catalog_var.get(k)),
            ]
            if k == 'update' or k == 'close':
                _rb = Frame(_frm, name=k)
                Radiobutton(_rb, text='是', value=True, variable=self._catalog_var.get(k)).pack(side='left')
                Radiobutton(_rb, text='否', value=False, variable=self._catalog_var.get(k)).pack(side='left')
                _itm[1] = _rb
            if k == 'target_file':
                _itm.append(
                    Button(_frm, text='...', width=5,
                           command=self.__asksaveasfilename(self._catalog_var.get(k), filetypes=[('excel', '.xlsx')])))
            _children.append(_itm)

        # 网格布局
        _frm.grid_columnconfigure(1, weight=1)
        self.__grid(_children)
        return _frm

    def __grid(self, _children: List[List[Widget]]):
        for _r, _lst in enumerate(_children):
            for _c, _itm in enumerate(_lst):
                _itm.grid(column=_c, row=_r, sticky='nsew', padx=3, pady=2)

    def __asksaveasfilename(self, _var: Variable, **kw):
        """
        询问保存文件名
        @param _var: 将结果保存到指定可变量 Variable
        """

        def _(event=None):
            _file = filedialog.asksaveasfilename(**kw)
            if _file:
                _var.set(_file)

        return _

    def __askdirectory(self, _var: Variable, **kw):
        """
        询问文件夹
        @param _var: 将结果保存到指定可变量 Variable
        """

        def _(event=None):
            _file = filedialog.askdirectory(**kw)
            if _file:
                _var.set(_file)

        return _

    def __askopenfilename(self, _var: Variable, **kw):
        """
        询问打开文件的文件名
        @param _var: 将结果保存到指定可变量 Variable
        """

        def _(event=None):
            _file = filedialog.askopenfilename(**kw)
            if _file:
                _var.set(_file)

        return _


class TemplateFrame(Frame, ISubmit):

    def __init__(self, master, **kw) -> None:
        """
        模板文件管理
        @param kw: 其它组件参数
        """
        super().__init__(master, **kw)
        self.__modify_widget: Widget | None = None
        self.__new_item_cad_path: Dict[str, str] = defaultdict()  # 存放新添加的模板 Dict(模板名称,cad路径)
        self.__header_dict = collections.OrderedDict({
            'name': '模板名称',
            'size': '图纸尺寸',
            'table_block_name': '表格图块名称',
            'cell_block_name': '单元格图块名称'
        })
        self.__new_item_entry: Dict[str, Entry | Combobox] = defaultdict()
        self.__treeview = ttk.Treeview(self, show='headings', name='table', columns=list(self.__header_dict.keys()))
        self.__init_treeview()

    def submit(self):
        # 读取 cad 文件保存到 .template
        modify_template('catalog',)
        # 保存配置信息
        # save_catalog_template_config()

    def __init_treeview(self):
        """初始化表格"""
        # 设置列标题
        for k, v in self.__header_dict.items():
            self.__treeview.heading(k, text=v)
            self.__treeview.column(k, anchor='center', width=100, minwidth=100)
        # 插入行
        for itm in get_all_catalog_template_config():
            self.__treeview.insert('', 'end', values=list(asdict(itm).values()), iid=itm.name)
        self.__treeview.bind('<Double-Button>', self.__modify_item)
        # self.__treeview.bind('<<TreeviewSelect>>', self.__treeview_change)
        self.__treeview.bind('<Button-3>', self.__right_menu)
        self.__treeview.pack(fill='both')

    def __check_entry(self, *args):
        """
        检查输入并更新到表格
        @param args: (modify_column, 修改后的值, iid)
        @return:
        """
        """"""
        # print(f'{args=}')
        _key, _new, iid = args
        _key: str = _key.split('.')[-1].replace('modify_', '')
        _old = self.__treeview.set(self.__treeview.get_children()[-1], _key)
        _flag = True
        if _key == 'name':
            _names = [self.__treeview.set(itm, 'name') for itm in self.__treeview.get_children()]
            if '输入模板名称...' == _new or (_names.count(_new) != 1 if _new != _old else 0):
                messagebox.showerror('error', '名称不可用！')
                _flag = False
        elif not _new.strip():
            messagebox.showerror('error', '不能为空！')
            _flag = False

        # 如果检查通过，更新到 treeview, 否则恢复原值
        self.__treeview.set(iid, _key, _new if _flag else _old)
        # 修改 cad 路径
        if _old in self.__new_item_cad_path.keys():
            self.__new_item_cad_path[_new] = self.__new_item_cad_path[_old]
            del self.__new_item_cad_path[_old]

        # 修改配置文件
        if _flag:
            _opt = {k: self.__treeview.set(iid, k) for k in self.__header_dict.keys()}
            _name = _opt.get('name') if _key != 'name' else _old
            modify_catalog_template_config(_name, _opt)

        return _flag

    def __get_cad_block_names(self):
        # 读取 dwg 文件
        _file_name = tkinter.filedialog.askopenfilename(filetypes=[('图形文件', '.dwg')], title='选取模板文件')
        if not _file_name:
            return
        # 读取图块名称
        _app = get_application(visible=True)
        _doc = open_file(_app, file=_file_name)
        _block_names = [_.Name for _ in _doc.Blocks if not _.IsLayout]
        _doc.Close()

        _block_names = ['cell', 'table']
        return _block_names

    def __modify_item(self, event):
        """双击修改表中的值"""
        _col = int(self.__treeview.identify_column(event.x).replace('#', ''))
        _iid = self.__treeview.identify_row(event.y)

        if self.__modify_widget is not None:
            self.__modify_widget.destroy()
        if not _iid:
            self.__treeview.selection_set([])
            return

        k = list(self.__header_dict.keys())[_col - 1]
        _val = self.__treeview.set(_iid, k)
        name = f'modify_{k}'
        # 定义修改组件
        if k == 'size':
            self.__modify_widget = ttk.Combobox(self, name=name, values=['A0', 'A1', 'A2', 'A3', 'A4'],
                                                state='readonly')
        else:
            self.__modify_widget = ttk.Entry(self, name=name)
        # 设置组件当前值
        _type = type(self.__modify_widget)
        if _type is Entry:
            self.__modify_widget.insert(0, _val)
        elif _type is Combobox:
            self.__modify_widget.set(_val)

        self.__modify_widget.configure(validate='focusout', justify='center',
                                       validatecommand=(self.register(self.__check_entry), '%W', '%P', _iid),
                                       takefocus=True)
        x, y, w, h = self.__treeview.bbox(_iid, _col - 1)
        self.__modify_widget.place(x=x, y=y, width=w, height=h)
        self.__modify_widget.focus()
        self.__modify_widget.select_range(0, 'end')

    def __add_new_item(self):
        """在末尾追加新行"""
        _file_name = tkinter.filedialog.askopenfilename(filetypes=[('图形文件', '.dwg')], title='选取模板文件')
        if _file_name:
            self.__treeview.insert('', 'end', tags='new_line')
            self.__treeview.tag_configure('new_line', foreground='gray')
            _dict = asdict(CatalogStyle(name='输入模板名称...'))
            self.__treeview.item(self.__treeview.get_children()[-1], values=[*_dict.values()])
            self.__new_item_cad_path[_dict['name']] = _file_name
            modify_catalog_template_config(_dict.get('name'), _dict)

    def __del_item(self):
        """删除条目"""
        for iid in self.__treeview.selection():
            delete_catalog_template_config(self.__treeview.set(iid, 'name'))
            self.__treeview.delete(iid)

    def __check_data(self):
        """检查所有数据是否合法"""
        # 检查空字符
        if '' in [_.strip() for itm in self.__treeview.get_children() for _ in self.__treeview.item(itm, 'value')]:
            return False
        # 检查重名
        _names = [self.__treeview.set(itm, 'name') for itm in self.__treeview.get_children()]
        _count = len(self.__treeview.get_children())
        return not any(['输入模板名称...' in _names, len(set(_names)) < _count])

    def __right_menu(self, event):
        """右键菜单"""
        _frm = Frame(self, name='right_menu')
        Button(_frm, text='添加', command=lambda: (self.__add_new_item(), _frm.destroy()),
               state='disabled' if not self.__check_data() else 'normal').pack()
        Button(_frm, text='删除', command=lambda: (self.__del_item(), _frm.destroy()),
               state='normal' if self.__treeview.selection() else 'disabled').pack()
        _frm.place(x=event.x, y=event.y)
        _frm.bind('<Leave>', lambda e: _frm.destroy())

    #
    # def _submit(self):
    #     _conf = get_config_without_default()
    #     if not self._new_template_vals:
    #         return
    #     # 检查重名
    #     _names = [n for n in _conf.sections() if n.startswith(self._prefix)]
    #     for itm, _, __ in self._new_template_vals:
    #         _n = self._prefix + '.' + itm.get('name').get()
    #         if _n in _names:
    #             messagebox.showerror(title='错误', message=f'样式名称 {_n} 已存在，请重新输入！')
    #             return
    #         _names.append(_n)
    #
    #     for itm, _, _file in self._new_template_vals:
    #         add_to_template(itm.get('name').get(), self._prefix, src=_file)
    #         sect_name = self._prefix + '.' + itm.get('name').get()
    #         get_config().add_section(sect_name)
    #         for k, v in itm.items():
    #             get_config().set(sect_name, k, v.get())
    #         save_config()
    #     self._table_update()
    #
    # def add_to_template(self, template_name: str, template_type: Literal['catalog_style', 'border_style'],
    #                     src: str):
    #     """
    #     保存样式到模板文件
    #     """
    #     target = os.path.join(get_config().defaults().get('template_path'), f'{template_type}.template')
    #     with open(src, 'rb') as f:
    #         tmp = {f'{template_name}': f.read()}
    #         if os.path.exists(target):
    #             with open(target, 'rb') as tf:
    #                 tmp.update(pickle.load(tf))
    #         with open(target, 'wb') as fw:
    #             pickle.dump(tmp, fw)
    #     messagebox.showinfo('result', f'成功保存模板 {template_type}.{template_name}')
