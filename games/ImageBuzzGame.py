# coding=utf-8

from GameImageMgr import GameImageMgr
from GameMgr import GameMgr


class ImageBuzzGame(GameMgr):
    def __init__(self):
        GameMgr.__init__(self, game_name='Image Buzz Game', game_content_mgr_classes=[GameImageMgr])
