# coding: utf-8

from GameFileMgr import GameFileMgr
import pygame as pg
from tools import safe_modulo

class GameSoundMgr(GameFileMgr):
    def __init__(self, dirname):
        if dirname == 'ask':
            dirname = GameFileMgr.prompt_sound_folder()
        dirname = "/games/sounds/" + dirname
        GameFileMgr.__init__(self, dirname)

        self.is_playing = False

    def process_event(self, event):
        GameFileMgr.process_event(self, event)

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
        GameFileMgr.next_file(self)
        self.sound_changed()

    def prev_file(self):
        GameFileMgr.prev_file(self)
        self.sound_changed()

    def next_version(self):
        GameFileMgr.next_version(self)
        self.sound_changed()

    def prev_version(self):
        GameFileMgr.prev_version(self)
        self.sound_changed()

    def sound_changed(self):
        self.question = safe_modulo(self.question, len(self.files))
        self.version = safe_modulo(self.version, len(self.files[self.question]))
        self.is_playing = False

    def draw_on(self, page_label):
        if not self.is_paused and not self.is_playing :
            self.win.new_sound(self.image_dir + self.files[self.question][self.version], label='game_sound_mgr_son')  # Ajoute du son
            self.win.new_text("Son : " + str(self.question + 1) + "/" + str(len(self.files)),
                              'page_info_game_mgr',
                              'black', label='game_sound_mgr_num_page', overwrite=True)  # Ajoute le numéro de page
            self.win.new_text("Version : " + str(self.version + 1) + "/" + str(len(self.files[self.question])),
                              'page_info_game_mgr', 'black', label='game_sound_mgr_num_version',
                              overwrite=True)  # Ajoute le numéro de version
            self.win.add('game_sound_mgr_num_page', 50, 'bottom - 140', page=page_label)
            self.win.add('game_sound_mgr_num_version', 50, 'bottom - 100', page=page_label)
        elif self.is_paused and self.is_playing:
            self.is_playing = False