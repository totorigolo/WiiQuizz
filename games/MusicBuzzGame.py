# coding=utf-8

from CompleteBuzzGame import CompleteBuzzGame


class MusicBuzzGame(CompleteBuzzGame):

    def __init__(self, buzzerMgr):
        CompleteBuzzGame.__init__(self, buzzerMgr, window_title='Blind Test', music_path='prompt')
