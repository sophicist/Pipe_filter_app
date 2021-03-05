from abc import ABCMeta, abstractmethod


class Iterator(metaclass=ABCMeta):
    # @staticmethod
    # @abstractmethod
    # def has_next():
    #   "returns boolean whether this is the end of collection or not"

    @staticmethod
    @abstractmethod
    def next():
        "return the next object in the collection"
#################################################################################


class Iterable(Iterator):

    def __init__(self, data):
        self.data = data
        self.index = [i[0] for i in enumerate(self.data)]
        self.min = 0
        self.max = self.index[-1]

    def add(self, new_list):
        self.data.append(new_list)

    def next(self):
        return self.data[-1]
