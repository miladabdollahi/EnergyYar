from abc import ABC, abstractmethod


class ReaderBase(ABC):

    @abstractmethod
    def read(self, bank_type, **options):
        pass

    @abstractmethod
    def get_class(self, bank_type, **options):
        pass

    @abstractmethod
    def default(self):
        pass
