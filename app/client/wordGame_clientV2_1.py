
import logging
from time import sleep

import grpc
import wordgame_pb2
import wordgame_pb2_grpc
from datatype.enums import TypeGameMode

userid = 0


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
        else:
            runMultiPlayer(stub, response.typeMode)


def runSinglePlayer(stub):
    gameFinished = False
    while not gameFinished:
        response = stub.GuessLetter(wordgame_pb2.LetterRequest(letter=askForLetter()))
        print(response.sentence)
        gameFinished = response.gameFinished


def runMultiPlayer(stub, typeMode):
    if typeMode == TypeGameMode.MULTIPLAYERJOIN:
        if not askForGameID(stub):
            return
    else:  # typeMode == TypeGameMode.MULTIPLAYERCREATE:
        response = stub.GetMyGameCode(wordgame_pb2.GameCodeRequest())
        print("Share your Game Code with the other player: " + response.GameCode)
    gameFinished = False
    while not gameFinished:
        response = stub.CheckTurn(wordgame_pb2.TurnRequest(user=userid))
        if not response.isMyTurn:
            print("It is other player's turn...")
            while not response.isMyTurn:
                sleep(1)
                response = stub.CheckTurn(wordgame_pb2.TurnRequest(user=userid))
            response = stub.CheckTeamMateAnswer(wordgame_pb2.TeamMateAnswerRequest())
            if response.gameFinished:
                print(response.finalSentence)
                break
            print(response.sentence)
        print("Your turn!")
        response = stub.GuessLetter(wordgame_pb2.LetterRequest(letter=askForLetter()))
        print(response.sentence)
        gameFinished = response.gameFinished


def askForLetter():
    letter = str.upper(input("Guess a Letter or introduce the full sentence to solve: "))
    while len(letter) < 1:
        letter = str.upper(input("You have to introduce at least 1 character: "))
    return letter


def askForGameID(stub):
    correctID = False
    ID = ""
    while ID != "exit" and not correctID:
        ID = input("Introduce the current game ID or type \"exit\" to exit: ")
        if ID == "exit":
            return False
        correctID = stub.CheckGameID(wordgame_pb2.CheckIDRequest(gameID=ID)).correctID
        if not correctID:
            print("That game ID is not correct")
    return True


if __name__ == '__main__':
    logging.basicConfig()
    run()
