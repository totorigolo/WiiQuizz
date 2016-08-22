# coding=utf-8

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
        self.win = WindowHelper.Instance()
        self.game_content_mgr_list = game_content_mgr_list

    def run(self):
        """
        Exécution du jeu.
        """

        # Ouvre une nouvelle page pour le jeu
        self.win.new_page(self.game_name, 960, 600, 'page_game', bg='white')
        self.win.dump_elements('page_game')
        self.win.go_to('page_game')

        """
            Appelée pour lister les événements
        """

        def event_fun(pg, win, vars, event):
            for cm in self.game_content_mgr_list:
                cm.update_events(pg.event)
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:
                return True

        """
            Appelé après les événements
        """

        def after_fun(pg, win, vars):
            pass

        self.win.event(event_fun=event_fun, after_fun=after_fun, vars=vars)


        for cm in self.game_content_mgr_list:
            # cm.update_events(pg.event)  # commenté car sinon erreurs de code
            pass
        for cm in self.game_content_mgr_list:
            # cm.draw_on(win) OU cm.draw_on('page_label')  # idem
            pass

        # blablabla

        '''
        -> En gros, si on prend l'exemple de ImageContentMgr (le nom est pas top mais ça tu verras toi ;) ), c'est
        lui qui va afficher l'image actuelle, réagir au master pour afficher / cacher, afficher la position actuelle
        (4/12 par ex), etc... De même pour TextContentMgr, SoundContentMgr et QuestionContentMgr.
        '''

        pass
