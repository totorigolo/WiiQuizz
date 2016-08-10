# coding=utf-8

import random
import time

import pygame
from pygame.locals import *

from windowsHelper import windowsHelper
from colorHelper import colorHelper

from tools import py_encode_font_txt, py_encode_title


# noinspection PyUnresolvedReferences
class ListDialog:
    def __init__(self):
        # Liste
        self.list = None
        
        self.py_width = 800
        self.py_height = 600
        
        # Démarre Fenètre
        self.window = windowsHelper.Instance()
        self.window.open(self.py_width, self.py_height, 'Initialisation des Buzzers')

        # Texte
        self.question_txt = 'Sélectionnez une réponse :'
        

        # Constantes pour PyGame
        self.py_margin = 35
        self.py_border = 5
        self.py_question_height = 110
        self.py_list_elem_margin = 10
        
        self.window.add_color('question', (165, 238, 255))
        self.window.add_color('list_elem', (99, 127, 255))
        self.window.add_color('selected', (20, 20, 20))
        self.window.add_color('selected_bckg', (255, 255, 255))
        self.window.add_color('border', (200, 200, 200))
        self.window.add_color('bckg', colorHelper('black'))

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

        # Initialise la fenêtre
        self.window.change_title(self.question_txt)
        # Met à jour la taille de la fenêtre
        self.window.change_properties(self.py_width, self.py_height)

        # Police de caractère (is watching you)
        self.window.add_font('Arial', 35, 'title')
        self.window.add_font('Arial', 25, 'txt')
        self.window.add_font('Arial', 20, 'sous_txt')
        

        self.window.add_rect("border",
                             self.py_margin,
                             self.py_margin,
                             self.py_width - 2 * self.py_margin,
                             self.py_height - 2 * self.py_margin,
                             self.py_border)

        txt_pos_y = self.py_question_height
        # Affichage du titre de la page
        if self.question_txt is not None:
            txt_pos_y = self.py_question_height
            text = self.window.add_text(self.question_txt, 'title', 'question', y=txt_pos_y, opt={'widthcentered':True})
            txt_pos_y += text.height
        # Affichage du sous titre
        if self.sous_texte is not None:
            text = self.window.add_text(self.sous_texte, 'sous_txt', 'question', y=txt_pos_y, opt={'widthcentered':True})
            txt_pos_y += text.height

        txt_pos_y += 20
         
        opt = {
            "font": "txt",
            "color": "question",
            "border": None,
            "colorActive": "selected",
            "borderActive": "selected_bckg",
            "fontActive": "txt",
            "widthcentered": True,
            "margin": 20
        }
        
        return self.window.add_menu(y= txt_pos_y, menu=self.list, opt=opt)

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
