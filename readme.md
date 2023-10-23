# **Geo Alpha** - Trading Generator Excersize 

## Setup trading_generator in VSC

|Action|Command
| :-| :-
|Create a virtual environment| python -m venv .venv
|Install relevant libraries | pip install -r requirements.txt|
|Create json launch file| Open and Paste contents of launch_items.txt (ensure commas are correct) and Save|
|Run|Select Dropdown Menu and Select Run main|


## Setup trading_generator (any)

|Action|Command
| :-| :-
|Create a virtual environment| python -m venv .venv
|Install relevant libraries | pip install -r requirements.txt|
|Run via Terminal|scripts -> script_run_main (via terminal)|


# Executive Summary

I set out to develop an infrastructure comprising of three primary components:

- **Generators**: Objects that produce a continuous stream of random numbers every minute [Emulating Websocket Stream of Data].

- **Strategies**: Objects that subscribe to one or multiple generators to compute a decision stream by summing the latest numbers from the subscribed generators.

- **Trader**: A unique object that listens to the decision outputs from all strategies, calculates the median of these decisions, and then prints the resulting values.

## Solution

My implementation revolves around a centralized design to maintain flexibility while ensuring robustness:

**ServiceMain showcases the ability to Launch and terminate generators and strategies**

- **Dynamic Creation & Destruction:** My system is designed such that we can instantiate any number of Generator and Strategy objects dynamically. The ServiceMain class serves as the demonstration centerpiece that validates My design's resilience. It automatically creates n generators, and then n-1 strategies each subscribing to a random selection of these generators. The Trader, being a singleton, listens to all these strategies.
- **Dynamic Creation & Destruction:** My system is designed such that it can instantiate any number of Generator and Strategy objects dynamically. The ServiceMain classautomatically creates n generators, and then n-1 strategies each subscribing to a random selection of these generators. The Trader then listens to all these strategies.

- **Observable Design Pattern:** The intercommunication between Generators, Strategies, and the Trader is achieved using the Observable pattern. Generators, as observables, notify their decisions to Strategies, which in turn, after processing, notify the Trader.

- **ServiceMain Showcase:** The ServiceMain class, in its run method, orchestrates the entire workflow. After initializing generators and strategies, it goes into a phase where, every 2 minutes, a strategy is deactivated. This method is demonstrative of the system's ability to dynamically destroy strategies without affecting the Trader's functionality. As strategies are taken down, the Trader continues to function with the remaining active strategies.

- **Resilience and Continuity:** When a strategy is deactivated (or "killed"), the Trader continues, computing the median from the decisions of the remaining strategies, ensuring uninterrupted functionality.
