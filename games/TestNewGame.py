# coding=utf-8

from GameMgr import GameMgr


class TestNewGame(GameMgr):
    def __init__(self):
        # GameMgr.__init__(self, game_name='Jeu de test', game_con_mgr=[ImageMgr, SoundMgr])
        GameMgr.__init__(self, game_name='Jeu de test')
