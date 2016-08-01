# coding=utf-8

from CompleteBuzzGame import CompleteBuzzGame


class SimpleBuzzGame(CompleteBuzzGame):

    def __init__(self, buzzerMgr):
        CompleteBuzzGame.__init__(self, buzzerMgr, window_title='Simple Buzz Game')
