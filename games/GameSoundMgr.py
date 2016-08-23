# coding: utf-8

from GameImageMgr import GameImageMgr
import pygame as pg

class GameSoundMgr(GameImageMgr):
    def __init__(self, dirname):
        GameImageMgr.__init__(self, dirname)
        self.is_playing = False

    def process_event(self, event):
        GameImageMgr.process_event(self, event)
        if event.type == pg.USEREVENT:
            if event.btn == '1':
                self.is_playing = not self.is_playing
                self.play()

    def play(self):
        """
        Si self.is_playing False lance le son, sinon l'arrête
        :return:
        """
        if self.is_playing:
            pass

    def draw_on(self, page_label):
        if not self.is_paused and not self.printed:
            self.win.new_sound(self.image_dir + self.files[self.question][self.version], label='game_sound_mgr_image')  # Ajoute l'image
            self.win.new_text("Image : " + self.question + "/"+ len(self.files), 'page_info_game_sound_mgr', 'black', label='game_sound_mgr_num_page')  # Ajoute le numéro de page
            self.win.new_text("Version : " + self.version + "/"+ len(self.files[self.question]), 'page_info_game_sound_mgr', 'black', label='game_sound_mgr_num_version')  # Ajoute le numéro de version
            self.win.add('game_sound_mgr_num_page', 50, 'bottom - 150', page=page_label)
            self.win.add('game_sound_mgr_num_version', 50, 'bottom - 100', page=page_label)
        elif self.is_paused and self.printed:
            self.printed = False