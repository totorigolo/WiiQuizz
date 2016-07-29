# coding=utf-8

import sys
import time

import pygame
from pygame.locals import *
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from BuzzerMgr import BuzzerMgr

# Pour la complétion IDE
import cwiid
from Buzzer import Buzzer

# noinspection PyUnresolvedReferences
class SimpleBuzzGame():
    """ Jeu simple affichant uniquement l'équipe qui a buzzé, avec le contrôle d'un Master """

    def __init__(self):
        # Constantes du jeu
        self.default_text = 'Grenade Quizz'
        self.team_names = [
            'master',
            'Pastèque',
            'Ananas',
            'Abricot',
            'Poireau'
        ]
        self.score_win = 500
        self.score_loose = 100

        # Constantes pour PyGame
        self.py_width = 800
        self.py_height = 600
        self.py_margin = 35
        self.py_border = 5
        self.py_frame_top = self.py_frame_left = self.py_margin + self.py_border
        self.py_frame_width = self.py_width - 2 * (self.py_margin + self.py_border)
        self.py_frame_height = self.py_height - 2 * (self.py_margin + self.py_border)
        self.py_color_BLACK = (0, 0, 0)
        self.py_color_txt = (50, 150, 250)
        self.py_color_border = (200, 200, 200)
        self.py_color_waiting = (200, 200, 200)
        self.py_color_master = (60, 60, 60)
        self.py_color_team1 = (207, 52, 52)
        self.py_color_team2 = (207, 250, 30)
        self.py_color_team3 = (230, 150, 20)
        self.py_color_team4 = (30, 208, 20)

        # Déclarations
        self.py_screen = None
        self.py_snd_buzzer = None
        self.py_snd_win = None
        self.py_snd_loose = None
        self.font = None
        self.font_scores = None

        self.buzzerMgr = BuzzerMgr('ask', True, dummy=False)
        self.nb_buzzers = len(self.buzzerMgr.buzzers) - 1 # enlève le master

    def run(self):
        # Démarre PyGame
        pygame.init()
        pygame.display.set_caption('Buzzer simple')
        self.py_screen = pygame.display.set_mode((self.py_width, self.py_height), RESIZABLE)
        # TODO: A redimentionnement de la fenêtre, changer les variables pour ajuster la vue

        # Sons
        self.py_snd_buzzer = pygame.mixer.Sound("./res/buzzer.ogg")
        self.py_snd_win = pygame.mixer.Sound("./res/win.ogg")
        self.py_snd_loose = pygame.mixer.Sound("./res/loose.ogg")

        # Police de caractère (is watching you)
        self.font = pygame.font.SysFont('Arial', 35)
        self.font_scores = pygame.font.SysFont('Arial', 15)

        # Boucle d'exécution
        running = True
        color_bckg = self.py_color_BLACK
        texte_affiche = self.default_text
        state = 'waiting'
        rising_edge = False
        rising_edge_which = False
        rising_edge_btn = False
        scores = [0] * 4
        while running:
            # Evènements PyGame
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False

            # Evènements Wiimote
            new_edge, new_which, new_btn = False, None, None
            if rising_edge:
                if not self.buzzerMgr.button_pressed(rising_edge_which, rising_edge_btn):
                    rising_edge = False
            else:
                if state == 'waiting':
                    liste_any = self.buzzerMgr.buzzers_which('any')
                    buzzer_any = self.buzzerMgr.any_of(liste_any)
                    if buzzer_any is not None:
                        if buzzer_any.team == 'master':
                            state = 'blocked_'
                            new_edge = 'rising'
                            new_which, new_btn = 'master', 'any'
                        else:
                            self.py_snd_buzzer.play()
                            state = 'buzz_team_{}_'.format(buzzer_any.team)
                elif state[0:10] == 'buzz_team_':
                    current_team = int(state[-1])
                    master_plus = self.buzzerMgr.button_pressed('master', cwiid.BTN_PLUS)
                    master_minus = self.buzzerMgr.button_pressed('master', cwiid.BTN_MINUS)
                    if master_plus:
                        self.py_snd_win.play()
                        scores[current_team - 1] += self.score_win
                        state = 'win_team_{}_'.format(current_team)
                        new_edge = 'rising'
                        new_which, new_btn = 'master', 'any'
                    elif master_minus:
                        self.py_snd_loose.play()
                        scores[current_team - 1] -= self.score_loose
                        state = 'loose_team_{}_'.format(current_team)
                        new_edge = 'rising'
                        new_which, new_btn = 'master', 'any'
                elif state == 'blocked' or state[0:10] == 'buzz_team_':
                    master_any = self.buzzerMgr.button_pressed('master', 'any')
                    if master_any:
                        state = 'waiting_'
                        new_edge = 'rising'
                        new_which, new_btn = 'master', 'any'
            if new_edge == 'rising':
                rising_edge = True
                rising_edge_which, rising_edge_btn = new_which, new_btn

            # Gestion de l'état
            if state == 'waiting_':
                color_bckg = self.py_color_waiting
                texte_affiche = self.default_text
                state = state[:-1]
            elif state == 'blocked_':
                color_bckg = self.py_color_master
                texte_affiche = ''
                state = state[:-1]
            elif state[0:10] == 'buzz_team_' and state[-1] == '_':
                team = int(state[-2])
                color_bckg = getattr(self, 'py_color_team{}'.format(team))
                texte_affiche = self.team_names[team]
                state = state[:-1]
            elif state[0:9] == 'win_team_' and state[-1] == '_':
                team = int(state[-2])
                color_bckg = getattr(self, 'py_color_team{}'.format(team))
                texte_affiche = 'Gagné !'
                state = 'blocked'
            elif state[0:11] == 'loose_team_' and state[-1] == '_':
                team = int(state[-2])
                color_bckg = getattr(self, 'py_color_team{}'.format(team))
                texte_affiche = 'FAUX !'
                state = 'blocked'

            # Affichage
            self.py_screen.fill(self.py_color_BLACK)
            pygame.draw.rect(self.py_screen, self.py_color_border, pygame.Rect((self.py_margin, self.py_margin),
                                                                               (self.py_width - 2 * self.py_margin,
                                                                                self.py_height - 2 * self.py_margin)),
                             self.py_border)
            pygame.draw.rect(self.py_screen, color_bckg,
                             pygame.Rect((self.py_frame_top, self.py_frame_left),
                                         (self.py_frame_width, self.py_frame_height)), 0)
            py_txt = self.font.render(unicode(texte_affiche, 'utf-8'), True, self.py_color_txt)
            txt_pos_x = (self.py_width - py_txt.get_rect().width) / 2
            self.py_screen.blit(py_txt, (txt_pos_x, 110))

            if self.nb_buzzers >= 1:
                self.py_screen.blit(self.font_scores.render(unicode('{} : {}'.format(self.team_names[1], scores[0]), 'utf-8'), True, self.py_color_team1), (10, 10))
            if self.nb_buzzers >= 2:
                score_2_txt = self.font_scores.render(unicode('{} : {}'.format(self.team_names[2], scores[1]), 'utf-8'), True, self.py_color_team2)
                self.py_screen.blit(score_2_txt, (self.py_width - score_2_txt.get_rect().width - 10, 10))
            if self.nb_buzzers >= 3:
                self.py_screen.blit(self.font_scores.render(unicode('{} : {}'.format(self.team_names[3], scores[2]), 'utf-8'), True, self.py_color_team3), (10, self.py_height - 30))
                score_4_txt = self.font_scores.render(unicode('{} : {}'.format(self.team_names[4], scores[3]), 'utf-8'), True, self.py_color_team4)
            if self.nb_buzzers >= 4:
                self.py_screen.blit(score_4_txt, (self.py_width - score_4_txt.get_rect().width - 10, self.py_height - 30))

            pygame.display.flip()

            # Baisse les FPS
            time.sleep(1. / 25)

        pygame.display.quit()
        pygame.quit()