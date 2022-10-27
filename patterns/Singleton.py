import threading
from random import random, Random


class SentencesIO:
    __instance = None
    __sentences = None

    @staticmethod
    def get_instance():
        if SentencesIO.__instance is None:
            with threading.Lock():
                if SentencesIO.__instance is None:  # Double locking mechanism
                    SentencesIO()
        return SentencesIO.__instance

    def __init__(self):
        if SentencesIO.__instance is not None:
            raise Exception("This is a singleton!")
        else:
            SentencesIO.__instance = self
            SentencesIO.__sentences = []
        file = open("../../data/phrases.txt")
        lines = file.readlines()
        for line in lines:
            self.__sentences.append(line.upper().strip())
        # print(self.__sentences)
        self.rand = Random()

    def getSentence(self):
        sentenceNumber = self.rand.randint(0, len(self.__sentences)-1)
        return self.__sentences[sentenceNumber]
