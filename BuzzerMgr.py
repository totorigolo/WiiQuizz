# coding=utf-8

import random
import time
import sys

import pygame
from pygame.locals import *

from Buzzer import Buzzer
from tools import py_encode_font_txt, py_encode_title

if not pygame.font: print 'Warning, fonts disabled'


# noinspection PyUnresolvedReferences
class BuzzerMgr:
    def __init__(self, nb_wiimote, need_master, dummy=False):
        """ Initialise les Wiimote dans une GUI """

        # TODO: S'arranger pour ne demander q''une seule fois la connexion des manettes durant une session

        # Nombre de wiimotes
        if nb_wiimote == 'ask':
            nb_wiimote = BuzzerMgr.prompt_nb_wiimotes(need_master)

        # Initialisation des attributs
        self.buzzers = dict()
        self.nb_wiimote = nb_wiimote
        self.need_master = need_master
        self.dummy = dummy
        self.initialized = False

        # Constantes pour PyGame
        self.py_width = 800
        self.py_height = 600
        self.py_margin = 35
        self.py_border = 5
        self.py_color_txt = (50, 150, 250)
        self.py_color_border = (200, 200, 200)
        self.py_color_success = (52, 207, 52)
        self.py_color_bckg = (0, 0, 0)

        # Démarre PyGame
        pygame.init()
        pygame.display.set_caption(py_encode_title('Initialisation des Buzzers'))
        self.py_screen = pygame.display.set_mode((self.py_width, self.py_height))

        # Images
        self.py_img_sync = pygame.image.load(sys.path[1] + '\\res\\sync_buzzer.jpg').convert()

        # Police de caractère (is watching you)
        self.font = pygame.font.SysFont('Arial', 35)

        # Boucle d'exécution
        running = True
        sub_state = -1
        init_state = 'aucun'
        current_buzzer = None
        texte_affiche = 'Chargement'
        transition_next = 0
        transition_percent = 0
        while running:
            # Evènements
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Gestion de la connexion
            if init_state == 'aucun':
                if self.need_master:
                    current_buzzer = Buzzer('master', dummy=self.dummy)
                    init_state = 'waiting_master'
                    current_buzzer.async_wait()
                    texte_affiche = 'Télécommande Master'
                else:
                    init_state = 10
            elif init_state == 'waiting_master':
                if current_buzzer.connected:
                    self.buzzers['master'] = current_buzzer
                    current_buzzer = None
                    init_state = 'transition'
                    transition_next = 1
                    transition_percent = 0
            elif isinstance(init_state, int):
                state_wii_nb = int(init_state / 10)
                sub_state = init_state - 10 * state_wii_nb
                if sub_state == 0:
                    texte_affiche = 'Télécommande {}'.format(state_wii_nb)
                    current_buzzer = Buzzer(state_wii_nb, dummy=self.dummy)
                    current_buzzer.async_wait()
                    init_state += 1
                elif sub_state == 1:
                    if current_buzzer.connected:
                        self.buzzers[state_wii_nb] = current_buzzer
                        current_buzzer = None
                        init_state = 'transition'
                        transition_next = state_wii_nb + 1
                        transition_percent = 0
                        sub_state = 2
            elif init_state == 'transition':
                transition_percent += transition_percent / 2 + 1
                if transition_percent >= 100:
                    if transition_next > self.nb_wiimote:
                        pygame.display.quit()
                        pygame.quit()
                        return
                    init_state = transition_next * 10
                    texte_affiche = ''

            # Affichage
            self.py_screen.fill(self.py_color_bckg)

            pygame.draw.rect(self.py_screen, self.py_color_border, pygame.Rect((self.py_margin, self.py_margin),
                                                                               (self.py_width - 2 * self.py_margin,
                                                                                self.py_height - 2 * self.py_margin)),
                             self.py_border)

            if init_state == 'transition':
                green_top = green_left = self.py_margin + self.py_border
                green_width = self.py_width - 2 * (self.py_margin + self.py_border)
                green_height = self.py_height - 2 * (self.py_margin + self.py_border)
                green_color = tuple(int(round(c * (100 - transition_percent) / 100.0)) for c in self.py_color_success)
                pygame.draw.rect(self.py_screen, green_color,
                                 pygame.Rect((green_top, green_left), (green_width, green_height)), 0)
            else:
                py_txt = self.font.render(py_encode_font_txt(texte_affiche), True, self.py_color_txt)
                txt_pos_x = (self.py_width - py_txt.get_rect().width) / 2
                self.py_screen.blit(py_txt, (txt_pos_x, 110))
                self.py_screen.blit(self.py_img_sync, (250, 250))

            pygame.display.flip()

            # Baisse les FPS
            time.sleep(1. / 25)

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

    @staticmethod
    def prompt_nb_wiimotes(need_master):
        if need_master:
            question = u"Combien de Wiimotes, dont master ? "
        else:
            question = u"A combien de Wiimotes voulez-vous jouer ? "

        from ListDialog import ListDialog
        dialog = ListDialog()
        return dialog.get_answer([i for i in range(5)], question)

