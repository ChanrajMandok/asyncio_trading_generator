from trading_generator.services.generator import Generator
from trading_generator.observables.observable import Observable


class Strategy(Observable):
    """Represents a strategy in a trading environment.
    
    The strategy is an observable object that aggregates values from 
    multiple generators. Observers can attach to a strategy to receive 
    updates whenever a new aggregated value (decision) is produced.
    """

    def __init__(self, 
                 *generators: Generator):
        """
        Initialize the strategy with a set of generators.
        """
        
        super().__init__()
        self.values = {id(generator): 0 for generator in generators}
        for generator in generators:
            generator.attach(self.update)
    

    async def update(self, 
                     generator_info:  tuple[int, int]) -> None:
        """Update the value from a specific generator and notify observers.
        
        Args:
            generator_info (tuple): Contains the ID of the generator and its 
                current value.
        """
        
        generator_id, value = generator_info
        self.values[generator_id] = value
        decision = sum(self.values.values())
        await self.notify(decision)