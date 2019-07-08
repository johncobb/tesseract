from abc import ABC, abstractmethod

class ParserAbstract(ABC):

    def __init__(self):
        self.blacklist = [["I", "1"], ["O", "0"], ["Q", "0"]]
        super().__init__()


    @abstractmethod
    def parse(self, file):
        pass


    
# class Kia(ParserAbstract):

#     def parse(self, file):
#         print("Hello Kia Parser" + file)



# if __name__ == "__main__":
#     parser_kia = Kia()

#     parser_kia.parse("this file")

# class Parser:
#     def load(self):
#         pass
#     def parse(self):
#         pass
#     def save(self):
#         pass

#     @classmethod
#     loadParserClass(cls, ...):

#         if conditionA:
#             return Parser
