# coding: utf8

from inspect import isfunction

from Singleton import Singleton

import pygame as pg
from pygame.locals import *

from ColorHelper import ColorHelper
from tools import py_encode_font_txt, py_encode_title
import re
import os

if not pg.font: print 'Warning, fonts disabled'
if not pg.mixer: print 'Warning, sound disabled'

@Singleton
class WindowHelper:

    def __init__(self):
        self.elements = {}  # éléments (toute sorte !)
        self.colors = {}  # couleurs
        self.fonts = {}  # liste des polices
        self.pages = {}  # liste des pages
        self.current_page = -1  # page active
        self.win = None  # Fenêtre pygame
        self.opened = False
        self.resizable = True

    """
        Initialise pygame
    """

    def init(self):
        if not self.opened:
            pg.init()

    def __del__(self):
        try:
            self.opened = False
            self.close()
            pg.quit()
        except AttributeError:
            pass

    """
        Ouvre une nouvelle fenêtre de taille width * height
    """

    def open_window(self, width=500, height=500, resizable=None):
        self.init()
        if resizable is None:
            resizable = self.resizable
        if resizable:
            self.win = pg.display.set_mode((width, height), RESIZABLE)
        else:
            self.win = pg.display.set_mode((width, height))
        self.resizable = resizable

        # Quelques ressources initialisées par défaut
        if not self.opened:
            self.new_font('Arial', 30, 'default')
            self.new_color('black')
            self.new_color('white')
        self.opened = True

    def is_open(self):
        return self.opened

    """
        Ferme la fenêtre
    """
    def close(self):
        try:
            pg.display.quit()
        except AttributeError:
            self.opened = False

    def callback_close(self):
        self.opened = False

    """
        Ferme la session pygame
    """
    def quit(self):
        self.__del__()
    """
        Ajoute une page
        param: title titre de la page
        param: label optional (default: num)
        param: bg optional couleur de fond (default: black)
        returns: label donné
    """

    def new_page(self, title, width=500, height=500, label=None, bg=None):
        if not self.is_open():
            self.open_window(width, height)
        if label is None:
            label = len(self.pages)
        if bg is None:
            bg = self.new_color('black')  # récupère le label de la couleur black
        elif (isinstance(bg, str) and bg not in self.colors.keys()) or \
                isinstance(bg, tuple) or \
                isinstance(bg, ColorHelper):
            bg = self.new_color(bg)
        p_width, p_height = pg.display.get_surface().get_size()
        if height is not None or width is not None:
            self.open_window(width, height)
        if width is None:
            width = p_width
        if height is None:
            height = p_height
        self.pages[label] = {
            'title': title,
            'width': width,
            'height': height,
            'bg': bg,
            'elements': []
        }
        return label

    """
        Change de page
    """

    def go_to(self, label):
        self.current_page = label
        pg.display.set_caption(py_encode_title(self.pages[label]['title']))
        self.reset()
        self.print_page(label)

    """
        Définit le nombre de fois qu'un élément peut être affiché avant d'être automatiquement supprimé
        param: label de l'élément
        param: num de fois que l'élément peut être utilisé
        return: label
    """

    def nb_use(self, label, num=1):
        self.elements[label]['nb_usable'] = num
        return label

    """
        Ajoute une couleur dans la liste des couleurs
        param: color type str | ColorHelper | tuple
        param: label optional (default: num)
        returns: label
    """

    def new_color(self, color, label=None):
        if label is None:
            if isinstance(color, str) and (color, color) not in self.colors.items():
                label = color
            else:
                label = len(self.colors)
        if isinstance(color, str) or isinstance(color, tuple):
            color = ColorHelper(color)
        self.colors[label] = color
        return label

    """
        Ajoute une police de caractère
    """

    def new_font(self, family, size, label=None, opt=None):
        if label is None:
            label = family + str(size)
        if opt is None:
            opt = {}
        elem = {
            'family': family,
            'size': size,
            'font': pg.font.SysFont(family, size),
            'anti_aliasing': True,
            'bold':False,
            'italic': False,
            'underline':False
        }
        elem.update(opt)
        # Mise à jour des options visuelles
        if elem['bold']:
            elem['font'].set_bold(True)
        if elem['italic']:
            elem['font'].set_italic(True)
        if elem['underline']:
            elem['font'].set_underline(True)
        self.fonts[label] = elem
        return label

    """
        Ajoute un texte dans la liste des éléments
    """

    def new_text(self, text, font, color, label=None, add_to_page=False):
        if label is None:
            label = len(self.elements)
        elem = {
            'type': 'text',
            'content': text,
            'obj': self.fonts[font]['font'].render(py_encode_font_txt(text), self.fonts[font]['anti_aliasing'], self.colors[color].get_rgb()),
            'nb_usable': -1
        }
        if add_to_page == 'current':
            self.add(self.current_page)
        elif isinstance(add_to_page, int) or isinstance(add_to_page, str):
            self.add(add_to_page)
        self.elements[label] = elem
        return label

    """
        Ajoute une image dans la liste des éléments
    """

    def new_img(self, url, label=None, add_to_page=False):
        if label is None:
            label = len(self.elements)
        bg = pg.image.load(url).convert()
        elem = {
            'type': 'img',
            'content': url,
            'obj': bg,
            'nb_usable': -1
        }
        if add_to_page == 'current':
            self.add(self.current_page)
        elif isinstance(add_to_page, int) or isinstance(add_to_page, str):
            self.add(add_to_page)
        self.elements[label] = elem
        return label

    """
        Ajoute un rectangle dans la liste des éléments
    """

    def new_rect(self, color, border, label=None, add_to_page=False):
        if label is None:
            label = len(self.elements)
        elem = {
            'type': 'rect',
            'color': color,
            'border': border,
            'nb_usable': -1
        }
        if add_to_page == 'current':
            self.add(self.current_page)
        elif isinstance(add_to_page, int) or isinstance(add_to_page, str):
            self.add(add_to_page)
        self.elements[label] = elem
        return label

    """
        Ajoute un cercle dans la liste des éléments
    """

    def new_circle(self, color, radius, border, label=None, add_to_page=False):
        if label is None:
            label = len(self.elements)
        elem = {
            'type': 'circle',
            'color': color,
            'radius': radius,
            'border': border,
            'nb_usable': -1
        }
        if add_to_page == 'current':
            self.add(self.current_page)
        elif isinstance(add_to_page, int) or isinstance(add_to_page, str):
            self.add(add_to_page)
        self.elements[label] = elem
        return label

    """
        Ajoute un remplissage
        param: color couleur à remplir
        param: label de l'élément
        param: add_to_page (défaut False)
        returns: label donné
    """

    def new_fill(self, color, label=None, add_to_page=False):
        if label is None:
            label = len(self.elements)
        elem = {
            'type': 'fill',
            'color': color,
            'nb_usable': -1
        }
        if add_to_page == 'current':
            self.add(self.current_page)
        elif isinstance(add_to_page, int) or isinstance(add_to_page, str):
            self.add(add_to_page)
        self.elements[label] = elem
        return label

    """
        Ajoute un son dans la liste des éléments
    """

    def new_sound(self, url, label=None, add_to_page=False):
        if label is None:
            label = len(self.elements)
        sound = pg.mixer.Sound(url)
        elem = {
            'type': 'sound',
            'url': url,
            'obj': sound,
            'playing': False,
            'nb_usable': -1
        }
        if add_to_page == 'current':
            self.add(self.current_page)
        elif isinstance(add_to_page, int) or isinstance(add_to_page, str):
            self.add(add_to_page)
        self.elements[label] = elem
        return label

    """
        Joue un son
    """

    def play_sound(self, label):
        if not self.elements[label]['playing']:
            self.elements[label]['obj'].play()
            self.elements[label]['playing'] = True

    """
        Arrête un son
    """

    def stop_sound(self, label):
        if self.elements[label]['playing']:
            self.elements[label]['obj'].stop()
            self.elements[label]['playing'] = False

    """
        Retourne True si le mixer est occupé, False sinon
    """

    def is_mixer_busy(self):
        return pg.mixer.get_busy()

    """
        Ajoute un menu dans la liste des éléments
    """

    def new_menu(self, choices, label=None, add_to_page=False):
        if label is None:
            label = len(self.elements)
        elem = {
            'type': 'menu',
            'choices': choices,
            'result': None,
            'nb_usable': -1
        }
        if add_to_page == 'current':
            self.add(self.current_page)
        elif isinstance(add_to_page, int) or isinstance(add_to_page, str):
            self.add(add_to_page)
        self.elements[label] = elem
        return label

    """
        Récupère le résultat du menu demandé, renvoit None si pas de résultat
    """
    def get_menu_result(self, label):
        return self.elements[label]['result']

    """
        Retourne un élément
    """

    def get_element(self, label):
        return self.elements[label]

    """
        Ajoute l'élément à la page donnée
    """

    def add(self, label, x='centered', y='centered', page=None):
        if page is None:
            page = self.current_page
        if label not in self.elements.keys():
            return False
        elem = {
            'label': label,
            'x': x,
            'y': y,
            'visible': True,
            'nb_recursion': -1  # récursion infinie
        }
        self.pages[page]['elements'].append(elem)
        return True

    """
        Ajoute un menu à la page donnée
    """

    def add_menu(self, label, x='centered', y='centered', before_fun=None, after_fun=None, opt=None, vars=None, page=None):
        if page is None:
            page = self.current_page
        if label not in self.elements.keys():
            return False
        if opt is None:
            opt = {}
        if vars is None:
            vars = {}
        elem = {
            'label': label,
            'x': x,
            'y': y,
            'visible': True,
            'nb_recursion': 1,
            'before_fun': before_fun,
            'after_fun': after_fun,
            'vars': vars,
            'opt': opt
        }
        self.pages[page]['elements'].append(elem)
        return True

    """
        Supprime le premier élément de label label demandé sur la fenêtre
    """

    def delete(self, label, page=None):
        if page is None:
            page = self.current_page
        for k in range(len(self.pages[page]['elements'])):
            elem_info = self.pages[page]['elements'][k]
            if elem_info['label'] == label:
                del self.pages[page]['elements'][k]
                return True
        return False

    """
        Affiche tous les éléments d'une page donnée
    """

    def print_page(self, page=None):
        if page is None:
            page = self.current_page
        num = 0
        while num < len(self.pages[page]['elements']):
            num = self.print_elem(num, page)

        if self.is_open():
            pg.display.flip()

    """
        Affiche un élément d'une page
    """

    def print_elem(self, num, page=None):
        if page is None:
            page = self.current_page
        elem_info = self.pages[page]['elements'][num]
        if not self.exists(elem_info['label']):
            return num + 1
        elem = self.elements[elem_info['label']]
        if elem_info['visible'] and elem['nb_usable'] != 0:  # Si l'élément est visible
            if elem['nb_usable'] != -1:
                elem['nb_usable'] -= 1
            if elem_info['nb_recursion'] != 0:  # nb de récursion déterminé et infinie (-1)
                if elem_info['nb_recursion'] > 0:
                    self.pages[page]['elements'][num]['nb_recursion'] -= 1
                if elem['type'] == 'rect':  # Si rectangle à afficher
                    self._print_rect(num, page)
                elif elem['type'] == 'circle':  # Si cercle à afficher
                    self._print_circle(num, page)
                elif elem['type'] == 'fill':
                    self.fill(elem['color'])
                elif elem['type'] == 'menu':  # Si menu à afficher
                    self._print_menu(num, page)
                else:  # Tout autre ressource à afficher
                    p_width, p_height = pg.display.get_surface().get_size()
                    changes = {
                        'top': "0",
                        'left': "0",
                        'right': str(p_width),
                        'bottom': str(p_height),
                        'x_center': str(p_width / 2),
                        'y_center': str(p_height / 2),
                        'self_width': str(elem['obj'].get_rect().width),
                        'self_height': str(elem['obj'].get_rect().height)
                    }
                    x = str(elem_info['x'])
                    y = str(elem_info['y'])
                    if x == 'centered':
                        x = str((p_width - elem['obj'].get_rect().width) / 2)
                    if y == 'centered':
                        y = str((p_height - elem['obj'].get_rect().height) / 2)
                    for k, v in changes.items():
                        x = x.replace(k, v)
                        y = y.replace(k, v)
                    x = eval(x)
                    y = eval(y)
                    self.win.blit(elem['obj'], (x, y))
                if elem_info['nb_recursion'] > 0:
                    self.pages[page]['elements'][num]['nb_recursion'] += 1
                if elem['nb_usable'] == 0:
                    del self.elements[elem_info['label']]
                    del self.pages[page]['elements'][num]
                    num += 1
        return num + 1

    """
        Affichage d'un rectangle
    """

    def _print_rect(self, num, page=None):
        if page is None:
            page = self.current_page
        elem_info = self.pages[page]['elements'][num]
        if elem_info['visible']:  # Si l'élément est visible
            elem = self.elements[elem_info['label']]
            p_width, p_height = pg.display.get_surface().get_size()
            x = elem_info['x']
            y = elem_info['y']
            if not isinstance(x, list) or not isinstance(x, list):
                raise
            x1, x2, y1, y2 = str(x[0]), str(x[1]), str(y[0]), str(y[1])
            changes = {
                'top': "0",
                'left': "0",
                'right': str(p_width),
                'bottom': str(p_height),
                'x_center': str(p_width/2),
                'y_center': str(p_height/2)
            }
            for k, v in changes.items():
                x1 = x1.replace(k, v)
                x2 = x2.replace(k, v)
                y1 = y1.replace(k, v)
                y2 = y2.replace(k, v)
            x1 = eval(x1)
            x2 = eval(x2)
            y1 = eval(y1)
            y2 = eval(y2)
            if isinstance(elem['color'], tuple):
                color = elem['color']
            else:
                color = self.colors[elem['color']].get_rgb()
            pg.draw.rect(self.win, color, [x1, y1, x2, y2], elem['border'])

    """
        Affichage un menu
    """

    def _print_menu(self, num, page=None):
        if page is None:
            page = self.current_page
        elem_info = self.pages[page]['elements'][num]
        elem = self.elements[elem_info['label']]
        menu = elem['choices']
        opt = elem_info['opt']
        options = {
            "font": "default",
            "color": "white",
            "border": None,
            "color_active": "white",
            "border_active": None,
            "font_active": "default",
            "margin": 20
        }
        options.update(opt)  # options d'affichage
        vars = elem_info['vars']
        elem_x, elem_y = elem_info['x'], elem_info['y']
        before_fun, after_fun = elem_info['before_fun'], elem_info['after_fun']
        width_win, height_win = pg.display.get_surface().get_size()

        choix = 0
        done = False
        pressed = False
        clock = pg.time.Clock()
        while not done:
            x, y = elem_x, elem_y
            clock.tick(10)  # Ne boucle que 25 fois/sec
            if before_fun is not None:
                vars.update(before_fun(pg, self, vars, menu))

            # Boucle d'événement
            for event in pg.event.get():
                if event.type == QUIT:
                    done = True
                    self.callback_close()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        done = True
                        pressed = True
                    if event.key == K_UP:
                        choix -= 1
                    if event.key == K_DOWN:
                        choix += 1
            choix %= len(menu)
            k = 0

            if after_fun is not None:
                vars.update(after_fun(pg, self, vars, menu))

            self.refresh()  # On raffréchit la page

            for i, m in enumerate(menu):
                if isinstance(m, list):
                    text = m[0]
                    callback = m[1]
                    if pressed and choix == i and isinstance(callback, str):
                        if callback.lower() == 'close':
                            callback = 'callback_close'
                        callback = "self." + callback + "("
                        for j in range(2, len(m)):
                            callback += str(m[j])
                            if j != len(m) - 1:
                                callback += ", "
                        callback += ")"
                        eval(callback)
                    elif pressed and choix == i and isfunction(callback):
                        params = "("
                        for j in range(2, len(m)):
                            params += str(m[j])
                            if j != len(m) - 1:
                                params += ", "
                        params += ")"
                        callback(eval(params))
                elif isinstance(m, list):
                    text = m[0]
                else:
                    text = m
                if not done and self.is_open():
                    if choix == k:
                        if options["border_active"] is not None:
                            txt = self.fonts[options["font_active"]]['font'].render(py_encode_font_txt(text),
                                                                              self.fonts[options["font_active"]]['anti_aliasing'],
                                                                              self.colors[options["color_active"]].get_rgb(),
                                                                              self.colors[options["border_active"]].get_rgb())
                        else:
                            txt = self.fonts[options["font_active"]]['font'].render(py_encode_font_txt(text),
                                                                              self.fonts[options["font_active"]]['anti_aliasing'],
                                                                              self.colors[options["color_active"]].get_rgb())
                    else:
                        if options["border"] is not None:
                            txt = self.fonts[options["font"]]['font'].render(py_encode_font_txt(text),
                                                                        self.fonts[options["font_active"]]['anti_aliasing'],
                                                                        self.colors[options["color"]].get_rgb(),
                                                                        self.colors[options["border"]].get_rgb())
                        else:
                            txt = self.fonts[options["font"]]['font'].render(py_encode_font_txt(text),
                                                                        self.fonts[options["font_active"]]['anti_aliasing'],
                                                                        self.colors[options["color"]].get_rgb())

                    if elem_x == "centered":
                        x = (width_win - txt.get_rect().width) / 2
                    if y == "centered":
                        y = 0  # TODO: ajouter l'auto-centrage pour les y
                    if k == 0:
                        if 'x' in vars.keys():
                            x = vars['x']
                        if 'y' in vars.keys():
                            y = vars['y']
                    self.win.blit(txt, (x, y))
                    y += txt.get_rect().height + options["margin"]

                    k += 1
            if self.is_open():
                pg.display.flip()
        if not self.is_open():
            self.close()
        self.elements[elem_info['label']]['result'] = choix

    """
        Affichage d'un cercle
    """

    def _print_circle(self, num, page=None):
        if page is None:
            page = self.current_page
        elem_info = self.pages[page]['elements'][num]
        if elem_info['visible']:  # Si l'élément est visible
            elem = self.elements[elem_info['label']]
            p_width, p_height = pg.display.get_surface().get_size()
            x = str(elem_info['x'])
            y = str(elem_info['y'])
            changes = {
                'top': "0",
                'left': "0",
                'right': str(p_width),
                'bottom': str(p_height),
                'x_center': str(p_width / 2),
                'y_center': str(p_height / 2)
            }
            radius = elem['radius']
            if x == 'centered':
                x = str(p_width - elem['radius'])
            if y == 'centered':
                y = str(p_height - elem['radius'])
            for k, v in changes.items():
                x = x.replace(k, v)
                y = y.replace(k, v)
            x = eval(x)
            y = eval(y)
            color = self.colors[elem['color']].get_rgb()
            pg.draw.circle(self.win, color, [x, y], radius, elem['border'])

    """
        Créé un événement
    """

    def event(self, before_fun=None, event_fun=None, after_fun=None, vars=None, page=None):
        if vars is None:
            vars = {}
        done = False
        clock = pg.time.Clock()
        while not done:
            clock.tick(10)  # 25 img/sec
            if before_fun is not None:
                done = before_fun(pg, self, vars)
            for event in pg.event.get():
                if event.type == QUIT:
                    done = True
                if event_fun is not None:
                    done = event_fun(pg, self, vars, event)
            if after_fun is not None:
                done = after_fun(pg, self, vars)
            if self.is_open():
                pg.display.flip()

    """
        Enlève les éléments de la page
    """

    def reset(self):
        color = self.colors[self.pages[self.current_page]['bg']].get_rgb()
        self.win.fill(color)

    """
        Rafréchit la page courante
    """

    def refresh(self):
        self.reset()
        self.print_page()

    """
        Supprime tous les éléments d'une page
        param: page
    """

    def dump_elements(self, page=None):
        if page is None:
            page = self.current_page
        self.pages[page]['elements'] = []

    """
        Remplie la page courante d'une couleur donnée
        param: color str couleur à remplir
    """

    def fill(self, color):
        self.win.fill(self.colors[color].get_rgb())

    """
        Retourne si un élément existe
    """

    def exists(self, label):
        return label in self.elements.keys()

    """
        Exécute une ligne du langage skt
    """

    def execute(self, line, mode='def'):
        mode = '#' + mode
        lines = [mode, line]
        self.parse_template_lang(lines)

    """
        Parser de skt
    """

    def parse_template_lang(self, lines):
        mode = None
        page = {
            'title': None,
            'label': None,
            'width': None,
            'height': None,
            'bg': None
        }
        elements = {'def': {}, 'placing': []}
        """ Récupération des éléments du fichier """
        for line in lines:
            line = line.strip()
            line = line.replace('\n', '')
            if len(line) >= 2 and line[0] != '/' and line[1] != '/':
                if re.match(r'#def', line) is not None:
                    mode = 'def'
                elif re.match(r'#placing', line) is not None:
                    mode = 'placing'
                else:
                    possible_bg = re.findall("#bg\s*\:\s*(\w+)", line)  # Récupère le bg
                    possible_page = re.findall("#page\s*\:\s*(\w+)\(?(\d*)?x?(\d*)?\)?", line)  # Récupère la page
                    possible_titre = re.findall("#title\s*\:\s*([\w\s]+)", line)  # Récupère le titre
                    possible_def = re.findall("(text|rect|img|circle)\s*:\s*(\w+)\((.*)\)\s*(\"([\w\d\s]*)\")?\s*",
                                              line)  # récupère les définitions
                    possible_placing = re.findall("(\w+)\((.*)\)", line)  # Récupère les placements d'éléments
                    # Paramètre de la page #page
                    if mode is None and len(possible_page) == 1:
                        if isinstance(possible_page[0], tuple):
                            page['label'], page['width'], page['height'] = possible_page[0]
                            page['width'] = int(page['width'])
                            page['height'] = int(page['height'])
                        else:
                            page['label'] = possible_page[0]
                            page['label'].replace(' ', '')
                    # #bg
                    elif mode is None and len(possible_bg) == 1:
                        page['bg'] = possible_bg[0]
                    # #title
                    elif mode is None and len(possible_titre) == 1:
                        page['title'] = possible_titre[0].replace('\n', '')
                    # #def
                    elif mode == 'def' and len(possible_def) > 0:
                        if len(possible_def[0]) == 3:
                            type, label, params = possible_def[0]
                            content = None
                        elif len(possible_def[0]) == 5:
                            type, label, params, c, content = possible_def[0]
                        # Récupère les éléments entre guillements
                        first_comma = None
                        last_comma = None
                        after_comma = None
                        for k in range(len(params)):
                            if params[k] == '"' and first_comma is None:
                                first_comma = k
                            elif params[k] == '"':
                                last_comma = k
                            if after_comma is None and last_comma is not None and params[k] == ',':
                                after_comma = k
                        if first_comma is not None:
                            content = params[first_comma + 1:last_comma]
                            params = params[0:first_comma] + params[after_comma + 1:]
                        params.replace(' ', '')  # Enlève les espaces
                        params = params.split(',')  # Sépare par la ','
                        for k in range(len(params)):
                            params[k] = params[k].strip()
                        elements[mode][label] = {
                            'type': type,
                            'params': params,
                            'content': content
                        }
                    # #placing
                    elif mode == 'placing' and len(possible_placing) > 0:
                        label, params = possible_placing[0]
                        params.replace(' ', '')
                        params = params.split(',')
                        for k in range(len(params)):
                            params[k] = params[k].strip()
                        elements[mode].append({
                            'label': label,
                            'params': params
                        })
        """ Parcourt des éléments et création de la page """
        if page['label'] is None:
            label_page = self.current_page
        else:
            label_page = self.new_page(page['title'], page['width'], page['height'], label=page['label'], bg=page['bg'])
        # On ajoute les éléments
        for label, elem in elements['def'].items():
            if elem['type'] == 'text':
                self.new_text(elem['content'], elem['params'][0].replace(' ', ''), elem['params'][1].replace(' ', ''),
                              label)
            elif elem['type'] == 'rect':
                self.new_rect(elem['params'][0].replace(' ', ''), int(elem['params'][1]), label)
            elif elem['type'] == 'circle':
                self.new_circle(elem['params'][0].replace(' ', ''), int(elem['params'][1]), int(elem['params'][2]),
                                label)
            elif elem['type'] == 'img':
                elem['params'][0] = elem['params'][0].replace('IMG_FOLDER', options['IMG_FOLDER']).replace('/', '\\')
                self.new_img(elem['params'][0], label)
        # On ajoute à la page
        for info in elements['placing']:
            label = info['label']
            if self.elements[label]['type'] == 'rect':
                if info['params'][0].isdigit():
                    info['params'][0] = int(info['params'][0])
                if info['params'][1].isdigit():
                    info['params'][1] = int(info['params'][1])
                if info['params'][2].isdigit():
                    info['params'][2] = int(info['params'][2])
                if info['params'][3].isdigit():
                    info['params'][3] = int(info['params'][3])
                self.add(label, [info['params'][0], info['params'][2]],
                         [info['params'][1], info['params'][3]], label_page)
            else:
                if info['params'][0].isdigit():
                    info['params'][0] = int(info['params'][0])
                if info['params'][1].isdigit():
                    info['params'][1] = int(info['params'][1])
                self.add(label, info['params'][0], info['params'][1], label_page)
    """
        Importe un fichier .skt
    """
    def import_template(self, filename, opt=None):
        if opt is None:
            opt = {}
        options = {
            'IMG_FOLDER': os.path.abspath('../res'),
            'SKT_FOLDER': os.path.abspath('../templates')
        }
        options.update(opt)
        if re.match('.*\.skt', filename) is None:
            filename = options['SKT_FOLDER'] + '\\' + filename + '.skt'
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.parse_template_lang(lines)


win = WindowHelper.Instance()