from abc import ABCMeta, abstractmethod
from .wrapper import KanbanizeSession


class GenericRequestMethod(metaclass=ABCMeta):

    endpoint = ''

    def __init__(self, service: KanbanizeSession, *args, **kwargs):
        self.service = service

    def insert(self, *args, **kwargs):
        ...

    def update(self, *args, **kwargs):
        ...

    def get(self, *args, **kwargs):
        ...

    def list(self, *args, **kwargs):
        ...

    def delete(self, *args, **kwargs):
        ...
