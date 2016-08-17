# coding=utf-8

import time
from os import listdir
from os.path import isfile, join, abspath

import pygame
from pygame.locals import *

from ListDialog import ListDialog
from tools import py_encode_font_txt, py_encode_title

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


# noinspection PyUnresolvedReferences
class CompleteBuzzGame:
    """ Jeu simple affichant uniquement l'équipe qui a buzzé, avec le contrôle d'un Master """

    def __init__(self, buzzerMgr, default_text='Grenade Quizz', window_title='BuzzGame', images_path=None, music_path=None):
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
        self.py_margin = 55
        self.py_border = 5
        self.py_frame_top = self.py_frame_left = self.py_margin + self.py_border

        #Colors
        self.window.add_color('black', 'black')
        self.window.add_color('txt', (50, 150, 250))
        self.window.add_color('border', (200, 200, 200))
        self.window.add_color('waiting', (200, 200, 200))
        self.window.add_color('master', (60, 60, 60))
        self.window.add_color('team1', (207, 52, 52))
        self.window.add_color('team2', (207, 250, 30))
        self.window.add_color('team3', (230, 150, 20))
        self.window.add_color('team4', (30, 208, 20))

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
        self.font_sous_txt = None

        # Images
        self.image_mode = False
        self.image_path = images_path
        self.image_list = None
        self.py_images = None

        # Images
        self.music_mode = False
        self.music_path = music_path
        self.music_list = None
        self.py_musics = None

        # Buzzers
        self.buzzerMgr = buzzerMgr
        self.nb_buzzers = len(self.buzzerMgr.buzzers) - 1  # enlève le master

    def run(self):
        # Mode image activé : Demande le répertoire des images
        if self.image_path == 'prompt' or self.image_path == 'ask':
            self.image_path = CompleteBuzzGame.prompt_image_folder()
            if self.image_path is not None:
                self.image_mode = True
                self.image_list = []
                self.py_images = []
                # TODO: Demander un autre dossier à la fin de celui-ci
            else:
                # TODO: Afficher une erreur avec MessageDialog
                return

        # Mode musique activé : Demande le répertoire des musiques
        if self.music_path == 'prompt' or self.music_path == 'ask':
            self.music_path = CompleteBuzzGame.prompt_music_folder()
            if self.music_path is not None:
                self.music_mode = True
                self.music_list = []
                self.py_musics = []
                # TODO: Demander un autre dossier à la fin de celui-ci
            else:
                # TODO: Afficher une erreur avec MessageDialog
                return

        # Démarre PyGame
        self.window.new_page(self.window_title, goTo=True)

        # Mode image activé : Chargement des images
        if self.image_mode:
            self.image_list = CompleteBuzzGame.get_file_list(self.image_path)
            if len(self.image_list) > 0:
                self.py_images = []
                for image_filename in self.image_list:
                    # TODO: Détecter les erreurs de chargement
                    self.window.add_img(abspath('/'.join((self.image_path, image_filename))), 0, 0, printElem=False)
            else:
                # TODO: Afficher une erreur avec MessageDialog
                return

        # Mode musique activé : Chargement des musiques
        if self.music_mode:
            self.music_list = CompleteBuzzGame.get_file_list(self.music_path)
            if len(self.music_list) > 0:
                self.py_musics = []
                for image_filename in self.music_list:
                    self.window.add_music(abspath('/'.join((self.music_path, image_filename))))
            else:
                # TODO: Afficher une erreur avec MessageDialog
                return

        # Sons
        self.window.add_music(abspath('./res/buzzer.ogg'))
        self.py_snd_buzzer = pygame.mixer.Sound()
        self.py_snd_win = pygame.mixer.Sound(abspath('./res/win.ogg'))
        self.py_snd_loose = pygame.mixer.Sound(abspath('./res/loose.ogg'))

        # Police de caractère (is watching you)
        self.font = pygame.font.SysFont('Arial', 35)
        self.font_scores = pygame.font.SysFont('Arial', 24)
        self.font_sous_txt = pygame.font.SysFont('Arial', 20)

        # Boucle d'exécution
        running = True
        color_bckg = self.py_color_BLACK
        texte_affiche = self.default_text
        state = 'waiting'
        image_cursor = 0
        image_mode_displayed = False
        music_cursor = 0
        music_timer_sec = 0
        music_mode_changed = True
        music_mode_playing = False
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
                    # Mode image activé : Gestion des images
                    change = False
                    if self.image_mode or self.music_mode:
                        change = True
                        if self.buzzerMgr.button_pressed('master', 'up'):
                            image_mode_displayed = True
                            music_mode_playing, music_mode_changed = True, True
                            new_edge, new_which, new_btn = 'rising', 'master', 'up'
                        elif self.buzzerMgr.button_pressed('master', 'down'):
                            image_mode_displayed = False
                            music_mode_playing, music_mode_changed = False, True
                            new_edge, new_which, new_btn = 'rising', 'master', 'down'
                        elif self.buzzerMgr.button_pressed('master', 'right'):
                            image_cursor += 1
                            music_cursor += 1
                            music_mode_playing, music_mode_changed = False, True
                            new_edge, new_which, new_btn = 'rising', 'master', 'right'
                        elif self.buzzerMgr.button_pressed('master', 'left'):
                            image_cursor -= 1
                            music_cursor -= 1
                            music_mode_playing, music_mode_changed = False, True
                            new_edge, new_which, new_btn = 'rising', 'master', 'left'
                        else:
                            change = False
                        if self.image_mode:  # Evitons la division par zéro
                            image_cursor %= len(self.image_list)
                        if self.music_mode:
                            music_cursor %= len(self.music_list)
                    if not change:
                        liste_any = self.buzzerMgr.buzzers_which(
                            'any')  # TODO: A pour master et any pour les joueurs (créer un 'players' comme which)
                        buzzer_any = self.buzzerMgr.any_of(liste_any)
                        if buzzer_any is not None:
                            if buzzer_any.team == 'master':
                                state = 'blocked_'
                                new_edge, new_which, new_btn = 'rising', 'master', 'any'
                            else:
                                self.py_snd_buzzer.play()
                                state = 'buzz_team_{}_'.format(buzzer_any.team)
                                music_mode_playing, music_mode_changed = False, True
                elif state == 'blocked' or state[0:10] == 'buzz_team_':
                    master_any = self.buzzerMgr.button_pressed('master', 'any')
                    master_plus = self.buzzerMgr.button_pressed('master', '+')
                    master_minus = self.buzzerMgr.button_pressed('master', '-')
                    if master_plus and not state == 'blocked':
                        current_team = int(state[-1])
                        self.py_snd_win.play()
                        scores[current_team - 1] += self.score_win
                        state = 'win_team_{}_'.format(current_team)
                        new_edge, new_which, new_btn = 'rising', 'master', 'any'
                    elif master_minus and not state == 'blocked':
                        current_team = int(state[-1])
                        self.py_snd_loose.play()
                        scores[current_team - 1] -= self.score_loose
                        state = 'loose_team_{}_'.format(current_team)
                        new_edge, new_which, new_btn = 'rising', 'master', 'any'
                    elif master_any:
                        music_mode_playing, music_mode_changed = False, True
                        state = 'waiting_'
                        new_edge, new_which, new_btn = 'rising', 'master', 'any'
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

            # Mode musique activé : Gestion de la lecture
            if self.music_mode:
                if music_mode_playing and music_mode_changed:
                    music_timer_sec = time.time()
                if music_mode_changed:  # Au changement de lecture, on démarre ou arrête la musique
                    music_mode_changed = False
                    for m in self.py_musics:
                        m.stop()
                    if music_mode_playing:
                        self.py_musics[music_cursor].play()
                if music_mode_playing:  # Détecte la fin de la lecture
                    if not pygame.mixer.get_busy():
                        music_mode_playing = False

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

            """ Mode image activé : Affiche l'image """
            if self.image_mode:
                if image_mode_displayed:  # Affiche l'image
                    img = self.py_images[image_cursor]
                    img_x = (self.py_width - img.get_rect().width) / 2
                    img_y = (self.py_height - img.get_rect().height) / 2
                    self.py_screen.blit(img, (img_x, img_y))
                else:  # Affiche quelle image n'est pas affichée
                    py_txt = self.font_sous_txt.render(
                        py_encode_font_txt('{} / {}'.format(image_cursor + 1, len(self.image_list))),
                        True, self.py_color_txt
                    )
                    txt_pos_x = self.py_margin + self.py_border + 5
                    txt_pos_y = self.py_margin + self.py_border + 5
                    self.py_screen.blit(py_txt, (txt_pos_x, txt_pos_y))

            """ Mode musique activé : Infos sur la musique en cours """
            if self.music_mode:
                timer_sec = time.time() - music_timer_sec if music_mode_playing else 0
                py_txt = self.font_sous_txt.render(
                    py_encode_font_txt(
                        "{} / {} : {} - {:.2f} / {:.2f} sec".format(music_cursor + 1, len(self.music_list),
                                                                      'Playing' if music_mode_playing else 'Stop',
                                                                      timer_sec,
                                                                      float(self.py_musics[music_cursor].get_length()))),
                    True, self.py_color_txt
                )
                txt_pos_x = self.py_margin + self.py_border + 5
                txt_pos_y = self.py_height - self.py_margin - self.py_border - 5 - py_txt.get_rect().height
                self.py_screen.blit(py_txt, (txt_pos_x, txt_pos_y))

            """ Texte affiché """
            if state != 'waiting' or not (self.image_mode and image_mode_displayed):
                py_txt = self.font.render(py_encode_font_txt(texte_affiche), True, self.py_color_txt)
                txt_pos_x = (self.py_width - py_txt.get_rect().width) / 2
                self.py_screen.blit(py_txt, (txt_pos_x, 110))

            """ Affiche les scores """
            if self.nb_buzzers >= 1:
                self.py_screen.blit(
                    self.font_scores.render(py_encode_font_txt('{} : {}'.format(self.team_names[1], scores[0])), True,
                                            self.py_color_team1), (10, 10))
            if self.nb_buzzers >= 2:
                score_2_txt = self.font_scores.render(
                    py_encode_font_txt('{} : {}'.format(self.team_names[2], scores[1])),
                    True, self.py_color_team2)
                self.py_screen.blit(score_2_txt, (self.py_width - score_2_txt.get_rect().width - 10, 10))
            if self.nb_buzzers >= 3:
                self.py_screen.blit(
                    self.font_scores.render(py_encode_font_txt('{} : {}'.format(self.team_names[3], scores[2])), True,
                                            self.py_color_team3), (10, self.py_height - 30))
                score_4_txt = self.font_scores.render(
                    py_encode_font_txt('{} : {}'.format(self.team_names[4], scores[3])),
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
        return CompleteBuzzGame.get_folder_list('./games/images/')

    @staticmethod
    def get_music_folders():
        return CompleteBuzzGame.get_folder_list('./games/musiques/')

    @staticmethod
    def get_folder_list(path):
        try:
            folders = []
            for folder in listdir(abspath(path)):
                if not isfile(join(abspath(path), folder)):
                    folders.append(folder)
            return path, folders
        except OSError:
            print u"Aucun répertoire d'images trouvé !"
            return []

    # TODO: En faire un Dialog -> FolderDialog
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
    def prompt_music_folder():
        folder, folder_list = CompleteBuzzGame.get_music_folders()
        dialog = ListDialog()
        # TODO: Gérer quand il n'y a aucun dossier
        choix = dialog.get_answer(folder_list + ['Annuler'], 'Sélectionnez un dossier :')
        if choix >= len(folder_list):
            return None
        return ''.join((folder, folder_list[choix]))

    @staticmethod
    def get_file_list(path):
        try:
            images = []
            for image in listdir(path):
                if isfile(join(path, image)):
                    images.append(image)
            return images
        except OSError:
            print 'Répertoire introuvable ({}) !'.format(path)
            return []

    def frame_width(self):
        return self.py_width - 2 * (self.py_margin + self.py_border)

    def frame_height(self):
        return self.py_height - 2 * (self.py_margin + self.py_border)