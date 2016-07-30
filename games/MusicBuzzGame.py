# coding=utf-8

from CompleteBuzzGame import CompleteBuzzGame


class MusicBuzzGame(CompleteBuzzGame):

    def __init__(self):
        CompleteBuzzGame.__init__(self, window_title='Blind Test', music_path='prompt')
