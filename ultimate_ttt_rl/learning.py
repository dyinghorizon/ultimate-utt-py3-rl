from ultimate_ttt_rl.board import GridStates, TTTBoardDecision
import json
import numpy as np

try:
    from keras.models import Sequential, load_model
    from keras.layers import Dense
    from keras.utils import plot_model
except ImportError:
    print("Keras not found. Neural network learning will not be available.")
    print("Install with: pip install keras tensorflow")


class GenericLearning(object):
    def getBoardStateValue(self, player, board, boardState):
        # Return the perceived `value` of a given board state
        raise NotImplementedError

    def learnFromMove(self, player, board, prevBoardState):
        # Learn from the previous board state and the current state of the board
        raise NotImplementedError

    def saveModel(self, filename):
        # Save to file (use pass if no implementation is necessary)
        # Useful for saving intermediate states of the learning model
        raise NotImplementedError

    def loadModel(self, filename):
        # Load an intermediate state of the learning model from file
        # Use only if also saving the intermediate state above
        raise NotImplementedError

    def resetForNewGame(self):
        pass

    def gameOver(self):
        pass


class TableLearning(GenericLearning):
    def __init__(self, DecisionClass=TTTBoardDecision):
        self.values = {}
        self.DecisionClass = DecisionClass

    def getBoardStateValue(self, player, board, boardState):
        decision = board.getBoardDecision()
        if decision == self.DecisionClass.WON_X:
            self.values[boardState] = 1.0 if player == GridStates.PLAYER_X else 0.0
        if decision == self.DecisionClass.WON_O:
            self.values[boardState] = 1.0 if player == GridStates.PLAYER_O else 0.0
        if decision == self.DecisionClass.DRAW or boardState not in self.values:
            self.values[boardState] = 0.5
        return self.values[boardState]

    def learnFromMove(self, player, board, prevBoardState):
        curBoardState = board.getBoardState()
        curBoardStateValue = self.getBoardStateValue(player, board, curBoardState)
        if prevBoardState not in self.values:
            self.getBoardStateValue(player, board, prevBoardState)
        self.values[prevBoardState] = self.values[prevBoardState] + 0.2*(curBoardStateValue - self.values[prevBoardState])

    def printValues(self):
        from pprint import pprint
        pprint(self.values)
        print('Total number of states: %s' % (len(self.values)))
        print('Total number of knowledgeable states: %s' % (len([x for x in self.values.values() if x!=0.5])))

    def saveLearning(self, filename):
        json.dump(self.values, open(filename, 'w'))

    def loadLearning(self, filename):
        self.values = json.load(open(filename, 'r'))


class NNUltimateLearning(GenericLearning):
    STATE_TO_NUMBER_MAP = {GridStates.EMPTY: 0, GridStates.PLAYER_O: -1, GridStates.PLAYER_X: 1}

    def __init__(self, DecisionClass=TTTBoardDecision):
        self.DecisionClass = DecisionClass
        self.values = {}
        try:
            self.initializeModel()
        except NameError:
            print("Keras not available. NNUltimateLearning will not work.")
            raise 

    def initializeModel(self):
        self.model = Sequential()
        self.model.add(Dense(81, input_dim=81, activation='relu'))
        #self.model.add(Dense(81, activation='relu'))
        self.model.add(Dense(1, activation='linear', kernel_initializer='glorot_uniform'))
        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        try:
            plot_model(self.model, to_file='model.png')
        except Exception as e:
            print(f"Could not plot model: {e}")

    def initialModelTraining(self, jsonFile):
        # If the neural network model should be seeded from some known state/value pairs
        import os
        if os.path.isfile(jsonFile):
            self.values = json.load(open(jsonFile, 'r'))
            self.gameOver()

    def resetForNewGame(self):
        self.values = {}

    def gameOver(self):
        boardStates, predYs = [], []
        for (k,v) in self.values.items():
            boardStates.append(self.convertBoardStateToInput(k))
            predYs.append(v)
        self.trainModel(boardStates, predYs)

    def convertBoardStateToInput(self, boardState):
        return [self.STATE_TO_NUMBER_MAP.get(x) for x in boardState]

    def trainModel(self, boardStates, y):
        self.model.fit(np.asarray(boardStates), np.asarray(y), verbose=0)

    def getPrediction(self, boardState):
        return self.model.predict(np.asarray([self.convertBoardStateToInput(boardState)]))

    def getBoardStateValue(self, player, board, boardState):  #TODO: Can batch the inputs to do several predictions at once
        decision = board.getBoardDecision()
        predY = self.getPrediction(boardState)[0]
        if decision == self.DecisionClass.WON_X:
            predY = 1.0 if player == GridStates.PLAYER_X else 0.0   #TODO: Explore using -1.0 instead of 0.0
            self.values[boardState] = predY
        if decision == self.DecisionClass.WON_O:
            predY = 1.0 if player == GridStates.PLAYER_O else 0.0
            self.values[boardState] = predY
        if decision == self.DecisionClass.DRAW:
            predY = 0.5
            self.values[boardState] = predY
        return predY

    def learnFromMove(self, player, board, prevBoardState):
        curBoardState = board.getBoardState()
        curBoardStateValue = self.getBoardStateValue(player, board, curBoardState)
        prevBoardStateValue = self.getPrediction(prevBoardState)[0]
        self.values[prevBoardState] = prevBoardStateValue + 0.2 * (curBoardStateValue - prevBoardStateValue)

    def printValues(self):
        pass

    def saveLearning(self, filename):
        self.model.save(filename)

    def loadLearning(self, filename):
        self.model = load_model(filename)
