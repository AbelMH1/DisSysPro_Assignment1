import json

import pika as pika

from app.templates.WordGameTemplate import WordGameTemplate
from datatype.enums import TypeGameMode


class WheelOfFortuneCooperative(WordGameTemplate):

    def __init__(self):
        super().__init__()
        self.pointsPlayers = [0, 0]
        self.turn = 0

        self.guessedSentence = [[], []]
        for x in range(len(self.sentence)):
            if self.sentence[x] == " ":
                self.guessedSentence[0].append(True)
                self.guessedSentence[1].append(True)
            else:
                self.guessedSentence[0].append(False)
                self.guessedSentence[1].append(False)

    def changeTurn(self):
        self.turn = (self.turn + 1) % 2

    def processGuess(self, guess):
        if len(guess) == 1:
            self.__processLetter(guess)
        else:
            self.__processSentence(guess)
        self.__checkFinishCondition()
        self.record_statistics(self.turn)

    def __processLetter(self, letter):
        if letter not in self.usedLetters:
            self.usedLetters.append(letter)
            timesLetterAppear = self.sentence.count(letter)
            if timesLetterAppear > 0:
                for i in range(len(self.sentence)):
                    if self.sentence[i] == letter:
                        self.guessedSentence[self.turn][i] = True
                        self.pointsPlayers[self.turn] += 10
            else:
                self.pointsPlayers[self.turn] -= 10

    def __processSentence(self, s):
        if len(self.sentence) != len(s):
            self.pointsPlayers[self.turn] -= 50
            return
        for i in range(len(self.sentence)):
            if self.sentence[i] != s[i]:
                self.pointsPlayers[self.turn] -= 50
                return
        unguesedLetters = 0
        otherPlayer = (self.turn + 1) % 2
        for i in range(len(self.sentence)):
            if not self.guessedSentence[otherPlayer][i] and not self.guessedSentence[self.turn][i]:
                self.guessedSentence[self.turn][i] = True
                unguesedLetters += 1
        self.pointsPlayers[self.turn] += 25 * unguesedLetters

    def __checkFinishCondition(self):
        for i in range(len(self.sentence)):
            if not self.guessedSentence[0][i] and not self.guessedSentence[1][i]:
                return
        self.gameFinished = True

    def getMessage(self):
        if self.gameFinished:
            m = self.sentence + "\nCongratulations!\nYou have guessed the sentence  :)"
        else:
            m = self.getHiddenSentence()
        return m + "\nPoints: " + str(self.pointsPlayers[self.turn])

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
        return TypeGameMode.MULTIPLAYERCREATE

    def checkTurn(self, user):
        return self.turn == user

    def checkGameID(self, gameID):
        return self.gameID == gameID

    def record_statistics(self, player_index):
        game_type = "Cooperative"
        lettersGuessed = []
        for i in range(len(self.sentence)):
            if self.guessedSentence[self.turn][i] and self.sentence[i] != ' ' and self.sentence[i] not in lettersGuessed:
                lettersGuessed.append(self.sentence[i])
        totalPoints = self.pointsPlayers[player_index]
        playerName = str(player_index) + "-" + self.players[player_index]
        message = [self.gameID, game_type, playerName, totalPoints, lettersGuessed]
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='player-stats')
        channel.basic_publish(exchange='',
                              routing_key='player-stats',
                              body=json.dumps(message))
        connection.close()


class WheelOfFortuneCooperativeBuilder:
    def __init__(self):
        pass

    def __call__(self):
        return WheelOfFortuneCooperative()
