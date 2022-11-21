import pickle

import commands
from commands import *
from common_utils import get_config, logging_except, modify_border_config, modify_catalog_config, modify_plot_config

# logging.basicConfig(level=logging.INFO,
#                     filename=r'E:\repo\tools\AutocadHelper\log\invoker.log',
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     encoding='utf-8')
logger = logging.getLogger(__name__)


def cmd_invoke():
    """命令行调用"""
    try:
        args = sys.argv[1:]
        if len(args) < 1:
            raise ValueError("至少应有一个参数作为命令名称")
        cmd: commands.Command = getattr(commands, args[0])()
        cmd.execute()
    except Exception as e:
        logger.error(repr(e))


# 创建临时文件
def _create_temp_file(template_file: str, style_name: str, temp_path: str) -> str:
    """
    创建临时文件

    Args:
        template_file (str): 模板文件路径
        style_name (str): 模板样式名称
        temp_path (str): 临时文件所在文件夹路径

    Returns:
        str: 临时文件路径, 临时文件的文件名为模板样式名
    """
    target_file = os.path.join(temp_path, f'{style_name}.dwg')
    with open(template_file, 'rb') as f:
        tmp: dict = pickle.load(f)
        _data = tmp.get(style_name, None)
        if _data is None:
            raise IOError(f'{style_name} 样式不存在')
        _dir = os.path.dirname(target_file)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        with open(target_file, 'wb') as fw:
            fw.write(_data)
    return target_file


def _create_catalog_style():
    """
    获取模板样式
    """
    try:
        conf = get_config()
        style_name = conf['catalog']['catalog_style']
        sect_name = 'catalog_style.' + style_name
        if sect_name in conf.sections():
            sect = conf[sect_name]
        else:
            sect = conf[sect_name]
        _paper = conf['plot.paper_size'][sect.get('size')]
        ##############################
        # template_file = _create_temp_file(sect['catalog_template_file'], style_name,
        #                                   sect['temp_path'])
        #######################
        return CatalogStyle(template_file=r'D:\repo\tools\AutocadHelper\temp\catalog_style_zhongdian2.dwg',
                            # template_file,
                            paper=_paper,
                            table_block_name=sect['table_block_name'],
                            cell_block_name=sect['cell_block_name'])
    except Exception as e:
        logging.error(e.args)
        raise


# 创建目录
def create_catalog_invoker():
    """创建目录"""
    app = acad_utils.get_application(version=23)
    # 从配置文件读取上一次的配置
    sect = modify_catalog_config()
    try:
        # 读取目录样式
        _ccs = _create_catalog_style()
        # 读取 excel 数据
        _suffix = sect.get('suffix')
        _prefix = sect.get('prefix')
        _excel_file = sect.get('excel_file')
        _catalog_data: Dict[str, List[Dict]] = {}
        _: Dict[str, pd.DataFrame] = pd.read_excel(_excel_file, sheet_name=None, dtype=str)
        # 创建目录表格数据
        for k, v in _.items():
            _catalog_data[_prefix + k + _suffix] = [i for i in v.to_dict(orient='index').values()]
        # 创建命令并执行
        CreateCatalog(application=app,
                      catalog_style=_ccs,
                      catalog_data=_catalog_data,
                      target_file=sect.get('target_file'),
                      update=sect.getboolean('update'),
                      close=sect.getboolean('close')).execute()
        ############################
        # 删除临时文件
        # os.remove(_ccs.template_file)
    except Exception as e:
        logging.error(e.args)
        raise


# 添加目录模板
def add_catalog_template():
    ...


@logging_except
def insert_border_invoker():
    """插入图框"""
    app = acad_utils.get_application(version=24)
    # 从配置文件读取上一次的配置
    sect = modify_border_config()
    try:
        _: Dict[str, pd.DataFrame] = pd.read_excel(sect.get('excel_file'),
                                                   dtype=str,
                                                   sheet_name=None)
        data = []
        styles_dict = {}
        _dir = sect['target_path']
        for ignor, tb_data in _.items():
            tb_data.dropna(inplace=True,
                           axis='index',
                           subset=['border_style', 'layout', 'file'],
                           how='any')
            for dic in tb_data.to_dict(orient='records'):
                style_name = dic.get('border_style')
                if style_name not in styles_dict.keys():
                    _file = _create_temp_file(template_file=sect.get('border_template_file'),
                                              style_name=style_name,
                                              temp_path=sect.get('temp_path'))
                    _size = get_config()['border_style.' + style_name]['size']
                    styles_dict[style_name] = BorderStyle(template_file=_file, size=_size)
                data.append(
                    (os.path.join(_dir,
                                  dic.get('file')), dic.get('layout'), styles_dict[style_name]))
        InsertBorder(application=app, data=data, close=sect.getboolean('close')).execute()
    except Exception as e:
        logging.error(e.args)
        # raise


@logging_except
def modify_signature_and_plot_invoker():
    """修改图签并打印图纸"""
    app = acad_utils.get_application(version=24)
    # 从配置文件读取上一次的配置
    sect = modify_plot_config()
    _project_path = sect.get('project_path')
    _excel_file = sect.get('excel_file')
    _: Dict[str, pd.DataFrame] = pd.read_excel(_excel_file, sheet_name=None, dtype=str)
    # 创建目录表格数据
    _data: Dict[str, List[Dict]] = {}
    for k, v in _.items():
        _data[k] = v.to_dict(orient='index')
    ModifySignatureAndPlot(
        application=app,
        info_data=_data,
        project_path=_project_path,
        block_name='图签',
        plot=True,
        close=False,
        print_path=sect['print_path'],
    ).execute()



if __name__ == '__main__':
    print('*' * 20)
    create_catalog_invoker()
    # insert_border_invoker()
    # modify_signature_and_plot_invoker()
# conf = modify_catalog_config()
# sect = conf['catalog']
# print(sect.get('target_dwg_file'))

# app = get_application(version=24)
# doc = app.ActiveDocument
# lys = doc.Layouts
# bs = lys.Item('布局1').Block
# print(bs.Name)
# for b in bs:
#     print(b.ObjectName)

# while True:
#     cmds = [(CreateCatalog, '按子项分类'), (ModifyDrawingInfo, '将通用图拷贝的各个子项文件夹')]
#     for idx, (k, v) in enumerate(cmds):
#         print(idx, ' ', k.__name__, ' ', v)
#     i = input('输入命令序号(输入 quit 退出) : ')
#     try:
#         if (i.lower() == 'quit'):
#             break
#         i = int(i)
#         invoker = Invoker(cmds[i][0])
#         invoker.call()
#     except Exception as e:
#         print(e)
