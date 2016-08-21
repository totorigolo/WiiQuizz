# coding=utf-8

from CompleteBuzzGame import CompleteBuzzGame


class MusicAndImageBuzzGame(CompleteBuzzGame):
    def __init__(self):
        CompleteBuzzGame.__init__(self, window_title='Blind Test', images_path='prompt', music_path='prompt')
