# coding=utf-8

from GameMgr import GameMgr


class SimpleBuzzGame(GameMgr):
    def __init__(self):
        GameMgr.__init__(self, game_name='Simple Buzz Game')
