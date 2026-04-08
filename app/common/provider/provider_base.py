from abc import ABC, abstractmethod
from datetime import date

class ProviderBase(ABC):

    @abstractmethod
    def get_compute_list(self):
        pass

    @abstractmethod
    def get_compute_cost(self, start_date: date, end_date: date):
        pass

    @abstractmethod
    def get_storage_list(self):
        pass

    @abstractmethod
    def get_storage_cost(self, start_date: date, end_date: date):
        pass
