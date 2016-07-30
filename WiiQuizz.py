# coding: utf8

from GamesMgr import GamesMgr
import os


if __name__ == '__main__':

    try:
        # Création du gestionnaire de jeux
        gamesMgr = GamesMgr()
        gamesMgr.run()
    except KeyboardInterrupt:
        print 'Application stoppée.'
