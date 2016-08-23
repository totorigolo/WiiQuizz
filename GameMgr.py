# coding=utf-8

from BuzzerMgr import BuzzerMgr
from TeamMgr import TeamMgr
from WindowHelper import WindowHelper


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

    def __init__(self, game_name='WiiQuizz', game_content_mgr_list=None):
        """
        Initialise le GameMgr.
        Les gestionnaires de contenu vont afficher leur contenu dans le jeu.
        :param game_name: object
        :param game_content_mgr_list: Une liste des gestionnaires de contenu. None pour n'en utiliser aucun et
        obtenir un jeu de buzzer simple.
        """
        self.game_name = game_name
        self.team_mgr = TeamMgr.Instance()
        self.win = WindowHelper.Instance()
        self.game_content_mgr_list = game_content_mgr_list
        self.page_label = 'page_game'

        if self.game_content_mgr_list is None:
            self.game_content_mgr_list = []

        # Connexion des manettes
        self.buzzer_mgr = BuzzerMgr.Instance()
        self.buzzer_mgr.require(2)

        # Gestion des équipes
        # TODO: il faudrait aussi une fonction require() pour TeamMgr
        # TODO: il faut refaire ça
        self.team_mgr.add_team(1, self.buzzer_mgr.buzzers[1], "Pastèque")
        self.team_mgr.add_team(2, self.buzzer_mgr.buzzers[2], "Ananas")

    def run(self):
        """
        Exécution du jeu.
        """
        # Ouvre une nouvelle page pour le jeu
        self.win.new_page(self.game_name, 960, 600, 'page_game', bg='white')
        self.win.dump_elements('page_game')
        self.win.go_to('page_game')

        # Variable accessibles dans les fonctions suivantes
        vars = {
            'pause': False,  # TODO
            'page_label': self.page_label,
            'team_mgr': self.team_mgr,
            'game_content_mgr_list': self.game_content_mgr_list,
            'self': self,
            "event_poster": BuzzerMgr.Instance()
        # TODO: En faire une fonction -> Afin de bénéficier des évènements wiimotes
        }

        def event_fun(pg, win, vars, event):
            """
                Appelé pour lister les événements
            """
            for cm in vars['game_content_mgr_list']:
                cm.add_events(event)
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:  # Event clavier
                return True
            if event.type == pg.USEREVENT and event.pressed:  # Event wiimote
                if event.wiimote_id == 'master':  # Gestion de la télécommande master
                    if not vars['pause'] and vars['team_mgr'].state == 'waiting_answer':  # Une équipe a buzzé
                        if event.btn == '+':
                            vars['team_mgr'].accept_buzz()
                        elif event.btn == '-':
                            vars['team_mgr'].refuse_buzz()
                        elif event.btn == 'A':
                            vars['team_mgr'].cancel_buzz()

                    elif not vars['pause'] and vars[
                        'team_mgr'].state == 'waiting_msg':  # Message de réponse juste ou fausse
                        vars['team_mgr'].skip_msg()

                    elif event.btn == 'B':  # B: Bascule la pause
                        vars['pause'] = not vars['pause']

                        # Affichage de la pause
                        if vars['pause']:
                            self.win.import_template('pause')
                        else:
                            self.win.delete('text_pause_img', vars['page_label'])
                            self.win.delete('bg_pause', vars['page_label'])
                            self.win.edit_color('bg_pause', 'white')

                        # Informe les GameSomeMgr
                        for cm in vars['game_content_mgr_list']:
                            cm.pause(vars['pause'])

                elif not vars['pause']:  # Gère le buzz des wiimotes
                    vars['team_mgr'].add_buzz(event.wiimote_id)

        def after_fun(pg, win, vars):
            """
                Appelé après les événements
            """
            # Gestion du buzz
            if vars['team_mgr'].awaiting_buzzes():
                vars['team_mgr'].pick_one_buzz()

            # Affichage des contenus
            for cm in vars['game_content_mgr_list']:
                cm.process_events()
                cm.draw_on(vars['page_label'])

            # Affichage des scores
            vars['team_mgr'].draw_on(vars['page_label'])

            # Affichage du masque de pause
            # TODO: Je sais pas comment faire : un masque noir foncé semi-transparent
            if vars['pause']:
                self.win.import_template('pause')

        self.win.event(event_fun=event_fun, after_fun=after_fun, vars=vars)

        # blablabla

        '''
        -> En gros, si on prend l'exemple de ImageContentMgr (le nom est pas top mais ça tu verras toi ;) ), c'est
        lui qui va afficher l'image actuelle, réagir au master pour afficher / cacher, afficher la position actuelle
        (4/12 par ex), etc... De même pour GameTextMgr, GameSoundMgr et GameQuestionMgr.
        '''

        pass
