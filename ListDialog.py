# coding=utf-8

import random
import time

import pygame
from pygame.locals import *

from tools import py_encode_font_txt, py_encode_title

if not pygame.font: print 'Warning, fonts disabled'


# noinspection PyUnresolvedReferences
class ListDialog:
    def __init__(self):
        # Liste
        self.list = None

        # Texte
        self.question_txt = 'Sélectionnez une réponse :'

        # Constantes pour PyGame
        self.py_width = 800
        self.py_height = 600
        self.py_margin = 35
        self.py_border = 5
        self.py_question_height = 110
        self.py_list_elem_margin = 10
        self.py_color_question = (165, 238, 255)
        self.py_color_list_elem = (99, 127, 255)
        self.py_color_selected = (20, 20, 20)
        self.py_color_selected_bckg = (255, 255, 255)
        self.py_color_border = (200, 200, 200)
        self.py_color_bckg = (0, 0, 0)

        # Initialisations
        self.py_screen = None
        self.py_img_sync = None
        self.font = None
        self.font_title = None
        self.font_txt = None

    def get_answer(self, list, question=None, sous_texte = None):
        self.list = list
        self.question_txt, self.sous_texte = None, None
        if question is not None:
            self.question_txt = question
        if sous_texte is not None:
            self.sous_texte = sous_texte

        # Démarre PyGame
        pygame.init()
        pygame.display.set_caption(py_encode_title(self.question_txt))
        self.py_screen = pygame.display.set_mode((self.py_width, self.py_height))

        # Police de caractère (is watching you)
        self.font_title = pygame.font.SysFont('Arial', 35)
        self.font_txt = pygame.font.SysFont('Arial', 30)
        self.font_sous_txt = pygame.font.SysFont('Arial', 20)

        # Boucle d'exécution
        cursor = 0
        choice = None
        running = True
        while running:
            # Evènements
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        choice = cursor
                        running = False
                    if event.key == K_UP:
                        cursor -= 1
                    if event.key == K_DOWN:
                        cursor += 1
                    cursor %= len(list)

            # Affichage
            self.py_screen.fill(self.py_color_bckg)
            pygame.draw.rect(self.py_screen, self.py_color_border, pygame.Rect((self.py_margin, self.py_margin),
                                                                               (self.py_width - 2 * self.py_margin,
                                                                                self.py_height - 2 * self.py_margin)),
                             self.py_border)
                             
                             
            txt_pos_y = self.py_question_height
            
            if self.question_txt is not None:
                py_txt = self.font_title.render(py_encode_font_txt(self.question_txt), True, self.py_color_question)
                txt_pos_x = (self.py_width - py_txt.get_rect().width) / 2
                txt_pos_y = self.py_question_height
                self.py_screen.blit(py_txt, (txt_pos_x, txt_pos_y))
                txt_pos_y += py_txt.get_rect().height
                
            
            if self.sous_texte is not None:
                py_txt = self.font_sous_txt.render(py_encode_font_txt(self.sous_texte), True, self.py_color_question)
                txt_pos_x = (self.py_width - py_txt.get_rect().width) / 2
                txt_pos_y = self.py_question_height + 50
                self.py_screen.blit(py_txt, (txt_pos_x, txt_pos_y))
                txt_pos_y += py_txt.get_rect().height

            i = 0
            for str in self.list:
                if i != cursor:
                    py_txt = self.font_txt.render(py_encode_font_txt(str), True, self.py_color_question)
                else:
                    py_txt = self.font_txt.render(py_encode_font_txt(str), True, self.py_color_selected,
                                                  self.py_color_selected_bckg)
                txt_pos_x = (self.py_width - py_txt.get_rect().width) / 2
                txt_pos_y += py_txt.get_rect().height + self.py_list_elem_margin
                self.py_screen.blit(py_txt, (txt_pos_x, txt_pos_y))
                i += 1

            pygame.display.flip()

            # Baisse les FPS
            time.sleep(1. / 25)

        pygame.display.quit()
        pygame.quit()

        return choice

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
