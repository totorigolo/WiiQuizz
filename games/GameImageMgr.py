# coding: utf-8
import os

import pygame as pg

from ListDialog import ListDialog
from WindowHelper import WindowHelper
from tools import list_files


class GameImageMgr:
    """
    Gère les images
    """

    def __init__(self, dirname):
        if dirname == 'ask':
            dirname = GameImageMgr.prompt_image_folder()
        project_dir = os.path.abspath(
            '/'.join((os.path.dirname(os.path.abspath(__file__)), '..'))) + "/games/images/" + dirname
        self.files = list_files(project_dir)
        self.image_dir = project_dir + "/"
        self.question = 0
        self.version = 0
        self.current_img = self.files[self.question][self.version]
        self.win = WindowHelper.Instance()

        self.win.new_font('Arial', 20, 'page_info_game_img_mgr')
        self.is_paused = False
        self.printed = False

    @staticmethod
    def get_file_list(path):
        try:
            file_list = []
            for image in os.listdir(path):
                if os.path.isfile(os.path.join(path, image)):
                    file_list.append(image)
            return file_list
        except OSError:
            print 'Répertoire introuvable ({}) !'.format(path)
            return []

    @staticmethod
    def get_folder_list(path):
        try:
            folders = []
            for folder in os.listdir(os.path.abspath(path)):
                if not os.path.isfile(os.path.join(os.path.abspath(path), folder)):
                    folders.append(folder)
            return path, folders
        except OSError:
            print u"Aucun répertoire d'images trouvé !"
            return []

    @staticmethod
    def get_image_folders():
        return GameImageMgr.get_folder_list('./games/images/')

    # TODO: En faire un Dialog -> FolderDialog
    @staticmethod
    def prompt_image_folder():
        folder, folder_list = GameImageMgr.get_image_folders()
        dialog = ListDialog()
        # TODO: Gérer quand il n'y a aucun dossier
        choix = dialog.get_answer(folder_list + ['Annuler'], 'Sélectionnez un dossier :')
        if choix >= len(folder_list):
            return None
        return folder_list[choix]

    def get_current_file(self):
        """
        Renvoie l'image courante
        :return: lien de l'image courante
        """
        return self.image_dir + self.current_img

    def get_next_file(self):
        """
        Renvoie l'image de la catégorie suivant
        :return: lien de l'image suivante | False si pas d'image suivante
        """
        try:
            img = self.files[self.question + 1][0]
        except KeyError:
            return False
        return self.image_dir + img

    def get_prev_file(self):
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

    def process_event(self, event):
        """
        Gère les événements
        :type event: événement
        :return:
        """
        if event.type == pg.USEREVENT:
            if event.btn == 'DROITE':
                self.question += 1
                self.printed = False
            elif event.btn == 'GAUCHE':
                self.question -= 1
                self.printed = False
            elif event.btn == 'HAUT':
                self.version += 1
                self.printed = False
            elif event.btn == 'BAS':
                self.version -= 1
                self.printed = False

    def draw_on(self, page_label):
        if not self.is_paused and not self.printed:
            self.win.new_img(self.image_dir + self.files[self.question][self.version], label='game_img_mgr_image')  # Ajoute l'image
            self.win.new_text("Image : " + self.question + "/"+ len(self.files), 'page_info_game_img_mgr', 'black', label='game_img_mgr_num_page')  # Ajoute le numéro de page
            self.win.new_text("Version : " + self.version + "/"+ len(self.files[self.question]), 'page_info_game_img_mgr', 'black', label='game_img_mgr_num_version')  # Ajoute le numéro de version
            self.win.add('game_img_mgr_image', page=page_label)
            self.win.add('game_img_mgr_num_page', 50, 'bottom - 140', page=page_label)
            self.win.add('game_img_mgr_num_version', 50, 'bottom - 100', page=page_label)
            self.printed = True
        elif self.is_paused and self.printed:
            self.win.delete('game_img_mgr_image', page_label)
            self.printed = False

    def pause(self):
        """
        Est exécuté lorsque le jeu est mis en pause
        """
        self.id_paused = not self.is_paused
