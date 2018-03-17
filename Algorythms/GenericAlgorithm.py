from abc import ABC, abstractmethod

class GenericAlgorithm(ABC):

    def __init__(self):

        self.animation = None
        self.control_panel = None
        super().__init__()

    @abstractmethod
    def update(self, frame):
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def start(self):
        pass
