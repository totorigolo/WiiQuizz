# coding: utf-8

import pygame as pg

import FSDialog
from File import File
from tools import safe_modulo


class Image(File):
    """
    Gère les images
    """

    def __init__(self, dirname):
        if dirname == 'ask':
            dirname = FSDialog.get_folder('./games/images/')
        dirname = "/games/images/" + dirname

        File.__init__(self, dirname)

        self.once = False
        self.showing = False
        self.is_paused = False
        self.image_changed()

    def next_file(self):
        File.next_file(self)
        self.image_changed()

    def prev_file(self):
        File.prev_file(self)
        self.image_changed()

    def next_version(self):
        File.next_version(self)
        self.image_changed()

    def prev_version(self):
        File.prev_version(self)
        self.image_changed()

    def image_changed(self):
        self.question = safe_modulo(self.question, len(self.files))
        self.version = safe_modulo(self.version, len(self.files[self.question]))

        # Chargement et préchargement
        self.win.new_img(self.files_dir + self.files[self.question][self.version], label='game_img_mgr_image',
                         overwrite=True)  # Ajoute l'image

        self.win.new_text("Image : " + str(self.question + 1) + "/" + str(len(self.files)), 'page_info_game_mgr',
                          'black', label='game_img_mgr_num_page', overwrite=True)  # Ajoute le numéro de page
        self.win.new_text("Version : " + str(self.version + 1) + "/" + str(len(self.files[self.question])),
                          'page_info_game_mgr', 'black', label='game_img_mgr_num_version',
                          overwrite=True)  # Ajoute le numéro de version

        print 'image changed'

    def process_event(self, event, page_label):
        """
        Gère les événements
        Cette méthode est appelé à chaque fois qu'un événement est détecté
        (touche clavier, bouton wiimote appuyé...)
        :param event: événement détecté
        :type event: événement
        """
        keyboard_pressed = keyboard_up = keyboard_down = keyboard_left = keyboard_right = keyboard_return = False
        if event.type == pg.KEYDOWN:
            keyboard_pressed = True
            event.btn = ""
            if event.key == pg.K_UP:
                keyboard_up = True
            elif event.key == pg.K_DOWN:
                keyboard_down = True
            elif event.key == pg.K_LEFT:
                keyboard_left = True
            elif event.key == pg.K_RIGHT:
                keyboard_right = True
            elif event.key == pg.K_RETURN:
                keyboard_return = True
            else:
                keyboard_pressed = False
        if event.type == pg.USEREVENT and event.wiimote_id == 'master' and event.pressed or keyboard_pressed:
            if keyboard_right or event.btn == 'DROITE':
                self.next_file()
            elif keyboard_left or event.btn == 'GAUCHE':
                self.prev_file()
            elif keyboard_up or event.btn == 'HAUT':
                self.prev_version()
            elif keyboard_down or event.btn == 'BAS':
                self.next_version()
            elif (keyboard_return or event.btn == '1') and not self.is_paused:
                self.showing = not self.showing
                if self.showing:
                    # Pour le z-index
                    self.win.remove('game_img_mgr_num_page', page=page_label)
                    self.win.remove('game_img_mgr_num_version', page=page_label)
                    self.win.add('game_img_mgr_image', page=page_label)
                    self.win.add('game_img_mgr_num_page', 50, 'bottom - 140', page=page_label)
                    self.win.add('game_img_mgr_num_version', 50, 'bottom - 100', page=page_label)
                else:
                    self.win.remove('game_img_mgr_image', page_label)

    def draw_on(self, page_label):
        """
        Affiche les éléments sur la page
        Appelé à chaque tour de boucle
        :param page_label:
        :return:
        """
        # Use the draw_on version of the parent
        File.draw_on(self, page_label)

        if not self.once:
            self.win.add('game_img_mgr_num_page', 50, 'bottom - 140', page=page_label)
            self.win.add('game_img_mgr_num_version', 50, 'bottom - 100', page=page_label)
            self.once = True

    def pause(self, state, page_label):
        File.pause(self, state, page_label)
        if self.is_paused:
            self.showing = False
            self.win.remove('game_img_mgr_image', page_label)

    def on_quit(self, page_label):
        self.win.destroy('game_img_mgr_image', page_label)
