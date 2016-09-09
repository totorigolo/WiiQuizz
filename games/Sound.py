# coding: utf-8

import pygame as pg

from File import File
from tools import safe_modulo


class Sound(File):
    def __init__(self, dirname):
        if dirname == 'ask':
            dirname = File.prompt_sound_folder()
        dirname = "/games/sounds/" + dirname
        File.__init__(self, dirname)

        self.is_playing = False
        self.sound_changed()

        self.once = False

    def process_event(self, event, page_label):
        File.process_event(self, event, page_label)

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
            if event.btn == 'DROITE' or keyboard_right:
                self.next_file()
            elif event.btn == 'GAUCHE' or keyboard_left:
                self.prev_file()
            elif event.btn == 'HAUT' or keyboard_up:
                self.prev_version()
            elif event.btn == 'BAS' or keyboard_down:
                self.next_version()
            elif event.btn == '1' or keyboard_return:
                self.play()
                self.is_playing = not self.is_playing

    def play(self):
        """
        Si self.is_playing False lance le son, sinon l'arrête
        :return:
        """
        if self.is_playing:
            self.win.stop_sound('game_sound_mgr_son')
        else:
            self.win.play_sound('game_sound_mgr_son')

    def next_file(self):
        File.next_file(self)
        self.sound_changed()

    def prev_file(self):
        File.prev_file(self)
        self.sound_changed()

    def next_version(self):
        File.next_version(self)
        self.sound_changed()

    def prev_version(self):
        File.prev_version(self)
        self.sound_changed()

    def sound_changed(self):
        self.question = safe_modulo(self.question, len(self.files))
        self.version = safe_modulo(self.version, len(self.files[self.question]))
        self.win.new_sound(self.image_dir + self.files[self.question][self.version],
                           label='game_sound_mgr_son', overwrite=True)  # Charge le son
        self.is_playing = False

        self.win.new_text("Son : " + str(self.question + 1) + "/" + str(len(self.files)),
                          'page_info_game_mgr',
                          'black', label='game_sound_mgr_num_page', overwrite=True)  # Ajoute le numéro de page
        self.win.new_text("Version : " + str(self.version + 1) + "/" + str(len(self.files[self.question])),
                          'page_info_game_mgr', 'black', label='game_sound_mgr_num_version',
                          overwrite=True)  # Ajoute le numéro de version

    def draw_on(self, page_label):
        if not self.once:
            self.win.add('game_sound_mgr_num_page', 50, 'bottom - 140', page=page_label)
            self.win.add('game_sound_mgr_num_version', 50, 'bottom - 100', page=page_label)
            self.once = True

        if self.is_paused and self.is_playing:
            self.is_playing = False

    def on_quit(self, page_label):
        self.is_playing = False
        self.win.stop_sound('game_sound_mgr_son')
        print 'Sound stopped'
