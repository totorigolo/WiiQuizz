# coding=utf-8

import random
from WindowHelper import WindowHelper
from constants import *

class ListDialog:
    def __init__(self):
        self.win = WindowHelper.Instance()

        self.win.new_color((5, 51, 90), 'dark_blue')
        self.win.new_color((176, 194, 238), 'light_blue')

        self.win.new_font('Arial', 40, 'title')
        self.win.new_font('Arial', 20, 'sub_title')
        self.win.new_font('Arial', 25, 'options')



    def get_answer(self, choices, question=None, sub_text = None):
        if question is None:
            question = ""
        if sub_text is None:
            sub_text = ""

        page_label = self.win.go_to(self.win.new_page(question, WIN_WIDTH, WIN_HEIGHT, bg='white'))

        self.win.new_text(question, 'title', 'dark_blue', label='title_list_dialog')
        self.win.new_text(sub_text, 'sub_title', 'dark_blue', label='sub_title_list_dialog')
        self.win.new_menu(choices, label='menu_list_dialog')

        self.win.import_template('menu')

        opt = {
            "font": "options",
            "color": "dark_blue",
            "border": None,
            "color_active": "dark_blue",
            "border_active": "light_blue",
            "font_active": "options",
            "margin": WIN_MARGIN
        }

        self.win.add_menu('menu_list_dialog', 'centered', 180, opt=opt, page=page_label)
        self.win.refresh()
        return self.win.get_menu_result('menu_list_dialog')

    def button_pressed(self, which, btn):
        if which not in self.buzzers.keys() or self.buzzers[which].dummy:
            return False
        return self.buzzers[which].is_pressed(btn)


    def buzzers_which(self, btn):
        list_which = []
        for _, b in self.buzzers.iteritems():
            if b.dummy:
                return []
            if b.is_pressed(btn):
                list_which.append(b)
        return list_which


    @staticmethod
    def any_of(buzzers):
        """ Sélectionne un buzzer au hasard, sauf avec master qui a la priorité """
        if len(buzzers) == 0:
            return None
        for b in buzzers:
            if b.team == 'master':
                return b
        return random.choice(buzzers)