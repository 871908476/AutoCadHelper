from configparser import SectionProxy
from tkinter import W, StringVar, Tk, Variable, ttk, BooleanVar, IntVar, DoubleVar

from typing import Dict, List, Tuple


def get_option_to_variable(master, section: SectionProxy,
                           options: List[str | Tuple[str, type]] = None,
                           _vars=None):
    """
    从 SectionProxy 对象获取属性值并转化为 Variable 类型数据
    @param master: 所属组件
    @param section: _description_
    @param options: 参数数据, Tuple[str, python_type] 参数名称，参数数据类型, str 等同于 (name, str), None 表示以 str 类型获取 section 所有选项值
    @param _vars: 默认值
    @return: 对应的字典
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
            _data[k] = BooleanVar(master, value=section.getboolean(k, vars=_vars))
        elif _type is int:
            _data[k] = IntVar(master, value=section.getint(k, vars=_vars))
        elif _type is float:
            _data[k] = DoubleVar(master, value=section.getfloat(k, vars=_vars))
        else:
            _data[k] = StringVar(master, value=section.get(k, vars=_vars))
    return _data


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
