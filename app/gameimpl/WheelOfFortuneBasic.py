import json

import pika

from app.templates.WordGameTemplate import WordGameTemplate
from datatype.enums import TypeGameMode
from patterns import Singleton


class WheelOfFortuneBasic(WordGameTemplate):

    def __init__(self):
        super().__init__()
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
        self.__checkFinishCondition()
        self.record_statistics()

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
                self.points -= 10

    def __processSentence(self, s):
        if len(self.sentence) != len(s):
            self.points -= 50
            return
        for i in range(len(self.sentence)):
            if self.sentence[i] != s[i]:
                self.points -= 50
                return
        self.points += 25 * self.guessedSentence.count(False)
        for i in range(len(self.sentence)):
            self.guessedSentence[i] = True

    def __checkFinishCondition(self):
        for x in self.guessedSentence:
            if not x:
                return
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
            if self.guessedSentence[i]:
                out += self.sentence[i]
            else:
                out += "_"
        return out

    def getIntroMessage(self):
        return 'Wheel Of Fortune Basic\n' \
               'Each guessed letter gives 10 points for each time it appears in the sentence.' \
               'If it is not in the sentence it discounts 10 points.\n' \
               'Solving the whole sentence gives 25 points for each hidden letter and discounts 50 if not correct.\n' \
               'Try to guess the sentence!\n%s' % self.getHiddenSentence()

    def getTypeGame(self):
        return TypeGameMode.SINGLEPLAYER

    def record_statistics(self):
        game_type = "Basic"
        lettersGuessed = []
        for i in range(len(self.sentence)):
            if self.guessedSentence[i] and self.sentence[i] != ' ' and self.sentence[i] not in lettersGuessed:
                lettersGuessed.append(self.sentence[i])
        totalPoints = self.points
        playerName = self.players[0]
        message = [self.gameID, game_type, playerName, totalPoints, lettersGuessed]
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='player-stats')
        channel.basic_publish(exchange='',
                              routing_key='player-stats',
                              body=json.dumps(message))
        connection.close()


class WheelOfFortuneBasicBuilder:
    def __init__(self):
        pass

    def __call__(self):
        return WheelOfFortuneBasic()
