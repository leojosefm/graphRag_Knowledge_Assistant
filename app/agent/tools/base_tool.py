from abc import ABC, abstractmethod


#abstractmethod decorator marks the method that must be implemented in any subclass
#propery built in python funciton  - access like an attribute  a.description , a.name etc instead of a.name()

class BaseTool(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def execute(self, **kwargs):
        pass

    def close(self):
        pass