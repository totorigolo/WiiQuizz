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
        self.question = 0  # TODO: Quoi si pas de 0.0.jpg ?
        self.version = 0
        self.current_img = self.files[self.question][self.version]
        self.win = WindowHelper.Instance()

        self.win.new_font('Arial', 20, 'page_info_game_img_mgr')
        self.is_paused = False
        self.printed = False
        self.showing = False

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

    def next_file(self):
        self.question += 1
        self.question %= len(self.files)
        self.printed = False
        self.version = 0

    def prev_file(self):
        self.question -= 1
        self.question %= len(self.files)
        self.printed = False
        self.version = 0

    def next_version(self):
        self.version += 1
        self.version %= len(self.files[self.question])
        self.printed = False

    def prev_version(self):
        self.version -= 1
        self.version %= len(self.files[self.question])
        self.printed = False

    def process_event(self, event):
        """
        Gère les événements
        :type event: événement
        :return:
        """
        if event.type == pg.USEREVENT and event.wiimote_id == 'master':
            if event.btn == 'DROITE':
                self.next_file()
            elif event.btn == 'GAUCHE':
                self.prev_file()
            elif event.btn == 'HAUT':
                self.prev_version()
            elif event.btn == 'BAS':
                self.next_version()
            elif event.btn == '1':
                self.showing = not self.showing

    def draw_on(self, page_label):
        # if not self.is_paused and not self.printed and self.showing:
        if not self.is_paused and self.showing:
            self.win.new_img(self.image_dir + self.files[self.question][self.version], label='game_img_mgr_image',
                             overwrite=True)  # Ajoute l'image
            self.win.add('game_img_mgr_image', page=page_label)
            self.printed = True
        # elif not self.showing or self.id_paused:
        #     self.win.delete('game_img_mgr_image', page_label)
        #     self.printed = False

        self.win.new_text("Image : " + str(self.question + 1) + "/" + str(len(self.files)), 'page_info_game_img_mgr',
                          'black', label='game_img_mgr_num_page', overwrite=True)  # Ajoute le numéro de page
        self.win.new_text("Version : " + str(self.version + 1) + "/" + str(len(self.files[self.question])),
                          'page_info_game_img_mgr', 'black', label='game_img_mgr_num_version',
                          overwrite=True)  # Ajoute le numéro de version
        self.win.add('game_img_mgr_num_page', 50, 'bottom - 140', page=page_label)
        self.win.add('game_img_mgr_num_version', 50, 'bottom - 100', page=page_label)

    def pause(self, state):
        """
        Est exécuté lorsque le jeu est mis en pause
        """
        self.id_paused = state
