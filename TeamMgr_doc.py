# coding=utf-8

from Singleton import Singleton


@Singleton
class TeamMgr:
    """
    Cette classe s'occupe de la gestion des équipes. C'est elle qui gère :
     - les scores
     - les pénalités ou bonus
     - les noms des équipes et leur couleur
     - l'affichage des scores
     - la joie à la victoire, et la déception à la défaite
    """

    def __init__(self):
        """
        Initialise le TeamMgr
        """
        # TODO: Déclarer les tableaux, etc
        # TODO: Pourquoi pas créer une classe Team aussi, si on veut plus tard s'amuser à mettre des pénalités et bonus ;)
        pass

    def draw_scores(self, page_label):
        """
        Affiche sur la page page_label les status des équipes.
        :param page_label: Page sur laquelle afficher les status
        :return:
        """
        pass

    def add_points(self, team, how_many):
        """
        Ajoute des points à l'équipe team. La méthode d'ajout varie suivant le mode de score, indiqué par how_many.
        Les modes de score disponibles sont :
          - 'add_only' : add=Ajout de 500 points, loose=Retrait de zéro point.
          - 'add_more' : add=Ajout de 500 points, loose=Retrait de 100 point.
          - 'equal' : add=Ajout de 500 points, loose=Retrait de 500 point.
          - 'hardcore' : add=Ajout de 100 points, loose=Retrait de 500 point.
        :param team: L'équipe à qui ajouter les points. Peut être 1 à 4.
        :param how_many: Peut être un int indiquant le nombre de points ou un mode de score.
        """
        pass

    def loose_points(self, team, how_many):
        """
        Retire des points à l'équipe team. La méthode de retrait varie suivant le mode de score (voir add_points),
        indiqué par how_many.
        :param team: L'équipe à qui ajouter les points. Peut être 1 à 4.
        :param how_many: Peut être un int indiquant le nombre de points ou un mode de score.
        """
        pass

    def get_best(self):
        """
        :return: Une liste contenant l'équipe actuellement en tête, potentiellement plusieurs équipes si ex-aequo. Les
        élèments de la liste peuvent être de 1 à 4.
        """
        pass

    def congratulate_winner(self):
        """
        Félicite l'équipe qui a gagné, sans oublier les autres.
        """
        pass
