# The Ultimate Tic Tac Toe Player Bot - with Reinforcement Learning

Reinforcement Learning based [Ultimate Tic Tac Toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe) player

## Background

This project provides an implementation of Ultimate Tic Tac Toe with reinforcement learning capabilities. It includes a simple table-based learning algorithm and a neural network-based learning algorithm.

Ultimate Tic Tac Toe is a complex version of the classic Tic Tac Toe game where each cell of the traditional 3x3 grid contains another 3x3 grid. To win, a player must win three small grids in a row.

This project is meant for others to test their learning algorithms on an existing infrastructure for the Ultimate Tic Tac Toe game.

## Installation

```bash
pip install ultimate-ttt-rl
```

Or you can install from source:

```bash
git clone https://github.com/yourname/ultimate-ttt-rl.git
cd ultimate-ttt-rl
pip install -e .
```

## Board

To instantiate and play a game of ultimate tic tac toe:

```python
from ultimate_ttt_rl.ultimateboard import UTTTBoard
from ultimate_ttt_rl.board import GridStates

b = UTTTBoard()
b.makeMove(GridStates.PLAYER_X, (1,1), (1,1))
b.makeMove(GridStates.PLAYER_O, b.getNextBoardLocation(), (1, 2))
b.makeMove(GridStates.PLAYER_X, b.getNextBoardLocation(), (1, 1))
```

The co-ordinate system is used for the master board, as well as any tile within it:

E.g. co-ordinates of `(1,1), (1,1)` as in the first move above represents the center square of the center tile.

To view the state of the board at any given time (you'll get a console output):

```python
b.printBoard()
```

## Players

There are two implemented bots for playing the game:
1. `RandomUTTTPlayer` who makes moves at random
2. `RLUTTTPlayer` who makes moves based on a user-supplied learning algorithm

To play the game with one or a combination of these bots, use the `SingleGame` class. E.g. with two random players:

```python
from ultimate_ttt_rl.game import SingleGame
from ultimate_ttt_rl.ultimateplayer import RandomUTTTPlayer
from ultimate_ttt_rl.ultimateboard import UTTTBoard, UTTTBoardDecision

player1, player2 = RandomUTTTPlayer(), RandomUTTTPlayer()
game = SingleGame(player1, player2, UTTTBoard, UTTTBoardDecision)
result = game.playAGame()
```

When using the RL player, it will need to be initialized with a learning algorithm of your choice. The package provides two sample learning algorithms: `TableLearning` and `NNUltimateLearning`

```python
from ultimate_ttt_rl.game import SingleGame
from ultimate_ttt_rl.learning import TableLearning
from ultimate_ttt_rl.ultimateplayer import RandomUTTTPlayer, RLUTTTPlayer
from ultimate_ttt_rl.ultimateboard import UTTTBoard, UTTTBoardDecision

player1, player2 = RLUTTTPlayer(TableLearning(UTTTBoardDecision)), RandomUTTTPlayer() 
game = SingleGame(player1, player2, UTTTBoard, UTTTBoardDecision)
result = game.playAGame()
```

## Learning Algorithm

The reinforcement learning (RL) player uses a learning algorithm to improve its chances of winning as it plays a number of games and learns about different positions. The learning algorithm is the key piece to the puzzle for making the RL bot improve its chances of winning over time.

There is a generic template provided for the learning algorithm:

```python
class GenericLearning(object):
    def getBoardStateValue(self, player, board, boardState):
        # Return the perceived `value` of a given board state
        raise NotImplementedError

    def learnFromMove(self, player, board, prevBoardState):
        # Learn from the previous board state and the current state of the board
        raise NotImplementedError
        
    def resetForNewGame(self):
        # Optional to implement. Reinitialize some form of state for each new game played
        pass
        
    def gameOver(self):
        # Option to implement. When a game is completed, run some sort of learning e.g. train a neural network
        pass
```

Any learning model must inherit from this class and implement the above methods. For examples see `TableLearning` for a lookup table based solution, and `NNUltimateLearning` for a neural network based solution.

Every *board state* is an 81-character string which represents a raster scan of the entire 9x9 board (row-wise). You can map this to numeric entries as necessary.

## Using your own learning algorithm

Simply implement your learning model by inheriting from `GenericLearning`. Then instantiate the provided reinforcement learning bot with an instance of this model:

```python
from ultimate_ttt_rl.ultimateboard import UTTTBoardDecision
from ultimate_ttt_rl.learning import GenericLearning
import random
from ultimate_ttt_rl.ultimateplayer import RLUTTTPlayer

class MyLearningModel(GenericLearning):
   def getBoardStateValue(self, player, board, boardState):
       # Your implementation here
       value = random.uniform(0, 1) # As an example (and a very poor one)
       return value   # Must be a numeric value
   
   def learnFromMove(self, player, board, prevBoardState):
       # Your implementation here - learn some value for the previousBoardState
       pass

learningModel = MyLearningModel(UTTTBoardDecision)
learningPlayer = RLUTTTPlayer(learningModel)
```

## Sequence of games

More often than not you will want to just play a sequence of games and observe the learning over time. Code samples for that have been provided and use the `GameSequence` class:

```python
from ultimate_ttt_rl.ultimateplayer import RLUTTTPlayer, RandomUTTTPlayer
from ultimate_ttt_rl.game import GameSequence
from ultimate_ttt_rl.ultimateboard import UTTTBoard, UTTTBoardDecision
from ultimate_ttt_rl.learning import TableLearning

learningPlayer = RLUTTTPlayer(TableLearning(UTTTBoardDecision))
randomPlayer = RandomUTTTPlayer()
results = []
numberOfSetsOfGames = 40
for i in range(numberOfSetsOfGames):
    games = GameSequence(100, learningPlayer, randomPlayer, BoardClass=UTTTBoard, BoardDecisionClass=UTTTBoardDecision)
    results.append(games.playGamesAndGetWinPercent())
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
