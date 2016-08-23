# coding=utf-8

from GameImageMgr import GameImageMgr
from GameMgr import GameMgr


class TestNewGame(GameMgr):
    def __init__(self):
        GameMgr.__init__(self, game_name='Jeu de test', game_content_mgr_classes=[GameImageMgr])
        # GameMgr.__init__(self, game_name='Jeu de test')
