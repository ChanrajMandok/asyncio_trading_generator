from typing import Callable


class Observable:
    """Represents a simple implementation of the observer pattern.

    This class allows observers to attach and detach. When notified,
    it informs all attached observers of the given value.
    """

    def __init__(self):
        """Initialize an empty list of observers."""
        
        self._observers = []


    def attach(self, 
               observer: Callable) -> None:
        """Attach an observer if it's not already attached.

        Args:
            observer (Callable): The observer to attach.
        """
        
        if observer not in self._observers:
            self._observers.append(observer)


    def detach(self, 
               observer: Callable) -> None:
        """Detach an observer if it's attached.

        Args:
            observer (Callable): The observer to detach.
        """
        
        if observer in self._observers:
            self._observers.remove(observer)


    async def notify(self, 
                     value) -> None:
        """Notify all attached observers with the given value.

        Args:
            value: The value to notify observers with.
        """
        
        for observer in self._observers:
            await observer(value)