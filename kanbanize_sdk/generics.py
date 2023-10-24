from abc import ABCMeta, abstractmethod
from .wrapper import KanbanizeSession


class GenericRequestMethod(metaclass=ABCMeta):

    __endpoint = ''

    def __init__(self, service: KanbanizeSession, *args, **kwargs):
        self.service = service

    @property
    def endpoint(self):
        return self.__endpoint

    @abstractmethod
    def insert(self, *args, **kwargs):
        ...

    @abstractmethod
    def update(self, *args, **kwargs):
        ...

    @abstractmethod
    def get(self, *args, **kwargs):
        ...

    @abstractmethod
    def list(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete(self, *args, **kwargs):
        ...
