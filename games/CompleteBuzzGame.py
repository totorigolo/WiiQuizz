# coding=utf-8

import time
from os import listdir
from os.path import isfile, join, abspath

from WindowHelper import WindowHelper
from ListDialog_old import ListDialog
from tools import py_encode_font_txt


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

        self.win = WindowHelper.Instance()

        # Constantes pour PyGame
        self.py_width = 800
        self.py_height = 600
        self.py_margin = 55
        self.py_border = 5
        self.py_frame_top = self.py_frame_left = self.py_margin + self.py_border

        # Démarre Fenêtre si pas ouverte
        if not self.win.is_open():
            self.win.open_window(self.py_width, self.py_height)

        # Colors
        self.win.new_color('black')
        self.win.new_color((50, 150, 250), 'txt')
        self.win.new_color((200, 200, 200), 'border')
        self.win.new_color((200, 200, 200), 'waiting')
        self.win.new_color((60, 60, 60), 'master')
        self.win.new_color((207, 52, 52), 'team1')
        self.win.new_color((207, 250, 30), 'team2')
        self.win.new_color((230, 150, 20), 'team3')
        self.win.new_color((30, 208, 20), 'team4')

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

        # Nouvelle page
        label_page = self.win.new_page(self.window_title)
        self.win.go_to(label_page)

        # Mode image activé : Chargement des images
        if self.image_mode:
            self.image_list = CompleteBuzzGame.get_file_list(self.image_path)
            if len(self.image_list) > 0:
                self.py_images = []
                for image_filename in self.image_list:
                    # TODO: Détecter les erreurs de chargement
                    self.py_images.append(
                        self.win.new_img(abspath('/'.join((self.image_path, image_filename))))
                    ) # On enregistre les labels des images
            else:
                # TODO: Afficher une erreur avec MessageDialog
                return

        # Mode musique activé : Chargement des musiques
        if self.music_mode:
            self.music_list = CompleteBuzzGame.get_file_list(self.music_path)
            if len(self.music_list) > 0:
                self.py_musics = []
                for image_filename in self.music_list:
                    self.py_musics.append(
                        self.win.new_sound(abspath('/'.join((self.music_path, image_filename))))
                    )  # On enregistre les labels des sons
            else:
                # TODO: Afficher une erreur avec MessageDialog
                return

        # Sons
        self.win.new_sound(abspath('./res/buzzer.ogg'), label='snd_buzzer')
        self.win.new_sound(abspath('./res/win.ogg'), label='snd_win')
        self.win.new_sound(abspath('./res/loose.ogg'), label='snd_loose')

        # Police de caractère (is watching you)
        self.win.new_font('Arial', 35, 'font')
        self.win.new_font('Arial', 24, 'scores')
        self.win.new_font('Arial', 20, 'sous_txt')

        # Bordure de l'écran
        self.win.new_rect('border', self.py_border, label='win_border')

        # Fonds d'écrans
        self.win.new_rect('waiting', 0, label='bg_waiting')
        self.win.new_rect('master', 0, label='bg_master')
        self.win.new_rect('team1', 0, label='bg_team1')
        self.win.new_rect('team2', 0, label='bg_team2')
        self.win.new_rect('team3', 0, label='bg_team3')
        self.win.new_rect('team4', 0, label='bg_team4')

        # Variable d'execution
        vars = {
            'texte_affiche': self.default_text,
            'state': 'waiting',
            'image_cursor': 0,
            'image_mode_displayed': False,
            'music_cursor': 0,
            'music_timer_sec': 0,
            'music_mode_changed': True,
            'music_mode_playing': False,
            'rising_edge': False,
            'rising_edge_which': False,
            'rising_edge_btn': False,
            'scores': [0] * 4,
            'self': self,
            'label_page': label_page
        }

        """
            Appelée pour lister les événements
        """

        def event_fun(pg, win, vars, event):
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:
                return True
            if event.type == pg.locals.VIDEORESIZE:
                vars['self'].py_height = event.h
                vars['self'].py_width = event.w
                vars['self'].py_screen = win.open_window(event.w, event.h)

        """
            Appelé après les événements
        """

        def after_fun(pg, win, vars):
            # variables
            texte_affiche = vars['texte_affiche']
            state = vars['state']
            image_cursor = vars['image_cursor']
            image_mode_displayed = vars['image_mode_displayed']
            music_cursor = vars['music_cursor']
            music_timer_sec = vars['music_timer_sec']
            music_mode_changed = vars['music_mode_changed']
            music_mode_playing = vars['music_mode_playing']
            rising_edge = vars['rising_edge']
            rising_edge_which = vars['rising_edge_which']
            rising_edge_btn = vars['rising_edge_btn']
            scores = vars['scores']
            label_page = vars['label_page']

            # Evénements Wiimote
            new_edge, new_which, new_btn = False, None, None
            if rising_edge:
                if not vars['self'].buzzerMgr.button_down(rising_edge_which, rising_edge_btn):
                    rising_edge = False
            else:
                if state == 'waiting':
                    # Mode image activé : Gestion des images
                    change = False
                    if vars['self'].image_mode or vars['self'].music_mode:
                        change = True
                        if vars['self'].buzzerMgr.button_down('master', 'up'):
                            image_mode_displayed = True
                            music_mode_playing, music_mode_changed = True, True
                            new_edge, new_which, new_btn = 'rising', 'master', 'up'
                        elif vars['self'].buzzerMgr.button_down('master', 'down'):
                            image_mode_displayed = False
                            music_mode_playing, music_mode_changed = False, True
                            new_edge, new_which, new_btn = 'rising', 'master', 'down'
                        elif vars['self'].buzzerMgr.button_down('master', 'right'):
                            image_cursor += 1
                            music_cursor += 1
                            music_mode_playing, music_mode_changed = False, True
                            new_edge, new_which, new_btn = 'rising', 'master', 'right'
                        elif vars['self'].buzzerMgr.button_down('master', 'left'):
                            image_cursor -= 1
                            music_cursor -= 1
                            music_mode_playing, music_mode_changed = False, True
                            new_edge, new_which, new_btn = 'rising', 'master', 'left'
                        else:
                            change = False
                        if vars['self'].image_mode:  # Evitons la division par zéro
                            image_cursor %= len(vars['self'].image_list)
                        if vars['self'].music_mode:
                            music_cursor %= len(vars['self'].music_list)
                    if not change:
                        liste_any = vars['self'].buzzerMgr.buzzers_which(
                            'any')  # TODO: A pour master et any pour les joueurs (créer un 'players' comme which)
                        buzzer_any = vars['self'].buzzerMgr.any_of(liste_any)
                        if buzzer_any is not None:
                            if buzzer_any.team == 'master':
                                state = 'blocked_'
                                new_edge, new_which, new_btn = 'rising', 'master', 'any'
                            else:
                                win.play_sound('snd_buzzer')
                                state = 'buzz_team_{}_'.format(buzzer_any.team)
                                music_mode_playing, music_mode_changed = False, True
                elif state == 'blocked' or state[0:10] == 'buzz_team_':
                    master_any = vars['self'].buzzerMgr.button_down('master', 'any')
                    master_plus = vars['self'].buzzerMgr.button_down('master', '+')
                    master_minus = vars['self'].buzzerMgr.button_down('master', '-')
                    if master_plus and not state == 'blocked':
                        current_team = int(state[-1])
                        win.play_sound('snd_win') # Victoire !!
                        scores[current_team - 1] += vars['self'].score_win
                        state = 'win_team_{}_'.format(current_team)
                        new_edge, new_which, new_btn = 'rising', 'master', 'any'
                    elif master_minus and not state == 'blocked':
                        current_team = int(state[-1])
                        win.play_sound('snd_loose')  # Boooo !!
                        scores[current_team - 1] -= vars['self'].score_loose
                        state = 'loose_team_{}_'.format(current_team)
                        new_edge, new_which, new_btn = 'rising', 'master', 'any'
                    elif master_any:
                        music_mode_playing, music_mode_changed = False, True
                        state = 'waiting_'
                        new_edge, new_which, new_btn = 'rising', 'master', 'any'
            if new_edge == 'rising':
                rising_edge = True
                rising_edge_which, rising_edge_btn = new_which, new_btn

            # Gestion de l'état : Préparation du texte (label : txt_affiche)
            color_bckg = 'waiting'
            if state == 'waiting_':
                color_bckg = 'waiting'
                win.nb_use(win.new_text(vars['self'].default_text, 'font', 'waiting', label='txt_affiche'), 1)
                state = state[:-1]
            elif state == 'blocked_':
                color_bckg = 'master'
                win.nb_use(win.new_text('', 'font', 'master', label='txt_affiche'), 1)
                state = state[:-1]
            elif state[0:10] == 'buzz_team_' and state[-1] == '_':
                team = int(state[-2])
                color_bckg = 'team{}'.format(team)
                texte_affiche = vars['self'].team_names[team]
                win.nb_use(win.new_text(texte_affiche, 'font', color_bckg, label='txt_affiche'), 1)
                state = state[:-1]
            elif state[0:9] == 'win_team_' and state[-1] == '_':
                team = int(state[-2])
                color_bckg = 'team{}'.format(team)
                win.nb_use(win.new_text('Gagné !', 'font', color_bckg, label='txt_affiche'), 1)
                state = 'blocked'
            elif state[0:11] == 'loose_team_' and state[-1] == '_':
                team = int(state[-2])
                color_bckg = 'team{}'.format(team)
                win.nb_use(win.new_text('FAUX !', 'font', color_bckg, label='txt_affiche'), 1)
                state = 'blocked'
            else:
                win.nb_use(win.new_text('', 'font', 'waiting', label='txt_affiche'), 1)

            # Mode musique activé : Gestion de la lecture
            if vars['self'].music_mode:
                if music_mode_playing and music_mode_changed:
                    music_timer_sec = time.time()
                if music_mode_changed:  # Au changement de lecture, on démarre ou arrête la musique
                    music_mode_changed = False
                    for m in vars['self'].py_musics:
                        win.stop_sound(m)
                    if music_mode_playing:
                        win.play_sound(music_cursor)
                if music_mode_playing:  # Détecte la fin de la lecture
                    if not win.is_mixer_busy():
                        music_mode_playing = False

            # Affichage
            win.fill('black')

            # Bordures
            win.add('win_border',
                     [vars['self'].py_margin, vars['self'].py_width - 2 * vars['self'].py_margin],
                     [vars['self'].py_margin, vars['self'].py_height - 2 * vars['self'].py_margin],
                     label_page)

            # Fond
            label_bg = 'bg_' + color_bckg
            win.add(label_bg,
                    [vars['self'].py_frame_top, vars['self'].frame_width()],
                    [vars['self'].py_frame_left, vars['self'].frame_height()],
                    label_page)

            # Mode image activé : Affiche l'image
            if vars['self'].image_mode:
                if image_mode_displayed:  # Affiche l'image
                    img = vars['self'].py_images[image_cursor]
                    img_x = (vars['self'].py_width - img.get_rect().width) / 2
                    img_y = (vars['self'].py_height - img.get_rect().height) / 2
                    win.add(img, img_x, img_y, label_page)
                else:  # Affiche l'image non affichée
                    text = '{} / {}'.format(image_cursor + 1, len(vars['self'].image_list))
                    # L'objet sera utilisé qu'une fois avant d'être supprimé
                    label_txt = win.nb_use(win.new_text(text, 'sous_txt', 'txt'), 1)

                    txt_pos_x = vars['self'].py_margin + vars['self'].py_border + 5
                    txt_pos_y = vars['self'].py_margin + vars['self'].py_border + 5
                    win.add(label_txt, txt_pos_x, txt_pos_y, label_page)

            # Mode musique activé : Infos sur la musique en cours
            if vars['self'].music_mode:
                timer_sec = time.time() - music_timer_sec if music_mode_playing else 0
                text = "{} / {} : {} - {:.2f} / {:.2f} sec".format(music_cursor + 1, len(vars['self'].music_list),
                                                                    'Playing' if music_mode_playing else 'Stop',
                                                                    timer_sec,
                                                                    float(vars['self'].py_musics[music_cursor].get_length()))
                label_txt = win.nb_use(win.new_text(text, 'font', 'txt'), 1)

                txt_pos_x = vars['self'].py_margin + vars['self'].py_border + 5
                txt_pos_y = vars['self'].py_height - vars['self'].py_margin - vars['self'].py_border - \
                            5 - win.get_element(label_txt)['obj'].get_rect().height
                win.add(label_txt, txt_pos_x, txt_pos_y, label_page)

            # Texte affiché
            if state != 'waiting' or not (vars['self'].image_mode and image_mode_displayed):
                txt_pos_x = (vars['self'].py_width - win.get_element('txt_affiche')['obj'].get_rect().width) / 2
                win.add('txt_affiche', txt_pos_x, 110, label_page)

            # Affiche les scores
            if vars['self'].nb_buzzers >= 1:
                win.add(
                    win.nb_use(
                        win.new_text('{} : {}'.format(vars['self'].team_names[1], scores[0]), 'scores', 'team1'),
                        1),
                    10, 10, label_page)
            if vars['self'].nb_buzzers >= 2:
                label_txt = win.nb_use(win.new_text('{} : {}'.format(vars['self'].team_names[2], scores[1]), 'scores', 'team2'), 1)
                win.add(label_txt, vars['self'].py_width - win.get_element(label_txt)['obj'].get_rect().width, 10, label_page)
            if vars['self'].nb_buzzers >= 3:
                win.add(
                    win.nb_use(win.new_text('{} : {}'.format(vars['self'].team_names[3], scores[2]), 'scores', 'team3'), 1),
                    10, vars['self'].py_height - 30, label_page
                )
            if vars['self'].nb_buzzers >= 4:
                label_txt = win.nb_use(win.new_text('{} : {}'.format(vars['self'].team_names[4], scores[3]), 'scores', 'team4'),
                           1)
                win.add(label_txt,
                        vars['self'].py_width - win.get_element(label_txt)['obj'].get_rect().width - 10,
                        vars['self'].py_height - 30,
                        label_page)
            win.refresh()

        self.win.event(event_fun=event_fun, after_fun=after_fun, vars=vars)


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