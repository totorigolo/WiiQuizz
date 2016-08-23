# coding: utf-8

from tools import list_files
import os


class GameImageMgr:
    """
    Gère les images
    """

    def __init__(self, dirname):
        project_dir = os.path.abspath('/'.join((os.path.dirname(os.path.abspath(__file__)), '..'))) + "/games/" + dirname
        self.files = list_files(project_dir)
        self.image_dir = project_dir + "/"
        self.question = 0
        self.version = 0
        self.current_img = self.files[self.question][self.version]

    def get_current_img(self):
        """
        Renvoie l'image courante
        :return: lien de l'image courante
        """
        return self.image_dir + self.current_img

    def get_next_img(self):
        """
        Renvoie l'image de la catégorie suivant
        :return: lien de l'image suivante | False si pas d'image suivante
        """
        try:
            img = self.files[self.question + 1][0]
        except KeyError:
            return False
        return self.image_dir + img

    def get_prev_img(self):
        """
        Renvoie l'image de la catégorie précédente
        :return: lien de l'image précédente | False si pas d'image suivante
        """
        try:
            img = self.files[self.question - 1][0]
        except KeyError:
            return False
        return self.image_dir + img

    def get_next_version(self):
        """
        Renvoie l'image de la version suivante
        :return: lien de la version suivante | False si pas d'image suivante
        """
        try:
            img = self.files[self.question][self.version + 1]
        except KeyError:
            return False
        return self.image_dir + img

    def get_prev_version(self):
        """
        Renvoie l'image de la version précédente
        :return: lien de la version précédente | False si pas d'image suivante
        """
        try:
            img = self.files[self.question][self.version - 1]
        except KeyError:
            return False
        return self.image_dir + img


    def pause(self):
        """
        Est exécuté lorsque le jeu est mis en pause
        """
        pass
