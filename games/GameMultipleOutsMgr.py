# coding: utf-8

import pygame as pg
from GameFileMgr import GameFileMgr
from tools import safe_modulo


class GameMultipleOutsMgr(GameFileMgr):
    """
    Gère les images
    """
    def __init__(self, dirname):
        if dirname == 'ask':
            dirname = GameFileMgr.prompt_image_folder()
        dirname = "/games/mult_outs/" + dirname

        GameFileMgr.__init__(self, dirname)

    def process_event(self, event):
        GameFileMgr.process_event(self, event)

    def draw_on(self, page_label):
        GameFileMgr.draw_on(self, page_label)