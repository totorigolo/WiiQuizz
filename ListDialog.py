# coding=utf-8

import random
from WindowHelper import WindowHelper


# noinspection PyUnresolvedReferences
class ListDialog:
    def __init__(self):
        # Liste
        self.list = None
        
        self.py_width = 800
        self.py_height = 600

        self.win = WindowHelper.Instance()

        # Démarre Fenêtre si pas ouverte
        if not self.win.is_open():
            self.win.open_window(self.py_width, self.py_height)

        # Texte
        self.question_txt = 'Sélectionnez une réponse :'
        

        # Constantes pour PyGame
        self.py_margin = 35
        self.py_border = 5
        self.py_question_height = 110
        self.py_list_elem_margin = 10

        # Couleurs
        self.win.new_color((165, 238, 255), 'question')
        self.win.new_color((99, 127, 255), 'list_elem')
        self.win.new_color((20, 20, 20), 'selected')
        self.win.new_color('white', 'selected_bckg')
        self.win.new_color((200, 200, 200), 'border')
        self.win.new_color('black', 'bckg')

        # Initialisations
        self.py_screen = None
        self.py_img_sync = None
        self.font = None
        self.font_title = None
        self.font_txt = None
        self.font_sous_txt = None

    def get_answer(self, list, question=None, sous_texte = None):
        self.list = list
        self.question_txt, self.sous_texte = None, None
        if question is not None:
            self.question_txt = question
        if sous_texte is not None:
            self.sous_texte = sous_texte

        # Préparation de la page
        # Nouvelle page
        label_page = self.win.new_page(self.question_txt)

        # Police de caractère (is watching you)
        self.win.new_font('Arial', 35, 'title')
        self.win.new_font('Arial', 25, 'txt')
        self.win.new_font('Arial', 20, 'sous_txt')
        

        self.win.new_rect('border', self.py_border, label='rect_border')
        self.win.add('rect_border',
                     [self.py_margin, self.py_width - 2 * self.py_margin],
                     [self.py_margin, self.py_height - 2 * self.py_margin],
                     label_page)

        txt_pos_y = self.py_question_height
        # Affichage du titre de la page
        if self.question_txt is not None:
            txt_pos_y = self.py_question_height
            self.win.new_text(self.question_txt, 'title', 'question', label='question_txt')
            self.win.add('question_txt', 'centered', txt_pos_y, label_page)
            text_height = self.win.get_element('question_txt')['obj'].get_rect().height # Hauteur du texte
            txt_pos_y += text_height
        # Affichage du sous titre
        if self.sous_texte is not None:
            self.win.new_text(self.sous_texte, 'sous_txt', 'question', label='sous_txt')
            self.win.add('sous_txt', 'centered', txt_pos_y, label_page)
            text_height = self.win.get_element('sous_txt')['obj'].get_rect().height
            txt_pos_y += text_height

        txt_pos_y += 20

        self.win.new_menu(self.list, label='menu')
        opt = {
            "font": "txt",
            "color": "question",
            "border": None,
            "color_active": "selected",
            "border_active": "selected_bckg",
            "font_active": "txt",
            "margin": 20
        }
        self.win.add_menu('menu', 'centered', txt_pos_y, opt=opt, page=label_page)
        self.win.go_to(label_page)
        return self.win.get_menu_result('menu') # récupération du résultat

    def button_pressed(self, which, btn):
        if which not in self.buzzers.keys() or self.buzzers[which].dummy:
            return False
        return self.buzzers[which].is_pressed(btn)

    def buzzers_which(self, btn):
        list_which = []
        for poop, b in self.buzzers.iteritems():
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