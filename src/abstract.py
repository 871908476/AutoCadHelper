from abc import abstractmethod


class Command:
    ''' 
    抽象命令类 
    
    '''

    def __init__(self, **kwargs) -> None:
        pass

    @abstractmethod
    def execute(self):
        pass