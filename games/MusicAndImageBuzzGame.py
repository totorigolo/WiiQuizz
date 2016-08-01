# coding=utf-8

from CompleteBuzzGame import CompleteBuzzGame


class MusicAndImageBuzzGame(CompleteBuzzGame):

    def __init__(self, buzzerMgr):
        CompleteBuzzGame.__init__(self, buzzerMgr, window_title='Blind Test', images_path='prompt', music_path='prompt')
