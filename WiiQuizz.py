# coding: utf8

"""
Credits:
OpenClipart-Vectors (https://pixabay.com/en/users/OpenClipart-Vectors-30363/)
"""

from BuzzerMgr import BuzzerMgr
from GamesMgr import GamesMgr


if __name__ == '__main__':

    try:
        # Connexion de la manette Master
        buzzerMgr = BuzzerMgr.Instance()
        buzzerMgr.connect_master()

        # Création du gestionnaire de jeux
        gamesMgr = GamesMgr()
        gamesMgr.run()
    except KeyboardInterrupt:
        print 'Application stoppée.'
