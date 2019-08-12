from abc import ABC, abstractmethod

class ParserAbstract(ABC):

    def __init__(self):
        self.blacklist = [["I", "1"], ["O", "0"], ["Q", "0"]]
        super().__init__()


    @abstractmethod
    def parse(self, file):
        pass