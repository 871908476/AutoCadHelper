import os.path
import sys

os.chdir('src')

from src.commands import *
from src.manager_commands import *

logging.basicConfig(level=logging.INFO,
                    filename=r'../exception.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger(__name__)


def cmd_invoke():
    """命令行调用"""
    args = sys.argv[1:]
    try:
        if len(args) < 1:
            raise ValueError("至少应有一个参数作为命令名称")
        cmd: Command = globals().get(args[0])()
        cmd.execute()
    except Exception as e:
        logger.error(repr(e))


if __name__ == '__main__':
    cmd_invoke()
