import random
import asyncio

from trading_generator.observables.observable import Observable


class Generator(Observable):
    """Represents a generator in a trading environment.
    
    The generator is an observable object that continuously produces
    random values replicating a steam of market data. Observers can 
    attach to a generator to receive updates whenever a new value is produced.
    """

    def __init__(self):
        """Initialize the generator with an asyncio Event for stopping the task."""
        
        super().__init__()
        self._stop_signal = asyncio.Event()
        self._task: asyncio.Task = None


    async def run(self) -> None:
        """Continuously generate random values and notify observers.

        The method runs in an asynchronous loop, generating a random value
        every 60 seconds and notifying all attached observers. The loop 
        continues until an external signal stops it.
        """
        
        while not self._stop_signal.is_set():
            value = random.randint(1, 100)
            await self.notify((id(self), value))
            await asyncio.sleep(60)


    def start(self) -> None:
        """Start the generator by creating an asyncio Task to run it."""
        
        if self._task is None:
            self._task = asyncio.create_task(self.run())


    def stop(self) -> None:
        """Stop the generator by setting the stop signal and canceling the task."""
        
        if self._task:
            self._stop_signal.set()
            self._task.cancel()
            self._task = None
