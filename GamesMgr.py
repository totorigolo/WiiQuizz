# coding=utf-8

import importlib

from BuzzerMgr import BuzzerMgr
from ListDialog import ListDialog
from games import game_list
from tools import print_noln


class GamesMgr:
    def __init__(self):
        print_noln('Recherche de jeux... ')
        self.games = []
        for name, file in game_list.iteritems():
            self.games.append((name, file))
        print '%d jeux trouvés.' % len(self.games)

        # Buzzers
        # TODO: Faire quelque chose du need_master qui est devenu inutile
        self.buzzerMgr = BuzzerMgr('ask', True, dummy=True)

    def run(self):
        while True:
            dialog = ListDialog()
            choix = dialog.get_answer([g[0] for g in self.games] + [['Quitter', 'close']],
                                      'Quel jeu désirez-vous lancer ?', None)
            choix = (choix + 1) % (len(self.games) + 1)  # Quitter correspond au choix 0
            if choix == 0:
                break

            print_noln('Chargement du jeu %s... ' % self.games[choix - 1][0])
            game_module = importlib.import_module('games.{}'.format(self.games[choix - 1][1]))
            game_class = getattr(game_module, game_module.__name__.split('.')[1])
            game = game_class(self.buzzerMgr)
            print 'jeu chargé !'

            game.run()
