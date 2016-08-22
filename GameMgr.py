# coding=utf-8


class GameMgr:
    """
    Cette classe s'occupe du déroulement d'un jeu. Elle cependant pas obligatoire à utiliser dans la création d'un
    nouveau jeu. Cependant, il est impératif que tout jeu comporte un constructeur et s'exécute dans une méthode
    run(); pour plus de détails, voir GamesMgr.
    C'est elle qui gère :
     - l'attente des buzzers
     - la suprématie du master
     ATTENTION : Ne pas confondre avec GamesMgr, qui gère le chargement DES jeux.
    """

    def __init__(self, game_content_mgr_list):
        """
        Initialise le GameMgr.
        Les gestionnaires de contenu vont afficher leur contenu dans le jeu.
        :type game_content_mgr_list: Une liste des gestionnaires de contenu
        """
        pass

    def run(self):
        """
        Exécution du jeu.
        """

        self.game_content_mgr_list = []
        # Le code après est ce que je pense de cette méthode :

        # blablabla

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
