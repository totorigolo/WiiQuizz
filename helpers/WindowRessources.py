# coding: utf8


"""
Class of the WindowHelper ressources
"""


class WindowRessources:
    def __init__(self, type):
        self.type = type

    def __del__(self):
        pass

    def __getitem__(self, item):
        return self.item

    def __setitem__(self, key, value):
        self.key = value

    def __delitem__(self, key):
        del self.key
