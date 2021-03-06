# coding: utf8

"""
Credits:
OpenClipart-Vectors (https://pixabay.com/en/users/OpenClipart-Vectors-30363/)
"""

import os

try:
    import pygame_sdl2

    pygame_sdl2.import_as_pygame()
    import pygame

    print "pygame_SDL2 a été trouvé et sera utilisé à la place de pygame -> SDL %d.%d.%d" % pygame_sdl2.get_sdl_version()
except ImportError:
    import pygame

    print "pygame_SDL2 n'a pas été trouvé -> SDL %d.%d.%d" % pygame.get_sdl_version()

from WindowHelper import WindowHelper
from BuzzerMgr import BuzzerMgr
from GamesMgr import GamesMgr


if __name__ == '__main__':

    try:
        print "Bienvenue dans WiiQuizz !"
        print "Répertoire d'exécution :", os.getcwd()
        print

        # Connexion de la manette Master et enregistrement des buzzers à WindowHelper
        buzzerMgr = BuzzerMgr.Instance()
        buzzerMgr.set_dummy(False)
        buzzerMgr.connect_master()
        WindowHelper.Instance().register_event_poster(buzzerMgr)

        # Création du gestionnaire de jeux
        gamesMgr = GamesMgr()
        gamesMgr.run()
    except KeyboardInterrupt or SystemExit:  # Si l'application a été stoppée, on ignore l'exception
        print 'Application stoppée.'
    except Exception as e:  # Sinon, on affiche graphiquement l'erreur
        import sys, traceback, time

        print "L'erreur graphique correspond à la stacktrace suivante :"
        time.sleep(0.1)
        traceback.print_exception(*sys.exc_info())

        # noinspection PyBroadException
        try:
            from Dialog import Dialog
            from constants import WIN_HEIGHT, WIN_WIDTH

            WindowHelper.Instance().open_window(WIN_WIDTH, WIN_HEIGHT)
            dialog = Dialog.Instance()
            dialog.new_message('error', e)
        except KeyboardInterrupt or SystemExit:
            pass
        except:
            print "Impossible d'afficher l'erreur graphiquement."
