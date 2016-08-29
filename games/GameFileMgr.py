# coding: utf-8

import os

import pygame as pg

from ListDialog import ListDialog
from WindowHelper import WindowHelper
from tools import list_files


class GameFileMgr:
    """
    Gère les fichiers
    """

    def __init__(self, dirname):
        if dirname == 'ask':
            dirname = self.prompt_image_folder()
        project_dir = os.path.abspath(
            '/'.join((os.path.dirname(os.path.abspath(__file__)), '..'))) + dirname
        self.files = list_files(project_dir)

        self.image_dir = project_dir + "/"
        self.question = 0
        self.version = 0

        self.initialized = False
        if self.files is not None and  len(self.files) > 0 and len(self.files[0]) > 0:
            self.initialized = True

        self.win = WindowHelper.Instance()

        self.win.new_font('Arial', 20, 'page_info_game_img_mgr')
        self.is_paused = False

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
            print u"Aucun répertoire trouvé !"
            return []

    @staticmethod
    def get_image_folders():
        return GameFileMgr.get_folder_list('./games/images/')

    @staticmethod
    def get_sound_folders():
        return GameFileMgr.get_folder_list('./games/sounds/')

    @staticmethod
    def get_text_folders():
        return GameFileMgr.get_folder_list('./games/texts/')

    # TODO: En faire un Dialog -> FolderDialog
    @staticmethod
    def prompt_image_folder():
        folder, folder_list = GameFileMgr.get_image_folders()
        dialog = ListDialog()
        # TODO: Gérer quand il n'y a aucun dossier
        choix = dialog.get_answer(folder_list + ['Annuler'], 'Sélectionnez un dossier :')
        if choix >= len(folder_list):
            return ''
        return folder_list[choix]

    def next_file(self):
        self.question += 1
        self.version = 0

    def prev_file(self):
        self.question -= 1
        self.version = 0

    def next_version(self):
        self.version += 1

    def prev_version(self):
        self.version -= 1

    def process_event(self, event):
        """
        Gère les événements
        :type event: événement
        :return:
        """
        if self.initialized:
            return

        if event.type == pg.USEREVENT and event.wiimote_id == 'master':
            if event.btn == 'DROITE':
                self.next_file()
            elif event.btn == 'GAUCHE':
                self.prev_file()
            elif event.btn == 'HAUT':
                self.prev_version()
            elif event.btn == 'BAS':
                self.next_version()

    def draw_on(self, page_label):
        if self.initialized:
            return

    def pause(self, state):
        """
        Est exécuté lorsque le jeu est mis en pause
        """
        self.id_paused = state
