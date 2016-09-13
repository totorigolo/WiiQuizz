# coding=utf-8

import importlib

from BuzzerMgr import BuzzerMgr
from Dialog import Dialog
from GameMgr import GameMgr
from ListDialog import ListDialog
from games import game_list


class GamesMgr:
    """
    TODO: Doc à réaliser. cf GameMgr qui dit : "pour plus de détails, voir GamesMgr."
    """
    def __init__(self):
        print 'Recherche de jeux...',
        self.games = game_list[:]
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

            try:
                game_info = self.games[choix - 1]
                print game_info
                print ('Chargement du jeu %s...' % game_info[0])
                game_content_mgr_classes = []

                def load_addon(list, name):
                    module = importlib.import_module(name)
                    print 'Loading addon %s...' % name,
                    list.append(getattr(module, name))
                    print 'loaded !'

                if isinstance(game_info[1], str):
                    load_addon(game_content_mgr_classes, game_info[1])
                elif isinstance(game_info[1], list):
                    for addon in game_info[1]:
                        load_addon(game_content_mgr_classes, addon)

                print 'Creating The Game...'
                game_mgr = GameMgr(game_info[0], game_content_mgr_classes)
                print 'Game created, launching.'
                game_mgr.run()
                print 'Game terminated.'

            except Exception as e:
                import sys, traceback, time
                traceback.print_exception(*sys.exc_info())

                dialog = Dialog.Instance()
                dialog.new_message('error', e if len(e.message) > 0 else "Erreur")
