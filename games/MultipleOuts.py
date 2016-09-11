# coding: utf-8

from random import shuffle

import pygame as pg

import FSDialog
from File import File
from tools import safe_modulo


class MultipleOuts(File):
    """
    Gère les questions à 4 réponses
    """

    def __init__(self, dirname):
        if dirname == 'ask':
            dirname = FSDialog.get_folder('./games/mult_outs/')
        dirname = "/games/mult_outs/" + dirname
        File.__init__(self, dirname)

        self.win.new_color('black')
        self.win.new_color((80, 100, 255), 'blue_options')

        self.once = False
        self.showing = False
        self.is_paused = False

        self.question_text = ""
        self.answers = []
        self.good_answer_index = -1

        self.question_changed()

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
                self.showing = not self.showing
                self.__draw_questions()

    def __draw_questions(self):
        if self.showing:
            self.win.import_template('options_game')
            self.win.edit_text('question_text', self.question_text)
            self.win.edit_text('option_up_text', self.answers[0])
            self.win.edit_text('option_left_text', self.answers[1])
            self.win.edit_text('option_down_text', self.answers[2])
            self.win.edit_text('option_right_text', self.answers[3])
        else:
            self.win.undo_template('options_game')

    def next_file(self):
        File.next_file(self)
        self.question_changed()

    def prev_file(self):
        File.prev_file(self)
        self.question_changed()

    def next_version(self):
        File.next_version(self)
        self.question_changed()

    def prev_version(self):
        File.prev_version(self)
        self.question_changed()

    def process_question(self, path):
        raw = [line.rstrip('\n') for line in open(path)]
        raw = [line for line in raw if len(line) > 0]

        random = False
        time_shown = None
        self.question_text = ""
        self.answers = []
        self.good_answer_index = -1

        for line in raw:
            if line[0] == "@":
                if line.find("RandomOrder") != -1:
                    random = True
                elif line.find("TimeShown") != -1:
                    time_shown = int(line[13:])
                    print "Time shown ignored."
                else:
                    print "Unknown option : %s" % line
            elif line[0] == "#":
                self.question_text = line[2:]
            elif line[0] == "*":
                self.good_answer_index = len(self.answers)
                self.answers.append(line[1:])
            else:
                self.answers.append(line)

        if random:
            good_answer = self.answers[self.good_answer_index]
            shuffle(self.answers)
            i = 0
            for answer in self.answers:
                if answer == good_answer:
                    self.good_answer_index = i
                i += 1

    def question_changed(self):
        self.question = safe_modulo(self.question, len(self.files))
        self.version = safe_modulo(self.version, len(self.files[self.question]))

        # Chargement et préchargement
        self.process_question(self.files_dir + self.files[self.question][self.version])
        self.__draw_questions()

        self.win.new_text("Image : %d/%d" % (self.question + 1, len(self.files)), 'page_info_game_mgr',
                          'black', label='game_img_mgr_num_page', overwrite=True)  # Ajoute le numéro de page
        self.win.new_text("Version : %d/%d" % (self.version + 1, len(self.files[self.question])),
                          'page_info_game_mgr', 'black', label='game_img_mgr_num_version',
                          overwrite=True)  # Ajoute le numéro de version

        print 'question changed'

    def draw_on(self, page_label):
        if not self.once:
            self.win.add('game_sound_mgr_num_page', 50, 'bottom - 140', page=page_label)
            self.win.add('game_sound_mgr_num_version', 50, 'bottom - 100', page=page_label)
            self.once = True

    def pause(self, state, page_label):
        File.pause(self, state, page_label)
        if self.is_paused:
            self.showing = False
            self.win.undo_template('options_game')

    def on_quit(self, page_label):
        self.win.destroy('game_img_mgr_image', page_label)
