# coding=utf-8

import os
import random
import time

from windowsHelper import windowsHelper
from colorHelper import colorHelper

from tools import py_encode_font_txt, py_encode_title, format_text


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
        window = windowsHelper(self.py_width, self.py_height, 'Initialisation des Buzzers')
        
        # Couleurs
        window.addColor("txt", (50, 150, 250))
        window.addColor("border", (200, 200, 200))
        window.addColor("success", (52, 207, 52))
        window.addColor("bckg", colorHelper("black"))

        # Images
        window.addImg(os.path.abspath('./res/sync_buzzer.jpg'), 0, 0, printElem=False, label="img_wiimote")

        # Police de caractère (is watching you)
        window.addFont("Arial", 35, "font")
        
            
        window.addRect('border', 
            self.py_margin, 
            self.py_margin, 
            self.py_width - 2 * self.py_margin, 
            self.py_height - 2 * self.py_margin,
            self.py_border,
            label='bordure')

        # Options d'execution
        options = {
            'sub_state': -1, 
            'init_state': 'aucun', 
            'current_buzzer': None, 
            'texte_affiche': 'Chargement', 
            'transition_next': 0, 
            'transition_percent': 0,
            'self': self # instance de l'objet courant, appelable dans fun_after grace à options['self']
        }
        fun_before = lambda pg, win, opt: () # Fonction s'executant avant la boucle d'event
        fun_event = lambda event, pg, win, opt: () # Boucle s'executant pendant l'event
        """ 
            param: pg instance de pygame
            param: win instance de windowsHelper courante
            param: options, liste d'options envoyé en paramètre à la fonction event de windowsHelper (contient les variables)
        """
        def fun_after(pg, win, options):
            from Buzzer import Buzzer
            win.reset(True)
            if options['init_state'] == 'aucun':
                if options['self'].need_master:
                    options['current_buzzer'] = Buzzer('master', dummy=self.dummy)
                    options['init_state'] = 'waiting_master'
                    options['current_buzzer'].async_wait()
                    options['texte_affiche'] = 'Télécommande Master'
                else:
                    options['init_state'] = 10
            elif options['init_state'] == 'waiting_master':
                if options['current_buzzer'].connected:
                    options['self'].buzzers['master'] = options['current_buzzer']
                    options['current_buzzer'] = None
                    options['init_state'] = 'transition'
                    options['transition_next'] = 1
                    options['transition_percent'] = 0
            elif isinstance(options['init_state'], int):
                state_wii_nb = int(options['init_state'] / 10)
                sub_state = options['init_state'] - 10 * state_wii_nb
                if sub_state == 0:
                    options['texte_affiche'] = 'Télécommande {}'.format(state_wii_nb)
                    options['current_buzzer'] = Buzzer(state_wii_nb, dummy=self.dummy)
                    options['current_buzzer'].async_wait()
                    options['init_state'] += 1
                elif sub_state == 1:
                    if options['current_buzzer'].connected:
                        options['self'].buzzers[state_wii_nb] = options['current_buzzer']
                        options['current_buzzer'] = None
                        options['init_state'] = 'transition'
                        options['transition_next'] = state_wii_nb + 1
                        options['transition_percent'] = 0
                        sub_state = 2
            elif options['init_state'] == 'transition':
                options['transition_percent'] += options['transition_percent'] / 2 + 1
                if options['transition_percent'] >= 100:
                    if options['transition_next'] > options['self'].nb_wiimote:
                        win.toQuit = True
                        return True
                    options['init_state'] = options['transition_next'] * 10
                    options['texte_affiche'] = ''
                    

            # Affichage
            if  options['init_state'] == 'transition':
                green_top = green_left =  options['self'].py_margin +  options['self'].py_border
                green_width =  options['self'].py_width - 2 * ( options['self'].py_margin +  options['self'].py_border)
                green_height =  options['self'].py_height - 2 * ( options['self'].py_margin +  options['self'].py_border)
                green_color = tuple(int(round(c * (100 -  options['transition_percent']) / 100.0)) for c in win.colors['success'])
                win.addRect(green_color, green_top, green_left, green_width, green_height, 0)
            else:
                win.addText(options['texte_affiche'], 'font', 'txt', y=110, label=format_text(options['texte_affiche']), opt={'widthcentered':True})
                win.printElem('img_wiimote', x=250, y=250)
                win.printElem('bordure')
                
            return False
        
        window.event(fun_before, fun_event, fun_after, options)

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