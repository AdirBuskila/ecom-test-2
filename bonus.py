from abc import ABC, abstractmethod


class Animal(ABC):

    def __init__(self, legs: int):
        self._legs = legs

    @abstractmethod
    def walk(self):
        pass

    @abstractmethod
    def eat(self):
        pass


class Pet(ABC):

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def setName(self,name: str):
        pass

    @abstractmethod
    def play(self):
        pass
    
class Cat(Animal,Pet):
    
    def __init__(self, legs: int,name:str):
        super().__init__(legs)
        self._name = name
       
    def getName(self) -> str:
        return self._name 
        
    def setName(self,name: str):
        self._name = name
        
    def walk(self):
        print(f"The cat is walking with his {self._legs} legs")
        
    def play(self):
        print("The cat is playing.")
        
    def eat(self):
        print("The cat is eating.")
        
        
class Spider(Animal):
    def __init__(self, legs: int):
        super().__init__(legs)
        
    def eat(self):
        print("The spider is eating.")
        
class Fish(Animal,Pet):
    def __init__(self, legs: int,name:str):
        super().__init__(legs)
        self._name = name
       
    def getName(self) -> str:
        return self._name 
        
    def setName(self,name: str):
        self._name = name
        
    def walk(self):
        print(f"The fish is swimming with his flippers")
        
    def play(self):
        print("The fish is playing.")
        
    def eat(self):
        print("The fish is eating.")
