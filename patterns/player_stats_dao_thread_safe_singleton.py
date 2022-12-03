from tinydb import TinyDB, Query

import threading


class PlayerStatsDao:
    __instance = None

    @staticmethod
    def get_instance():
        if PlayerStatsDao.__instance is None:
            with threading.Lock():
                if PlayerStatsDao.__instance is None:  # Double locking mechanism
                    PlayerStatsDao()
        return PlayerStatsDao.__instance

    def __init__(self):
        if PlayerStatsDao.__instance is not None:
            raise Exception("This is a singleton!")
        else:
            PlayerStatsDao.__instance = self
        self.db = TinyDB('../../data/player_stats.json')
        self.lock = threading.Lock()

    def add(self, stat):
        self.lock.acquire()

        player_stats = Query()
        if not self.db.contains(
                player_stats.Game == stat[0] and player_stats.Player == stat[2]):
            self.db.insert({'Game': stat[0], 'GameMode': stat[1], 'Player': stat[2], 'TotalScore': stat[3],
                            'LettersGuessed': stat[4]})
        else:
            self.db.update({'Game': stat[0], 'GameMode': stat[1], 'Player': stat[2], 'TotalScore': stat[3],
                            'LettersGuessed': stat[4]}, player_stats.Game == stat[0] and player_stats.Player == stat[2])
        ret = str(self.db.get(player_stats.Game == stat[0] and player_stats.Player == stat[2]))
        self.lock.release()
        return ret
