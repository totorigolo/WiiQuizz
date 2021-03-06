# coding=utf-8

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

    def get_answer(self, choices, question=None, sub_text=None):
        page_label = self.win.go_to(self.win.new_page(question, WIN_WIDTH, WIN_HEIGHT, bg='white'))

        self.win.import_template('menu')

        if question is not None:
            self.win.edit_text('title_list_dialog', question)
        else:
            self.win.edit_text('title_list_dialog', " ")  # TODO: Permettre de supprimer des éléments des templates
        if sub_text is not None:
            self.win.edit_text('sub_title_list_dialog', sub_text)
        else:
            self.win.edit_text('sub_title_list_dialog', " ")

        self.win.new_menu(choices, label='menu_list_dialog')

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
