# coding=utf-8

import importlib

from BuzzerMgr import BuzzerMgr
from Dialog import Dialog
from ListDialog import ListDialog
from games import game_list


class GamesMgr:
    """
    TODO: Doc à réaliser. cf GameMgr qui dit : "pour plus de détails, voir GamesMgr."
    """
    def __init__(self):
        print 'Recherche de jeux...',
        self.games = []
        for name, file in game_list.iteritems():
            self.games.append((name, file))
        print '%d jeux trouvés.' % len(self.games)

        # Buzzers
        self.buzzerMgr = BuzzerMgr.Instance()

    def run(self):
        while True:
            dialog = ListDialog()
            choix = dialog.get_answer([g[0] for g in self.games] + [['Quitter', 'close']],
                                      'Quel jeu désirez-vous lancer ?', None)
            choix = (choix + 1) % (len(self.games) + 1)  # Quitter correspond au choix 0
            if choix == 0:
                break

            print ('Chargement du jeu %s...' % self.games[choix - 1][0]),
            game_module = importlib.import_module('games.{}'.format(self.games[choix - 1][1]))
            game_class = getattr(game_module, game_module.__name__.split('.')[1])
            print 'jeu chargé !'

            try:
                game = game_class()
                game.run()
            except Exception as e:
                import sys, traceback, time
                traceback.print_exception(*sys.exc_info())

                dialog = Dialog.Instance()
                dialog.new_message('error', e)
