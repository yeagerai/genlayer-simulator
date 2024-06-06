from abc import ABC, abstractmethod


class IContract(ABC):
    @abstractmethod
    def __init__(self):
        """
        Constructor for the abstract class, which should be implemented by subclasses.
        Raises an exception if an attempt is made to instantiate the abstract class directly.
        """
        raise NotImplementedError(
            "Constructor (__init__) must be implemented by subclass"
        )
