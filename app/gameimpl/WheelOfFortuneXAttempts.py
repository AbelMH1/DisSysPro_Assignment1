from app.templates.WordGameTemplate import WordGameTemplate
from patterns import Singleton


class WheelOfFortuneXAttempts(WordGameTemplate):

    def __init__(self, number_attempts):
        self.sentence = Singleton.SentencesIO.get_instance().getSentence()
        print(self.sentence)
        self.usedLetters = []
        self.guessedSentence = []
        self.points = 0
        self.gameFinished = False
        self.gameWined = False
        self.number_attempts = number_attempts
        for x in range(len(self.sentence)):
            if self.sentence[x] == " ":
                self.guessedSentence.append(True)
            else:
                self.guessedSentence.append(False)

    def processGuess(self, guess):
        if len(guess) == 1:
            self.__processLetter(guess)
        else:
            self.__processSentence(guess)

    def __processLetter(self, letter):
        if letter not in self.usedLetters:
            self.usedLetters.append(letter)
            timesLetterAppear = self.sentence.count(letter)
            if timesLetterAppear > 0:
                for i in range(len(self.sentence)):
                    if self.sentence[i] == letter:
                        self.guessedSentence[i] = True
                        self.points += 10
            else:
                self.number_attempts -= 1
                self.points -= 10
            self.__checkFinishCondition()

    def __checkFinishCondition(self):
        if self.number_attempts == 0:
            self.gameFinished = True
        for x in self.guessedSentence:
            if not x:
                return
        self.gameFinished = True
        self.gameWined = True

    def __processSentence(self, s):
        self.number_attempts -= 1
        if len(self.sentence) != len(s):
            self.points -= 50
            return
        for i in range(len(self.sentence)):
            if self.sentence[i] != s[i]:
                self.points -= 50
                return
        self.points += 25 * self.guessedSentence.count(False)
        self.gameFinished = True
        self.gameWined = True

    def getMessage(self):
        if self.gameFinished:
            if self.gameWined:
                m = self.sentence + "\nCongratulations!\nYou have guessed the sentence  :)"
            else:
                m = "Too bad, you exhausted all your attempts  :(\nThe answer was: " + self.sentence
            m += "\nPoints: " + str(self.points)
        else:
            m = self.getHiddenSentence() + "\nPoints: " + str(self.points) + "  Attempts left: "\
                + str(self.number_attempts)
        return m

    def getHiddenSentence(self):
        out = ""
        for i in range(0, len(self.sentence)):
            if self.guessedSentence[i]:
                out += self.sentence[i]
            else:
                out += "_"
        return out

    def getIntroMessage(self):
        return 'Wheel Of Fortune Attempts\n' \
               'Each guessed letter gives 10 points for each time it appears in the sentence.' \
               'If it is not in the sentence it discounts 10 points.\n' \
               'Solving the whole sentence gives 25 points for each hidden letter and discounts 50 if not correct.\n' \
               'You loose an attempt if you fail a letter or a sentence guess (repeated letters doesn\'t count)\n' \
               'Try to guess the sentence in less than {} attempts!\n{}'.format(self.number_attempts,
                                                                                self.getHiddenSentence())


class WheelOfFortuneXAttemptsBuilder:
    def __init__(self):
        pass

    def __call__(self, number_attempts=5):
        return WheelOfFortuneXAttempts(number_attempts)
