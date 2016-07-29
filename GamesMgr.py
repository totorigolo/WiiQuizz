# coding=utf-8

import importlib
import os.path
import sys

from tools import prompt_int


class GamesMgr:
    def __init__(self):
        scriptDir = os.path.abspath('./games/')
        self.games = []
        for file in os.listdir(scriptDir):
            if file[-3:] == ".py" and file != '__init__.py':
                sys.stdout.write('Chargement du jeu : {}...'.format(file))
                current = importlib.import_module('games.{}'.format(file.split('.')[0]))
                self.games.append(current)
                print ' chargé !'

    def run(self):
        while True:
            print 'Quel jeu désirez-vous lancer ? (0 pour Quitter)'
            self.list_games(True)

            choix = prompt_int(0, len(self.games))
            if choix == 0:
                break

            game_module = self.games[choix - 1]

            game_class = getattr(game_module, game_module.__name__.split('.')[1])
            game = game_class()
            game.run()

    def list_games(self, numbers=False):
        """ Cette fonction affiche les jeux chargés """
        print u'Jeux chargés :'
        i = 0
        for m in self.games:
            if numbers:
                print "   - {}. {}".format(i + 1, m.__name__.split('.')[1])
            else:
                print "   - {}".format(m.__name__)
