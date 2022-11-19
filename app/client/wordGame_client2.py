
import logging
from time import sleep

import grpc
import wordgame_pb2
import wordgame_pb2_grpc
from datatype.enums import TypeGameMode


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = wordgame_pb2_grpc.WordGameStub(channel)

        response = stub.FirstConnection(wordgame_pb2.WelcomeRequest())
        print(response.message)

        response = stub.SelectMode(wordgame_pb2.ModeRequest(gameType=input().upper()))
        print(response.message)
        while response.typeMode == TypeGameMode.INVALID:
            response = stub.SelectMode(wordgame_pb2.ModeRequest(gameType=input().upper()))
            print(response.message)

        if response.typeMode == TypeGameMode.SINGLEPLAYER:
            runSinglePlayer(stub)
        if response.typeMode == TypeGameMode.MULTIPLAYER:
            runMultiPlayer(stub)


def runSinglePlayer(stub):
    gameFinished = False
    while not gameFinished:
        response = stub.GuessLetter(wordgame_pb2.LetterRequest(letter=askForLetter()))
        print(response.sentence)
        gameFinished = response.gameFinished


def runMultiPlayer(stub):
    gameFinished = False
    # while not gameFinished:
    #     response = stub.CheckTurn(wordgame_pb2.TurnRequest(user=1))
    #     while not response.isMyTurn:
    #         sleep(1)
    #         response = stub.CheckTurn(wordgame_pb2.TurnRequest(user=1))
    #     response = stub.CheckTeamMateAnswer(wordgame_pb2.WatchRequest())
    #     print(response.sentence)
    #     response = stub.GuessLetter(wordgame_pb2.LetterRequest(letter=askForLetter()))
    #     print(response.sentence)
    #     gameFinished = response.gameFinished


def askForLetter():
    letter = str.upper(input("Guess a Letter or introduce the full sentence to solve: "))
    while len(letter) < 1:
        letter = str.upper(input("You have to introduce at least 1 character: "))
    return letter


if __name__ == '__main__':
    logging.basicConfig()
    run()
