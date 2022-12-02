from abc import ABC, abstractmethod
import random

from patterns import Singleton


def generateGameCode():
    code = ""
    for i in range(5):
        code += str(random.randint(0, 9))
    return code


class WordGameTemplate(ABC):

    def __init__(self):
        self.sentence = Singleton.SentencesIO.get_instance().getSentence()
        self.usedLetters = []
        self.guessedSentence = []
        self.points = 0
        self.players = []
        self.gameID = generateGameCode()
        self.gameFinished = False

    @abstractmethod
    def processGuess(self, guess):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    @abstractmethod
    def getMessage(self):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    @abstractmethod
    def getHiddenSentence(self):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    @abstractmethod
    def getIntroMessage(self):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    @abstractmethod
    def getTypeGame(self):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    def changeTurn(self):
        pass

    def addPlayerName(self, name):
        self.players.append(name)
        return len(self.players)-1
