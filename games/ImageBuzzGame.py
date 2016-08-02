# coding=utf-8

from CompleteBuzzGame import CompleteBuzzGame


class ImageBuzzGame(CompleteBuzzGame):

    def __init__(self, buzzerMgr):
        CompleteBuzzGame.__init__(self, buzzerMgr, window_title='Image Buzz Game', images_path='prompt')
