from abc import ABC, abstractmethod

class Object(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self, screen_surf) -> None:
        pass