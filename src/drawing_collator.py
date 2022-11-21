'''
蓝图整理工具
图纸命名格式：[图号_][图名_]_子项名称.pdf/.dwf
'''

import logging
import os
import os.path
import shutil
import sys
import yaml

from abstract import Command


class CategorizeBySubproject:
    ''' 通过子项名称分类 '''

    def __init__(self) -> None:
        '''
        Args:
            path: 图纸文件目录
        '''
        print('输入文件夹路径', end=': ')
        self.path = input()

    def action(self):
        dirs = os.listdir(self.path)
        for dir in dirs:
            src = os.path.join(self.path, dir)
            if os.path.isfile(src):
                p, n = os.path.split(src)
                name, ext = os.path.splitext(n)
                # 没有下划线则直接跳过
                if name.find('_') == -1:
                    continue
                name = name.strip()
                tmp = name.split('_')[-1]
                dst = os.path.join(self.path, tmp, name + ext)
                tmp = os.path.split(dst)
                if not os.path.exists(tmp[0]):
                    os.makedirs(tmp[0])
                shutil.move(src, dst)
                print(f'{dir} --> {dst}')


class CopyGeneralToSubproject:
    ''' 将通用图拷贝的各个子项文件夹 '''

    def __init__(self, path, config, source) -> None:
        '''
        Args:
            path: 项目根目录，所有子项文件夹位于该文件夹下
            config: 配置文件路径, 配置文件格式 { 子项名称：[ 该子项需要的通用图号 ] }
            source: 通用图路径
        '''
        self.path, self.config, self.source = (path, config, source)

    def action(self):
        path, config, source = (self.path, self.config, self.source)
        # 加载配置
        with open(config, encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        # 将图号与通用图关联 { 图号：[图纸路径]}
        dic = {}
        for dir in [d for d in os.listdir(source) if d.find('_') > -1]:
            no = dir.split('_')[0]
            if no not in dic:
                dic[no] = []
            dic[no].append(os.path.join(source, dir))
        # 遍历配置文件，复制图纸
        for k, ns in config.items():
            for n in ns:
                if n in dic:
                    for src in dic[n]:
                        p, name = os.path.split(src)
                        dst = os.path.join(path, k, name)
                        shutil.copy(src, dst)
                        print(src, '-->', dst)


class CopyGeneralToSubprojectCMD:
    ''' 将通用图拷贝的各个子项文件夹 '''

    def __init__(self) -> None:
        print('输入项目根目录(所有子项文件夹位于该文件夹下)', end=' : ')
        path = input()
        print('输入配置文件路径(配置文件格式 { 子项名称：[通用图号]})', end=' : ')
        config = input()
        print('输入通用图路径(输入 Enter 跳过, 默认为项目根目录下的 "通用图" 文件夹)', end=' : ')
        source = input()
        if source == '':
            source = os.path.join(path, '通用图')
        self.cmd = CopyGeneralToSubproject(path, config, source)

    def execute(self):
        self.cmd.action()


if __name__ == '__main__':
    print('*' * 20)
#     CategorizeBySubproject().action()

# while True:
#     cmds = [('CategorizeBySubproject', '按子项分类'), ('CopyGeneralToSubproject', '将通用图拷贝的各个子项文件夹')]
#     idx = 0
#     for k, v in cmds:
#         print(idx, ' ', k, ':', v)
#         idx += 1
#     print('输入对应编号选择功能(输入 quit / q 退出)', end=' : ')
#     try:
#         i = input()
#         if (i.lower() == 'quit') | (i == 'q'):
#             break
#         i = int(i)
#         cmd = globals()[cmds[i][0]]()
#         invoker = Invoker(cmd)
#         invoker.call()
#     except Exception as e:
#         print(e)
