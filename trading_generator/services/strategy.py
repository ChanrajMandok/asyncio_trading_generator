from typing import Callable

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
        self.generators = list(generators)
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
        
        generator_id, new_value = generator_info
        old_value = self.values.get(generator_id, None)
        
        # Update only if the value has changed
        if old_value != new_value:
            self.values[generator_id] = new_value
            decision = sum(self.values.values())
            await self.notify((self, decision))
            
            
    async def terminate(self, 
                        get_strategies: Callable[[], list['Strategy']]):
        """
        Terminate the strategy by detaching observers, stopping generators, and cleaning up.
        """
        
        print(f'Strategy {id(self)}, with {len(self.generators)} Generators is being terminated')
        
        # Detach all observers from this strategy
        for observer in list(self._observers):
            self.detach(observer)

        # Stop all generators that aren't in use by any other strategy
        all_strategies = get_strategies()
        for generator in self.generators:
            is_in_use = any(generator in strategy.generators for strategy in all_strategies if strategy != self)
            if not is_in_use:
                generator.stop()

        # Clear internal state
        self.values.clear()

        print(f"Strategy {id(self)} has been terminated.")