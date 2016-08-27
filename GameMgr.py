# coding=utf-8

from BuzzerMgr import BuzzerMgr
from TeamMgr import TeamMgr
from WindowHelper import WindowHelper
from constants import *


class GameMgr:
    """
    Cette classe s'occupe du déroulement d'un jeu. Elle est cependant pas obligatoire à utiliser dans la création d'un
    nouveau jeu. Cependant, il est impératif que tout jeu comporte un constructeur et s'exécute dans une méthode
    run(); pour plus de détails, voir GamesMgr.
    C'est elle qui gère :
     - l'attente des buzzers
     - la suprématie du master
     ATTENTION : Ne pas confondre avec GamesMgr, qui gère le chargement DES jeux.
    """

    def __init__(self, game_name='WiiQuizz', game_content_mgr_classes=None):
        """
        Initialise le GameMgr.
        Les gestionnaires de contenu vont afficher leur contenu dans le jeu.
        :param game_name: object
        :param game_content_mgr_classes: Une liste des gestionnaires de contenu. None pour n'en utiliser aucun et
        obtenir un jeu de buzzer simple.
        """
        self.game_name = game_name
        self.team_mgr = TeamMgr.Instance()
        self.win = WindowHelper.Instance()
        self.page_label = 'page_game'

        self.initialized = False

        # Charge les gestionnaires de contenu de jeu
        self.game_content_mgr_list = []
        if game_content_mgr_classes is not None:
            for cm_class in game_content_mgr_classes:
                cm_instance = cm_class('ask')
                self.game_content_mgr_list.append(cm_instance)
                if not cm_instance.initialized:
                    raise RuntimeError("Erreur lors du chargement du ContentMgr : %s" % str(cm_class).split('.')[-1])

        # Connexion des manettes
        self.buzzer_mgr = BuzzerMgr.Instance()
        self.buzzer_mgr.require('ask')

        # Gestion des équipes
        # TODO: il faudrait aussi une fonction require() pour TeamMgr, qui demande si différent nb de joueurs que faire des scores.
        # TODO: On pourrait ne pas conserver les scores entre les manches, mais retenir pour chaque équipe le nombre de fois où elle a terminé 1er, 2er...
        # TODO: il faut refaire ça
        for i in range(1, self.buzzer_mgr.get_nb_buzzers(False) + 1):
            self.team_mgr.add_team(i, self.buzzer_mgr.buzzers[i], TEAM_NAMES[i - 1])

        self.initialized = True

    def run(self):
        """
        Exécution du jeu.
        """
        if not self.initialized:
            print "Le jeu est mal initialisé."
            return

        # Ouvre une nouvelle page pour le jeu
        self.win.new_page(self.game_name, 960, 600, 'page_game', bg='white')
        self.win.dump_elements('page_game')
        self.win.go_to('page_game')

        # Variable accessibles dans les fonctions suivantes
        vars = {
            'pause': False,
            'page_label': self.page_label,
            'team_mgr': self.team_mgr,
            'game_content_mgr_list': self.game_content_mgr_list,
            'self': self
        }

        def before_fun(pg, win, vars):
            win.dump_elements(vars['page_label'])

        def event_fun(pg, win, vars, event):
            """
                Appelé pour lister les événements
            """
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:  # Event clavier
                return True
            elif event.type == pg.USEREVENT and event.pressed:  # Event wiimote
                if event.wiimote_id == 'master':  # Gestion de la télécommande master
                    if event.btn == 'HOME':
                        return True

                    elif not vars['pause'] and vars['team_mgr'].state == 'waiting_answer':  # Une équipe a buzzé
                        if event.btn == '+':
                            vars['team_mgr'].accept_buzz()
                        elif event.btn == '-':
                            vars['team_mgr'].refuse_buzz()
                        elif event.btn == 'A':
                            vars['team_mgr'].cancel_buzz()

                    # Message de réponse juste ou fausse : A pour passer
                    elif not vars['pause'] and vars['team_mgr'].state == 'waiting_msg' and event.btn == 'A':
                        vars['team_mgr'].skip_msg()

                    elif event.btn == 'B':  # B: Bascule la pause
                        vars['pause'] = not vars['pause']

                        # Informe les GameSomeMgr
                        for cm in vars['game_content_mgr_list']:
                            print 'pause changed'
                            cm.pause(vars['pause'])

                elif not vars['pause']:  # Gère le buzz des wiimotes
                    vars['team_mgr'].add_buzz(event.wiimote_id)

            else:  # Evènements non gérés
                for cm in vars['game_content_mgr_list']:
                    cm.process_event(event)

        def after_fun(pg, win, vars):
            """
                Appelé après les événements
            """
            # Gestion du buzz
            if vars['team_mgr'].awaiting_buzzes():
                vars['team_mgr'].pick_one_buzz()

            # Affichage des contenus
            for cm in vars['game_content_mgr_list']:
                cm.draw_on(vars['page_label'])

            # Affichage des scores
            vars['team_mgr'].draw_on(vars['page_label'])

            # Affichage de la pause
            if vars['pause']:
                self.win.import_template('pause')
            else:
                self.win.undo_template('pause')

            win.refresh()

        self.win.event(before_fun=before_fun, event_fun=event_fun, after_fun=after_fun, vars=vars, fps=60)
