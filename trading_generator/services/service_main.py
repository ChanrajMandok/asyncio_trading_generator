import random
import asyncio

from typing import Optional

from trading_generator.services.trader import Trader
from trading_generator.services.strategy import Strategy
from trading_generator.services.generator import Generator


class ServiceMain:

    def __init__(self):
        self.strategies = []


    async def run(self,
                  n: Optional[int] = 5) -> None:
        
        """
        Creates and manages a series of generator and strategy objects for a trading simulation.
        
        This method simulates a trading environment by:
        1. Creating `n` generator objects that produce market data.
        2. Creating `n-1` strategy objects which each subscribe to a random selection of the generators.
        3. Creating a trader object that subscribes to all the strategies to aggregate their outputs.
        4. Every 30 seconds, one of the strategies is terminated .
        
        The implementation ensures that the destruction of one strategy or generator doesn't affect the others. 
        Even after a strategy is destroyed, the trader continues to function with the remaining strategies, 
        demonstrating the system's resilience and modularity.

        This design ensures that:
        - Generators and strategies are independent entities.
        - The system can dynamically adjust to the addition or removal of strategies.
        - The trader can consistently aggregate data from active strategies regardless of changes in their number.
        
        Args:
            n (Optional[int], default=10): The number of generator objects to be created in the simulation.
            
        Why this answers the question:
        By creating and subsequently destroying strategy objects independently, while keeping the trader operational, 
        this method demonstrates that new generator and strategy objects can be created and destroyed without 
        affecting the functioning of the other components.
        """
        
        generators = [Generator() for _ in range(n)]
        
        # Start all generators
        for generator in generators:
            generator.start()

        # Create n-1 strategies with a random selection of generators 
        for _ in range(n-1):
            selected_generators = random.sample(generators, random.randint(1, n))
            strategy = Strategy(*selected_generators)
            self.strategies.append(strategy)

        # Create and attach a trader to the strategies
        trader = Trader(*self.strategies)

        # Close a strategy every 2 minutes
        for strategy in list(self.strategies):  
            # wait for 30 seconds
            await asyncio.sleep(30)  
            # kill the strategy
            await self.kill_strategy(self.strategies.index(strategy)) 


    async def kill_strategy(self, 
                            strategy_index: int):
        """Kill a specific strategy based on its index.

        Args:
            strategy_index (int): The index of the strategy to be killed.
        """
        
        if strategy_index >= 0 and strategy_index < len(self.strategies):
            strategy_to_kill = self.strategies[strategy_index]

            # terminate strategy
            await strategy_to_kill.terminate(lambda: self.strategies)

            # Remove the strategy's decision from Trader
            trader_instance = Trader()  
            trader_instance.remove_strategy(strategy_to_kill)
            
            # Remove the strategy from the strategies list
            del self.strategies[strategy_index]

            # Print the number of strategies left
            remaining_strategies = len(self.strategies)
            print(f"{remaining_strategies} Strategies Remain.")
            
            # If no strategies are left, print a closing message
            if remaining_strategies == 0:
                print("No more strategies Service is closing.")