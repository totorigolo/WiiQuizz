# coding: utf-8

import os

import pygame as pg

from WindowHelper import WindowHelper
from tools import list_files


class File:
    """
    Gère les fichiers
    """

    def __init__(self, dirname):
        project_dir = os.path.abspath(
            '/'.join((os.path.dirname(os.path.abspath(__file__)), '..'))) + dirname
        self.files = list_files(project_dir)

        self.files_dir = project_dir + "/"
        self.question = 0
        self.version = 0

        self.initialized = False
        if self.files is not None and len(self.files) > 0 and len(self.files[0]) > 0:
            self.initialized = True

        self.win = WindowHelper.Instance()

        self.win.new_font('Arial', 20, 'page_info_game_mgr')
        self.is_paused = False

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

    def process_event(self, event, page_label):
        """
        Gère les événements
        :type event: événement
        :return:
        """
        if self.initialized:
            return

        if event.type == pg.USEREVENT and event.wiimote_id == 'master' and event.pressed:
            if event.btn == 'DROITE':
                self.next_file()
            elif event.btn == 'GAUCHE':
                self.prev_file()
            elif event.btn == 'HAUT':
                self.prev_version()
            elif event.btn == 'BAS':
                self.next_version()

    def draw_on(self, page_label):
        pass

    def can_buzz(self):
        return True

    def pause(self, state, page_label):
        """
        Est exécuté lorsque le jeu est mis en pause
        """
        self.is_paused = state

    def on_quit(self, page_label):
        pass
