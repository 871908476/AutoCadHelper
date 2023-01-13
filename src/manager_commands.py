from tkinter.filedialog import asksaveasfilename

from .abstract import Command
from .manager_view import SettingFrame


class Setting(Command):
    """修改配置信息"""

    def __init__(self, select: str = None, **kwargs):
        super().__init__(**kwargs)
        self.__select = select

    def execute(self):
        SettingFrame(select=self.__select).mainloop()
        # match self.__section:
        #     case 'project':
        #         modify_project_config()
        #     case 'plot':
        #         modify_plot_config()
        #     case 'catalog':
        #         modify_catalog_config()
        #     case 'border':
        #         modify_border_config()
        #     case _:
        #         pass


def modify_project_config():
    """修改项目配置信息"""
    SettingFrame(
        section_name='project',
        options=[
            'project_path',
            'excel_file',
        ],
    ).mainloop()


def modify_plot_config():
    """修改打印配置"""
    SettingFrame(
        section_name='plot',
        options=[
            'print_path',
            'named_template',
            'plot_device',
            'plot_style',
        ],
    ).mainloop()


def modify_catalog_config():
    """修改创建图纸目录的配置文件 """
    dialog = SettingFrame(
        section_name='catalog',
        options=[
            'target_file', 'excel_file', 'catalog_style', 'suffix', 'prefix', ('update', bool),
            ('close', bool)
        ],
    )

    # def _(event: tk.Event):
    #     name = event.widget.winfo_name()
    #             s = asksaveasfilename(initialfile=)
    #             if s != '':
    #                 dialog._data[name].set(dialog._data[btn_name].get())
    #
    #         return _

    # 修改绑定按钮
    for btn in dialog.buttons:
        btn_name = btn.winfo_name()
        if btn_name == 'target_file':
            btn.bind(
                '<ButtonPress>', asksaveasfilename)

    dialog.mainloop()


def modify_border_config():
    """修改图框配置"""

    SettingFrame(section_name='border',
                 options=['project_path', 'excel_file', 'target_path', ('close', bool)]).mainloop()
