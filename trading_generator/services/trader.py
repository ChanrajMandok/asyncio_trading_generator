import statistics

from singleton_decorator import singleton

from trading_generator.services.strategy import Strategy

@singleton
class Trader:
    """Represents a trader in a trading environment.
    
    The trader subscribes to the decision output of every strategy, 
    takes the median across all strategies, and prints out the 
    stream of resulting values.
    """

    def __init__(self, 
                 *strategies: Strategy):
        """
        Initialize the trader with a set of strategies to listen to.
        
        Args:
            *strategies (Strategy): A list of strategy objects.
        """
        
        self._decisions = []
        for strategy in strategies:
            strategy.attach(self.update)


    async def update(self, 
                     decision: int) -> None:
        """Receive a decision from a strategy and compute the median.
        
        Args:
            decision (int): The decision value from a strategy.
        """
        
        self._decisions.append(decision)
        median_decision = statistics.median(self._decisions)
        self.print_decision(median_decision)


    @staticmethod
    def print_decision(decision: int)-> None:
        """Print the decision value."""
        print(f"Median Decision: {decision}")
