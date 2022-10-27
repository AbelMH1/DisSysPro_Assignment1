
import logging

import grpc
import wordgame_pb2
import wordgame_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = wordgame_pb2_grpc.WordGameStub(channel)

        response = stub.FirstConnection(wordgame_pb2.WelcomeRequest())
        print(response.message)

        response = stub.SelectMode(wordgame_pb2.ModeRequest(gameType=input().upper()))
        print(response.message)
        while not response.valid:
            response = stub.SelectMode(wordgame_pb2.ModeRequest(gameType=input().upper()))
            print(response.message)

        gameFinished = False
        while not gameFinished:
            response = stub.GuessLetter(wordgame_pb2.LetterRequest(letter=askForLetter()))
            print(response.sentence)
            gameFinished = response.gameFinished


def askForLetter():
    letter = str.upper(input("Guess a Letter or introduce the full sentence to solve: "))
    while len(letter) < 1:
        letter = str.upper(input("You have to introduce at least 1 character: "))
    return letter


if __name__ == '__main__':
    logging.basicConfig()
    run()
