# coding=utf-8

import time
from os import listdir
from os.path import isfile, join, abspath

import pygame
from pygame.locals import *

from BuzzerMgr import BuzzerMgr
from ListDialog import ListDialog

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


# noinspection PyUnresolvedReferences
class CompleteBuzzGame:
    """ Jeu simple affichant uniquement l'équipe qui a buzzé, avec le contrôle d'un Master """

    def __init__(self, default_text='Grenade Quizz', images_path=None, window_title='BuzzGame'):
        # Constantes du jeu
        self.default_text = default_text
        self.window_title = window_title
        self.team_names = [
            'master',
            'Pastèques',
            'Ananas',
            'Melons',
            'Kiwis'
        ]
        self.score_win = 500
        self.score_loose = 100

        # Constantes pour PyGame
        self.py_width = 800
        self.py_height = 600
        self.py_margin = 35
        self.py_border = 5
        self.py_frame_top = self.py_frame_left = self.py_margin + self.py_border
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

        # Images
        self.image_mode = False
        self.image_path = images_path
        self.image_folder = None
        self.image_list = None
        self.py_images = None

        # Buzzers
        self.buzzerMgr = BuzzerMgr('ask', True)
        self.nb_buzzers = len(self.buzzerMgr.buzzers) - 1  # enlève le master

    def run(self):
        # Mode image activé : Demande le répertoire des images
        if self.image_path == 'prompt' or self.image_path == 'ask':
            self.image_folder = CompleteBuzzGame.prompt_image_folder()
            if self.image_folder is not None:
                self.image_mode = True
                self.image_list = []
                self.py_images = []
                # TODO: Demander un autre dossier à la fin de celui-ci
            else:
                # TODO: Afficher une erreur avec MessageDialog
                return

        # Démarre PyGame
        pygame.init()
        pygame.display.set_caption(unicode(self.window_title, 'utf-8'))
        self.py_screen = pygame.display.set_mode((self.py_width, self.py_height), pygame.RESIZABLE)

        # Chargement des images
        if self.image_mode:
            self.image_list = CompleteBuzzGame.get_image_list(self.image_folder)
            if len(self.image_list) > 0:
                self.py_images = []
                for image_filename in self.image_list:
                    print abspath('/'.join((self.image_folder, image_filename)))
                    self.py_images.append(pygame.image.load(abspath('/'.join((self.image_folder, image_filename)))).convert())
            else:
                # TODO: Afficher une erreur avec MessageDialog
                return

        # Sons
        self.py_snd_buzzer = pygame.mixer.Sound(abspath('./res/buzzer.ogg'))
        self.py_snd_win = pygame.mixer.Sound(abspath('./res/win.ogg'))
        self.py_snd_loose = pygame.mixer.Sound(abspath('./res/loose.ogg'))

        # Police de caractère (is watching you)
        self.font = pygame.font.SysFont('Arial', 35)
        self.font_scores = pygame.font.SysFont('Arial', 15)

        # Boucle d'exécution
        running = True
        color_bckg = self.py_color_BLACK
        texte_affiche = self.default_text
        state = 'waiting'
        image_cursor = 0
        rising_edge = False
        rising_edge_which = False
        rising_edge_btn = False
        scores = [0] * 4
        while running:
            # Evènements PyGame
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False
                if event.type == VIDEORESIZE:
                    self.py_height = event.h
                    self.py_width = event.w
                    self.py_screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

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
                elif state == 'blocked' or state[0:10] == 'buzz_team_':
                    master_any = self.buzzerMgr.button_pressed('master', 'any')
                    master_plus = self.buzzerMgr.button_pressed('master', '+')
                    master_minus = self.buzzerMgr.button_pressed('master', '-')
                    if master_plus and not state == 'blocked':
                        current_team = int(state[-1])
                        self.py_snd_win.play()
                        scores[current_team - 1] += self.score_win
                        state = 'win_team_{}_'.format(current_team)
                        new_edge = 'rising'
                        new_which, new_btn = 'master', 'any'
                    elif master_minus and not state == 'blocked':
                        current_team = int(state[-1])
                        self.py_snd_loose.play()
                        scores[current_team - 1] -= self.score_loose
                        state = 'loose_team_{}_'.format(current_team)
                        new_edge = 'rising'
                        new_which, new_btn = 'master', 'any'
                    elif master_any:
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

            """ Bordures """
            pygame.draw.rect(self.py_screen, self.py_color_border, pygame.Rect((self.py_margin, self.py_margin),
                                                                               (self.py_width - 2 * self.py_margin,
                                                                                self.py_height - 2 * self.py_margin)),
                             self.py_border)

            """ Fond """
            pygame.draw.rect(self.py_screen, color_bckg,
                             pygame.Rect((self.py_frame_top, self.py_frame_left),
                                         (self.frame_width(), self.frame_height())), 0)

            """ Texte affiché """
            py_txt = self.font.render(unicode(texte_affiche), True, self.py_color_txt)
            txt_pos_x = (self.py_width - py_txt.get_rect().width) / 2
            self.py_screen.blit(py_txt, (txt_pos_x, 110))

            """ Mode image activé : Affiche l'image"""
            if self.image_mode:
                img = self.py_images[image_cursor]
                img_x = (self.py_width - img.get_rect().width) / 2
                img_y = (self.py_height - img.get_rect().height) / 2 + 250
                self.py_screen.blit(img, (img_x, img_y))

            """ Affiche les scores """
            if self.nb_buzzers >= 1:
                self.py_screen.blit(
                    self.font_scores.render(unicode('{} : {}'.format(self.team_names[1], scores[0]), 'utf-8'), True,
                                            self.py_color_team1), (10, 10))
            if self.nb_buzzers >= 2:
                score_2_txt = self.font_scores.render(unicode('{} : {}'.format(self.team_names[2], scores[1]), 'utf-8'),
                                                      True, self.py_color_team2)
                self.py_screen.blit(score_2_txt, (self.py_width - score_2_txt.get_rect().width - 10, 10))
            if self.nb_buzzers >= 3:
                self.py_screen.blit(
                    self.font_scores.render(unicode('{} : {}'.format(self.team_names[3], scores[2]), 'utf-8'), True,
                                            self.py_color_team3), (10, self.py_height - 30))
                score_4_txt = self.font_scores.render(unicode('{} : {}'.format(self.team_names[4], scores[3]), 'utf-8'),
                                                      True, self.py_color_team4)
            if self.nb_buzzers >= 4:
                self.py_screen.blit(score_4_txt,
                                    (self.py_width - score_4_txt.get_rect().width - 10, self.py_height - 30))

            """ Màj écran """
            pygame.display.flip()

            # Baisse les FPS
            time.sleep(1. / 25)

        pygame.display.quit()
        pygame.quit()

    @staticmethod
    def get_image_folders():
        default_dir = './games/images/'
        try:
            folders = []
            for folder in listdir(abspath(default_dir)):
                if not isfile(join(abspath(default_dir), folder)):
                    folders.append(folder)
            return default_dir, folders
        except OSError:
            print u"Aucun répertoire d'images trouvé !"
            return []

    @staticmethod
    def prompt_image_folder():
        folder, folder_list = CompleteBuzzGame.get_image_folders()
        dialog = ListDialog()
        # TODO: Gérer quand il n'y a aucun dossier
        choix = dialog.get_answer(folder_list + ['Annuler'], 'Sélectionnez un dossier :')
        if choix >= len(folder_list):
            return None
        return ''.join((folder, folder_list[choix]))

    @staticmethod
    def get_image_list(dir):
        try:
            images = []
            for image in listdir(dir):
                if isfile(join(dir, image)):
                    images.append(image)
            return images
        except OSError:
            print 'Répertoire introuvable ({}) !'.format(dir)
            return []

    def frame_width(self):
        return self.py_width - 2 * (self.py_margin + self.py_border)

    def frame_height(self):
        return self.py_height - 2 * (self.py_margin + self.py_border)
