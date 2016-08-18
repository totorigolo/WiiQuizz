# coding=utf-8

import os
import random

from WindowHelper import WindowHelper

# noinspection PyUnresolvedReferences
class BuzzerMgr:
    def __init__(self, nb_wiimote, need_master, dummy=False):
        """ Initialise les Wiimote dans une GUI """

        # TODO: S'arranger pour ne demander qu'une seule fois la connexion des manettes durant une session

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

        # Démarre Fenètre
        win = WindowHelper.Instance()
        # Démarre Fenêtre si pas ouverte
        if not win.is_open():
            win.open_window(self.py_width, self.py_height)

        page_label = win.new_page('Initialisation des Buzzers')
        
        # Couleurs
        win.new_color((50, 150, 250), "txt")
        win.new_color((200, 200, 200), "border")
        win.new_color((52, 207, 52), "success")
        win.new_color("black", "bckg")

        # Police de caractère (is watching you)
        win.new_font("Arial", 35, "font")

        # Images
        win.new_img(os.path.abspath('./res/sync_buzzer.jpg'), label='img_wiimote')

        # Textes de titre
        win.new_text('Télécommande master', 'font', 'txt', label='txt_tel_master')
        win.new_text('Télécommande 1', 'font', 'txt', label='txt_tel_1')
        win.new_text('Télécommande 2', 'font', 'txt', label='txt_tel_2')
        win.new_text('Télécommande 3', 'font', 'txt', label='txt_tel_3')
        win.new_text('Télécommande 4', 'font', 'txt', label='txt_tel_4')
        win.new_text('Chargement...', 'font', 'txt', label='loading')

        win.add('loading', 'centered', 110, page_label)

        win.new_rect('border', self.py_border, label='border_rect')
        win.add('border_rect',
                [self.py_margin, self.py_width - 2 * self.py_margin],
                [self.py_margin, self.py_height - 2 * self.py_margin],
                page_label)

        win.go_to(page_label)

        # Options d'execution
        vars = {
            'sub_state': -1, 
            'init_state': 'aucun', 
            'current_buzzer': None, 
            'texte_affiche': 'Chargement', 
            'transition_next': 0, 
            'transition_percent': 0,
            'page_label': page_label,
            'self': self # instance de l'objet courant, appelable dans fun_after grace à options['self']
        }

        """ 
            param: pg instance de pygame
            param: win instance de windowsHelper courante
            param: options, liste d'options envoyé en paramètre à la fonction event de windowsHelper (contient les variables)
        """
        def fun_after(pg, win, vars):
            from Buzzer import Buzzer
            page_label = vars['page_label']
            if vars['init_state'] == 'aucun':
                if vars['self'].need_master:
                    vars['current_buzzer'] = Buzzer('master', dummy=self.dummy)
                    vars['init_state'] = 'waiting_master'
                    vars['current_buzzer'].async_wait()
                    vars['texte_affiche'] = 'txt_tel_master'
                else:
                    vars['init_state'] = 10
            elif vars['init_state'] == 'waiting_master':
                if vars['current_buzzer'].connected:
                    vars['self'].buzzers['master'] = vars['current_buzzer']
                    vars['current_buzzer'] = None
                    vars['init_state'] = 'transition'
                    vars['transition_next'] = 1
                    vars['transition_percent'] = 0
            elif isinstance(vars['init_state'], int):
                state_wii_nb = int(vars['init_state'] / 10)
                sub_state = vars['init_state'] - 10 * state_wii_nb
                if sub_state == 0:
                    vars['texte_affiche'] = 'txt_tel_{}'.format(state_wii_nb)
                    vars['current_buzzer'] = Buzzer(state_wii_nb, dummy=self.dummy)
                    vars['current_buzzer'].async_wait()
                    vars['init_state'] += 1
                elif sub_state == 1:
                    if vars['current_buzzer'].connected:
                        vars['self'].buzzers[state_wii_nb] = vars['current_buzzer']
                        vars['current_buzzer'] = None
                        vars['init_state'] = 'transition'
                        vars['transition_next'] = state_wii_nb + 1
                        vars['transition_percent'] = 0
                        sub_state = 2
            elif vars['init_state'] == 'transition':
                vars['transition_percent'] += vars['transition_percent'] / 2 + 1
                if vars['transition_percent'] >= 100:
                    if vars['transition_next'] > vars['self'].nb_wiimote:
                        return True
                    vars['init_state'] = vars['transition_next'] * 10
                    vars['texte_affiche'] = ''

            # Affichage
            win.reset()
            win.delete('loading', page_label)  # Suppression du message de chargement

            if vars['init_state'] == 'transition':
                # Rectangle vert
                green_top = green_left = vars['self'].py_margin + vars['self'].py_border
                green_width = vars['self'].py_width - 2 * (vars['self'].py_margin + vars['self'].py_border)
                green_height = vars['self'].py_height - 2 * (vars['self'].py_margin + vars['self'].py_border)
                color_tuple = win.colors['success'].get_rgb()
                green_color = tuple(int(round(c * (100 - vars['transition_percent']) / 100.0)) for c in color_tuple)
                rect_label = win.nb_use(win.new_rect(green_color, 0), 1)
                win.add(rect_label, [green_top, green_width], [green_left, green_height], page_label)
            else:
                win.add(vars['texte_affiche'], 'centered', 110, page_label)
                win.add('img_wiimote', 250, 250, page_label)  # image wiimote
            win.print_page(page_label)
            win.delete(vars['texte_affiche'])
            return False
        
        win.event(after_fun=fun_after, vars=vars, page=page_label)

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
        from ListDialog import ListDialog
        dialog = ListDialog()

        if need_master:
            question = u'Combien de Wiimotes joueuses ?'
            sous_texte = "une manette supplémentaire est requise pour le contrôle du jeu"
            return dialog.get_answer([i for i in range(1, 5)], question, sous_texte) + 1
        else:
            question = u'A combien de Wiimotes voulez-vous jouer ?'
            sous_texte = None
            return dialog.get_answer([i for i in range(1, 5)], question, sous_texte)