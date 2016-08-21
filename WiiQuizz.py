# coding: utf8

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
