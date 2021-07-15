
# Connect4 AI
![pylint](https://github.com/technocrat13/Connect4Bot/actions/workflows/main.yml/badge.svg)
![pytest](https://github.com/technocrat13/Connect4Bot/actions/workflows/pytest.yml/badge.svg)


Python bot to play connect4, uses Q-Learning based on the Greedy Epsilon Bellman Equation 
## Installation

1. Unzip the latest version of `q_table_shelf.db (version)` and place in root
2. Install numpy
```bash
pip install numpy
```

## Usage
	
* To play a best of 3 against the AI:

	```bash
	python gameAIButBetter.py
	```
	The gameboard is  2D list and is represented in this form, positions to drop a `COIN` are from 1 to 7

* To train the model:
	```bash
	python train.py
	```
	By default this will train the model for 60000 episodes, the model in `q_table_shelf.db` has been trained for 200,000 episodes over 10 hours


## References

+ [An AI agent learns to play tic-tac-toe (part 3): training a Q-learning RL agent](https://towardsdatascience.com/an-ai-agent-learns-to-play-tic-tac-toe-part-3-training-a-q-learning-rl-agent-2871cef2faf0)
+ [Notebook for Topic 08 Video - Q-Learning - A Complete Example in Python.ipynb](https://colab.research.google.com/drive/1E2RViy7xmor0mhqskZV14_NUj2jMpJz3#scrollTo=Kq-QPfDnx4Fo)
