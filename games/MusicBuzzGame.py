# coding=utf-8

from GameMgr import GameMgr
from GameSoundMgr import GameSoundMgr


class MusicBuzzGame(GameMgr):
    def __init__(self):
        GameMgr.__init__(self, game_name='Image Buzz Game', game_content_mgr_classes=[GameSoundMgr])
