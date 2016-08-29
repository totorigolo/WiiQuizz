# coding: utf-8

import pygame as pg

from GameFileMgr import GameFileMgr
from tools import safe_modulo


class GameImageMgr(GameFileMgr):
    """
    Gère les images
    """

    def __init__(self, dirname):
        if dirname == 'ask':
            dirname = GameFileMgr.prompt_image_folder()
        dirname = "/games/images/" + dirname

        GameFileMgr.__init__(self, dirname)

        self.printed = False
        self.showing = False

    def next_file(self):
        GameFileMgr.next_file(self)
        self.image_changed()

    def prev_file(self):
        GameFileMgr.prev_file(self)
        self.image_changed()

    def next_version(self):
        GameFileMgr.next_version(self)
        self.image_changed()

    def prev_version(self):
        GameFileMgr.prev_version(self)
        self.image_changed()

    def image_changed(self):
        self.question = safe_modulo(self.question, len(self.files))
        self.version = safe_modulo(self.version, len(self.files[self.question]))
        self.printed = False

        # Chargement et préchargement
        # self.win.new_img(self.image_dir + self.files[self.question][self.version], label='game_img_mgr_image',
        #                  overwrite=True)  # Ajoute l'image
        # self.win.__preload_image(self.question, self.version)

    def __preload_image(self, question, version):
        """

        :param question: La question à précharger
        :param version: La version de la question à précharger
        :return:
        """
        try:
            self.win.preload_img(self.image_dir + self.files[self.question][self.version])  # Charge l'image l'image
            return True
        except AttributeError, NameError:
            print 'Préchagement pas encore implémenté (futur = RAII).'
        except KeyError:
            return False

    def process_event(self, event):
        """
        Gère les événements
        Cette méthode est appelé à chaque fois qu'un événement est détecté
        (touche clavier, bouton wiimote appuyé...)
        :param event: événement détecté
        :type event: événement
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
        """
        Affiche les éléments sur la page
        Appelé à chaque tour de boucle
        :param page_label:
        :return:
        """
        # Use the draw_on version of the parent
        GameFileMgr.draw_on(self, page_label)

        # if not self.is_paused and not self.printed and self.showing:
        if not self.is_paused and self.showing:
            self.win.new_img(self.image_dir + self.files[self.question][self.version], label='game_img_mgr_image',
                             overwrite=True)  # Ajoute l'image
            self.win.add('game_img_mgr_image', page=page_label)
            self.printed = True
        # elif not self.showing or self.id_paused:
        #     self.win.delete('game_img_mgr_image', page_label)
        #     self.printed = False

        self.win.new_text("Image : " + str(self.question + 1) + "/" + str(len(self.files)), 'page_info_game_mgr',
                          'black', label='game_img_mgr_num_page', overwrite=True)  # Ajoute le numéro de page
        self.win.new_text("Version : " + str(self.version + 1) + "/" + str(len(self.files[self.question])),
                          'page_info_game_mgr', 'black', label='game_img_mgr_num_version',
                          overwrite=True)  # Ajoute le numéro de version
        self.win.add('game_img_mgr_num_page', 50, 'bottom - 140', page=page_label)
        self.win.add('game_img_mgr_num_version', 50, 'bottom - 100', page=page_label)