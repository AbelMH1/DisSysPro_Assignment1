from abc import ABC, abstractmethod


class WordGameTemplate(ABC):

    def __init__(self):
        self.sentence = None
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
