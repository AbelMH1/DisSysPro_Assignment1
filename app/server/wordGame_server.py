from concurrent import futures
import logging

import grpc
import wordgame_pb2
import wordgame_pb2_grpc
from app.gameimpl import WheelOfFortuneBasic, WheelOfFortuneXAttempts, WheelOfFortuneCooperative
from datatype.enums import TypeGameMode
from patterns import WordGameFactory


class WordGame(wordgame_pb2_grpc.WordGameServicer):

    def __init__(self):
        self.game = None
        self.factory = WordGameFactory.WordGameFactory()
        self.factory.register_builder('WOFBASIC', WheelOfFortuneBasic.WheelOfFortuneBasicBuilder())
        self.factory.register_builder('WOFATTEMPTS', WheelOfFortuneXAttempts.WheelOfFortuneXAttemptsBuilder())
        self.factory.register_builder('WOFCOOP', WheelOfFortuneCooperative.WheelOfFortuneCooperativeBuilder())

    def FirstConnection(self, request, context):
        return wordgame_pb2.WelcomeReply(message='Welcome to WordGame! Choose the game mode you want to play from '
                                                 + 'the following ones: ' + self.factory.enumerateBuilders()
                                                 + '\nGame mode: ')

    def SelectMode(self, request, context):
        if self.factory.isBuilderRegistered(request.gameType):
            if self.game is not None and not self.game.gameFinished:
                if self.factory.create(request.gameType).getTypeGame() == TypeGameMode.MULTIPLAYERCREATE \
                        and self.game.getTypeGame() == TypeGameMode.MULTIPLAYERCREATE:
                    return wordgame_pb2.ModeReply(message=self.game.getIntroMessage(), typeMode=TypeGameMode.MULTIPLAYERJOIN)
                return wordgame_pb2.ModeReply(message='A game is already in progress, wait a moment and then try again'
                                                      ' choosing one of the modes available.\nGame modes available: '
                                              + self.factory.enumerateBuilders() + '\nGame mode: ',
                                              typeMode=TypeGameMode.INVALID)
            self.game = self.factory.create(request.gameType)
            return wordgame_pb2.ModeReply(message=self.game.getIntroMessage(), typeMode=self.game.getTypeGame())
        return wordgame_pb2.ModeReply(message='Choose one of the modes available!\nGame modes available: '
                                              + self.factory.enumerateBuilders() + '\nGame mode: ',
                                      typeMode=TypeGameMode.INVALID)

    def GuessLetter(self, request, context):
        self.game.processGuess(request.letter)
        return wordgame_pb2.LetterReply(sentence=self.game.getMessage(), gameFinished=self.game.gameFinished)

    def CheckTurn(self, request, context):
        return wordgame_pb2.TurnReply(isMyTurn=self.game.checkTurn(request.user))

    def CheckTeamMateAnswer(self, request, context):
        return wordgame_pb2.WatchReply(sentence=self.game.getHiddenSentence())

    def CheckGameID(self, request, context):
        return wordgame_pb2.CheckIDReply(correctID=self.game.checkGameID(request.gameID))


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wordgame_pb2_grpc.add_WordGameServicer_to_server(WordGame(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
