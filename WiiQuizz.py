# coding: utf8

"""
Credits:
OpenClipart-Vectors (https://pixabay.com/en/users/OpenClipart-Vectors-30363/)
"""

from GamesMgr import GamesMgr
import os


if __name__ == '__main__':

    try:
        # Création du gestionnaire de jeux
        gamesMgr = GamesMgr()
        gamesMgr.run()
    except KeyboardInterrupt:
        print 'Application stoppée.'
