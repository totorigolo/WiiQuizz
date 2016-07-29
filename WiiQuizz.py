# coding: utf8

from GamesMgr import GamesMgr

if __name__ == '__main__':
    # Création du gestionnaire de jeux
    gamesMgr = GamesMgr()
    gamesMgr.run()

    # try:
    #     # Création du gestionnaire de manettes
    #     stateMgr = StateMgr()
    #     stateMgr.run()
    # except:
    #     print "Erreur fatale inconnue."
