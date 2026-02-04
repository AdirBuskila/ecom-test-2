from abc import ABC, abstractmethod

class Animal(ABC):
    
    @abstractmethod
    def walk():
        pass
    
    @abstractmethod
    def eat():
        pass
    