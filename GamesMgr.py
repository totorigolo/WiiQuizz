# coding=utf-8

import importlib
import sys

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

    def run(self):
        while True:
            dialog = ListDialog()
            choix = dialog.get_answer([g[0] for g in self.games] + ['Quitter'], 'Quel jeu désirez-vous lancer ?')
            choix = (choix + 1) % (len(self.games) + 1)
            if choix == 0:
                break

            game_module = self.games[choix - 1][1]

            game_class = getattr(game_module, game_module.__name__.split('.')[1])
            game = game_class()
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
