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

    def __init__(self, *strategies: Strategy):
        """
        Initialize the trader with a set of strategies to listen to.
        
        Args:
            *strategies (Strategy): A list of strategy objects.
        """
        
        # Store decisions {strategy_id: decision}
        self._decisions = {}
        for strategy in strategies:
            strategy.attach(self.update)

    async def update(self, 
                     update: tuple[Strategy, int]) -> None:
        """Receive a decision from a strategy and compute the median.
        
        Args:
            decision (int): The decision value from a strategy.
        """
        
        strategy, decision  = update
        strategy_id = id(strategy)
        self._decisions[strategy_id] = decision
        median_decision = statistics.median(self._decisions.values())
        self.print_decision(median_decision)


    @staticmethod
    def print_decision(decision: int) -> None:
        """Print the decision value."""
        print(f"Trader Median Decision: {decision}")
        
        
    def remove_strategy(self, 
                        strategy: Strategy) -> None:
        """Remove a strategy's decision from the decisions dictionary.
        
        Args:
            strategy (Strategy): The strategy object to be removed.
        """
        
        # remove terminated strat from median decision
        strategy_id = id(strategy)
        if strategy_id in self._decisions:
            del self._decisions[strategy_id]
            print(f"Strategy {strategy_id} removed from Trader decisions.")