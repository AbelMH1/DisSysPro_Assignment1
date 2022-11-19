from app.templates.WordGameTemplate import WordGameTemplate
from datatype.enums import TypeGameMode
from patterns import Singleton


class WheelOfFortuneCooperative(WordGameTemplate):

    def __init__(self):
        self.sentence = Singleton.SentencesIO.get_instance().getSentence()
        print(self.sentence)
        self.usedLetters = []
        self.guessedSentence = [[], []]
        self.pointsPlayers = [0, 0]
        self.gameFinished = False
        self.turn = 0
        for x in range(len(self.sentence)):
            if self.sentence[x] == " ":
                self.guessedSentence[0].append(True)
                self.guessedSentence[1].append(True)
            else:
                self.guessedSentence[0].append(False)
                self.guessedSentence[1].append(False)

    def processGuess(self, guess, user):
        if user != self.turn:
            return
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
                self.__checkFinishCondition()
            else:
                self.points -= 10

    def __checkFinishCondition(self):
        for x in self.guessedSentence:
            if not x:
                return
        self.gameFinished = True

    def __processSentence(self, s):
        if len(self.sentence) != len(s):
            self.points -= 50
            return
        for i in range(len(self.sentence)):
            if self.sentence[i] != s[i]:
                self.points -= 50
                return
        self.points += 25 * self.guessedSentence.count(False)
        self.gameFinished = True

    def getMessage(self):
        if self.gameFinished:
            m = self.sentence + "\nCongratulations!\nYou have guessed the sentence  :)"
        else:
            m = self.getHiddenSentence()
        return m + "\nPoints: " + str(self.points)

    def getHiddenSentence(self):
        out = ""
        for i in range(0, len(self.sentence)):
            if self.guessedSentence[0][i] or self.guessedSentence[1][i]:
                out += self.sentence[i]
            else:
                out += "_"
        return out

    def getIntroMessage(self):
        return 'Wheel Of Fortune Cooperative\n' \
               'Each guessed letter gives 10 points for each time it appears in the sentence.' \
               'If it is not in the sentence it discounts 10 points.\n' \
               'Solving the whole sentence gives 25 points for each hidden letter and discounts 50 if not correct.\n' \
               'Try to guess the sentence with your partner!\n%s' % self.getHiddenSentence()

    def getTypeGame(self):
        return TypeGameMode.MULTIPLAYER


class WheelOfFortuneCooperativeBuilder:
    def __init__(self):
        pass

    def __call__(self):
        return WheelOfFortuneCooperative()
