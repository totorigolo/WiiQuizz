# coding=utf-8

import importlib
import sys

from BuzzerMgr import BuzzerMgr
from ListDialog import ListDialog
from games import game_list


class GamesMgr:
    def __init__(self):
        self.games = []
        for name, file in game_list.iteritems():
            sys.stdout.write('Chargement du jeu : {}...'.format(name))
            current = importlib.import_module('games.{}'.format(file))
            self.games.append((name, current))
            print ' chargé !'

        # Buzzers
        # TODO: Faire quelque chose du need_master qui est devenu inutile
        self.buzzerMgr = BuzzerMgr('ask', True, dummy=True)

    def run(self):
        while True:
            dialog = ListDialog()
            choix = dialog.get_answer([g[0] for g in self.games] + ['Quitter'], 'Quel jeu désirez-vous lancer ?', None)
            choix = (choix + 1) % (len(self.games) + 1) # Quitter correspond au choix 0
            if choix == 0:
                break
            


            game_module = self.games[choix - 1][1]

            game_class = getattr(game_module, game_module.__name__.split('.')[1])
            game = game_class(self.buzzerMgr)
            game.run()

    def list_games(self, numbers=False):
        """ Cette fonction affiche les jeux chargés """
        print 'Jeux chargés :'
        i = 0
        for m in self.games:
            if numbers:
                print "   - {}. {}".format(i + 1, m[0])
            else:
                print "   - {}".format(m[0])
            i += 1
