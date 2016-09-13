# coding: utf-8

from random import shuffle

import pygame as pg

import FSDialog
from File import File
from TeamMgr import TeamMgr
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
        self.win.new_color((30, 255, 60), 'green_buzz')

        self.once = False
        self.showing = False
        self.is_paused = False

        self.question_text = ""
        self.answers = []
        self.good_answer_index = -1

        self.who_buzzed = None
        self.which_buzzed = None
        self.team_mgr = TeamMgr.Instance()
        self.team_mgr.set_buzz_fun(self.buzz_fun)

        self.question_changed()

    def process_event(self, event, page_label):
        File.process_event(self, event, page_label)

        if event.type == pg.USEREVENT and event.wiimote_id == 'master' and event.pressed:
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
                self.__draw_questions()

    def buzz_fun(self, id, btn_or_pts):
        if not self.showing:
            return

        if self.who_buzzed is None:
            self.which_buzzed = None
            if btn_or_pts == "HAUT":
                self.which_buzzed = "up"
                self.win.edit_color('option_up', 'green_buzz')
            elif btn_or_pts == "BAS":
                self.which_buzzed = "down"
                self.win.edit_color('option_down', 'green_buzz')
            elif btn_or_pts == "GAUCHE":
                self.which_buzzed = "left"
                self.win.edit_color('option_left', 'green_buzz')
            elif btn_or_pts == "DROITE":
                self.which_buzzed = "right"
                self.win.edit_color('option_right', 'green_buzz')
            if self.which_buzzed is not None:
                self.who_buzzed = id
                self.team_mgr.just_buzzed_now_waiting(self.who_buzzed, display=False)
        else:
            if id == 'accept' or id == 'refuse' or id == 'cancel':
                self.who_buzzed = False

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

        if not self.who_buzzed and self.who_buzzed is not None:
            self.win.edit_color('option_up', 'blue_options')
            self.win.edit_color('option_down', 'blue_options')
            self.win.edit_color('option_left', 'blue_options')
            self.win.edit_color('option_right', 'blue_options')
            self.who_buzzed = None
            self.which_buzzed = None

    def pause(self, state, page_label):
        File.pause(self, state, page_label)
        if self.is_paused:
            self.showing = False
            self.win.undo_template('options_game')

    def on_quit(self, page_label):
        self.team_mgr.set_buzz_fun(self.team_mgr.default_buzz)
