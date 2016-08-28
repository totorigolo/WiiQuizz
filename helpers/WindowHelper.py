# coding: utf8

import os
import re
from inspect import isfunction

import pygame as pg
from pygame.locals import *

from ColorHelper import ColorHelper
from Singleton import Singleton
from tools import py_encode_font_txt, py_encode_title

if not pg.font: print 'Warning, fonts disabled'
if not pg.mixer: print 'Warning, sound disabled'


# TODO: Faire de belles erreurs, en utilisant Dialog pour les afficher
# TODO: Séparer le son du WindowHelper
# TODO: Faire un Ressource Manager, pour une gestion des ressources avancée
# TODO: Les erreurs de pygame sont meilleures, ne pas try si c'est pour raise aussitôt -> il faut résoudre l'erreur ou faire print et la re-raise

@Singleton
class WindowHelper:
    @staticmethod
    def Instance():
        """
        Cette fonction est un workaround pour bénéficier de l'autocomplétion sur cette classe
        :rtype: WindowHelper
        """
        return WindowHelper.Instance()

    def __init__(self):
        self.elements = {}  # éléments (toute sorte !)
        self.images = dict()  # TODO: dict d'images pour les précharger
        self.colors = {}  # couleurs
        self.fonts = {}  # liste des polices
        self.pages = {}  # liste des pages
        self.current_page = -1  # page active
        self.win = None  # Fenêtre pygame
        self.opened = False
        self.resizable = True
        self.templates = dict()
        self.event_posters = []
        pg.init()

    def __del__(self):
        try:
            self.opened = False
            self.close()
            pg.quit()
        except AttributeError:
            pass

    def open_window(self, width=None, height=None, resizable=None):
        """
            Ouvre une nouvelle fenêtre de taille width * height
        """
        if width is None:
            width = 500
        if height is None:
            height = 500
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
        else:
            self.refresh()
        self.opened = True

    def is_open(self):
        return self.opened

    def close(self):
        """
            Ferme la fenêtre
        """
        try:
            pg.display.quit()
        except AttributeError:
            self.opened = False

    def callback_close(self):
        self.opened = False

    def quit(self):
        """
            Ferme la session pygame
        """
        self.__del__()

    def new_page(self, title, width=None, height=None, label=None, bg=None):
        """
            Ajoute une page
            param: title titre de la page
            param: label optional (default: num)
            param: bg optional couleur de fond (default: black)
            returns: label donné
        """
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
        print "New page created with label '%s'." % label
        return label

    def go_to(self, label):
        """
            Change de page
        """
        self.current_page = label
        pg.display.set_caption(py_encode_title(self.pages[label]['title']))
        self.reset()
        self.print_page(label)
        return label

    def page_exists(self, page):
        return page in self.pages.keys()

    def nb_use(self, label, num=1):
        """
            Définit le nombre de fois qu'un élément peut être affiché avant d'être automatiquement supprimé
            param: label de l'élément
            param: num de fois que l'élément peut être utilisé
            return: label
        """
        # TODO: Utiliser les secondes ou un nombre
        self.elements[label]['nb_usable'] = num
        return label

    def new_color(self, color, label=None, overwrite=True):
        """
            Ajoute une couleur dans la liste des couleurs
            param: color type str | ColorHelper | tuple
            param: label optional (default: num)
            returns: label, False si la couleur existe déjà
        """
        if label is None:
            if isinstance(color, str) and (color, color) not in self.colors.items():
                label = color
            else:
                label = len(self.colors)
        if label in self.colors.keys() and not overwrite:
            return False
        if isinstance(color, str) or isinstance(color, tuple):
            self.colors[label] = ColorHelper(color)
        elif isinstance(color, ColorHelper):
            self.colors[label] = color
        else:
            raise ValueError("L'attribut color doit être du type ColorHelper, string ou tuple.")
        return label

    def new_font(self, family, size, label=None, opt=None, overwrite=False):
        """
            Ajoute une police de caractère
            :return label ou False si l'élément existait déjà
        """
        if label is None:
            label = family + str(size)
        if label in self.fonts.keys() and not overwrite:
            return False
        if opt is None:
            opt = {}
        elem = {
            'family': family,
            'size': size,
            'font': pg.font.SysFont(family, size),
            'anti_aliasing': True,
            'bold': False,
            'italic': False,
            'underline': False
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

    def new_text(self, text, font, color, label=None, add_to_page=None,
                 overwrite=True):  # TODO: Possibilité de mettre un fond au texte
        """
            Ajoute un texte dans la liste des éléments
            :return label | False si l'élément existait déjà
        """
        if label is None:
            label = self.get_unused_label()
        if label in self.elements.keys() and not overwrite:
            return False
        try:
            obj = self.fonts[font]['font'].render(py_encode_font_txt(text), self.fonts[font]['anti_aliasing'],
                                                  self.colors[color].get_rgb())
        except Exception as e:
            raise ValueError("Pygame error : %s" % e)
        elem = {
            'type': 'text',
            'color': color,
            'font': font,
            'content': text,
            'obj': obj,
            'nb_usable': -1
        }
        self.elements[label] = elem
        if add_to_page is not None:
            self.add(label, page=add_to_page)
        return label

    def new_img(self, url, alpha=False, label=None, add_to_page=None, overwrite=False):
        """
            Ajoute une image dans la liste des éléments
            :return label | False si l'élément existait déjà
        """
        if label is None:
            label = self.get_unused_label()
        if label in self.elements.keys() and not overwrite:
            return False
        if alpha:
            # try:
            bg = pg.image.load(url).convert_alpha()
            # except Exception as e:
            #     raise ValueError("Can't import image : %s" % e)
            # except:
            #     raise ImportError("The " + url + " image cannot be loaded.")
        else:
            # try:
            bg = pg.image.load(url).convert()
            # except Exception as e:
            #     raise ValueError("Can't import image : %s" % e)
            # except:
            #     raise ImportError("The " + url + " image cannot be loaded.")
        elem = {
            'type': 'img',
            'content': url,
            'alpha': alpha,
            'obj': bg,
            'nb_usable': -1
        }
        self.elements[label] = elem
        if add_to_page is not None:
            self.add(label, page=add_to_page)
        return label

    def new_rect(self, color, border, label=None, add_to_page=None, overwrite=True):
        """
            Ajoute un rectangle dans la liste des éléments
            :return label | False si l'élément existait déjà
        """
        if label is None:
            label = self.get_unused_label()
        if label in self.elements.keys() and not overwrite:
            return False
        elem = {
            'type': 'rect',
            'color': color,
            'border': border,
            'nb_usable': -1
        }
        self.elements[label] = elem
        if add_to_page is not None:
            self.add(label, page=add_to_page)
        return label

    def new_circle(self, color, radius, border, label=None, add_to_page=None, overwrite=True):
        """
            Ajoute un cercle dans la liste des éléments
            :return label | False si l'élément existait déjà
        """
        if label is None:
            label = self.get_unused_label()
        if label in self.elements.keys() and not overwrite:
            return False
        elem = {
            'type': 'circle',
            'color': color,
            'radius': radius,
            'border': border,
            'nb_usable': -1
        }
        self.elements[label] = elem
        if add_to_page is not None:
            self.add(label, page=add_to_page)
        return label

    def new_fill(self, color, label=None, add_to_page=None, overwrite=True):
        """
            Ajoute un remplissage
            param: color couleur à remplir
            param: label de l'élément
            param: add_to_page (défaut False)
            returns: label donné | False si l'élément existait déjà
        """
        if label is None:
            label = self.get_unused_label()
        if label in self.elements.keys() and not overwrite:
            return False
        elem = {
            'type': 'fill',
            'color': color,
            'nb_usable': -1
        }
        self.elements[label] = elem
        if add_to_page is not None:
            self.add(label, page=add_to_page)
        return label

    def new_sound(self, url, label=None, add_to_page=None, overwrite=False):
        """
            Ajoute un son dans la liste des éléments
            :return label | False si l'élément existait déjà
        """
        if label is None:
            label = self.get_unused_label()
        if label in self.elements.keys() and not overwrite:
            return False

        # Tente de charger le son
        sound = pg.mixer.Sound(url)
        if sound.get_length() < 0.001:
            raise ValueError("The " + url + " sound cannot be loaded.")

        elem = {
            'type': 'sound',
            'url': url,
            'obj': sound,
            'playing': False,
            'nb_usable': -1
        }
        self.elements[label] = elem
        if add_to_page is not None:
            self.add(label, page=add_to_page)
        return label

    def play_sound(self, label):
        """
            Joue un son
        """
        # if not self.elements[label]['playing']:
        self.elements[label]['obj'].play()
        # self.elements[label]['playing'] = True

    def stop_sound(self, label):
        """
            Arrête un son
        """
        # if self.elements[label]['playing']:
        self.elements[label]['obj'].stop()
        # self.elements[label]['playing'] = False

    def is_mixer_busy(self):
        """
            Retourne True si le mixer est occupé, False sinon
        """
        return pg.mixer.get_busy()

    def new_menu(self, choices, label=None, add_to_page=None):
        """
            Ajoute un menu dans la liste des éléments
        """
        if label is None:
            label = len(self.elements)
        elem = {
            'type': 'menu',
            'choices': choices,
            'result': None,
            'nb_usable': -1
        }
        self.elements[label] = elem
        if add_to_page == 'current':
            self.add(self.current_page)
        elif isinstance(add_to_page, int) or isinstance(add_to_page, str):
            self.add(add_to_page)
        return label

    def get_menu_result(self, label):
        """
            Récupère le résultat du menu demandé, renvoit None si pas de résultat
        """
        return self.elements[label]['result']

    def get_element(self, label):
        """
            Retourne un élément
        """
        return self.elements[label]

    def edit_color(self, label, color):
        """
            Modifie la couleur d'un élément
        """
        if 'color' in self.elements[label].keys():
            if self.elements[label]['type'] == 'text':
                font = self.elements[label]['font']
                text = self.elements[label]['content']
                try:
                    self.elements[label]['obj'] = self.fonts[font]['font'].render(py_encode_font_txt(text),
                                                                                  self.fonts[font]['anti_aliasing'],
                                                                                  self.colors[color].get_rgb())
                except Exception as e:
                    raise ValueError("The color cannot be changed : %s" % e)
            self.elements[label]['color'] = color
            return True
        return False

    def edit_text(self, label, text):
        """
            Modifie le contenu d'un élément
        """
        if self.elements[label]['type'] == 'text':
            font = self.elements[label]['font']
            color = self.elements[label]['color']
            self.elements[label]['content'] = text
            try:
                self.elements[label]['obj'] = self.fonts[font]['font'].render(py_encode_font_txt(text),
                                                                              self.fonts[font]['anti_aliasing'],
                                                                              self.colors[color].get_rgb())
            except Exception as e:
                raise ValueError("The text cannot be changed : %s" % e)
            return True
        return False

    def edit_border(self, label, border):
        """
            Modifie la bordure d'un élément
        """
        if 'border' in self.elements[label].keys():
            self.elements[label]['border'] = border
            return True
        return False

    def add(self, label, x='centered', y='centered', page=None):
        """
            Ajoute l'élément à la page donnée
            :type x: Any
            :type y: Any
        """
        if page is None or page == 'current':
            page = self.current_page
        if label not in self.elements.keys():
            raise ValueError("The element to add does not exist.")
        elem = {
            'label': label,
            'x': x,
            'y': y,
            'visible': True,
            'nb_recursion': -1  # récursion infinie
        }
        self.pages[page]['elements'].append(elem)
        return True

    def add_menu(self, label, x='centered', y='centered', before_fun=None, after_fun=None, opt=None, vars=None,
                 page=None):
        """
            Ajoute un menu à la page donnée
        """
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

    def delete(self, label, page=None):
        """
            Supprime le premier élément de label label demandé sur la fenêtre
        """
        # TODO: Faire des tests
        # TODO: Si son, le stoper
        if page is None:
            page = self.current_page

        def delete_from_page_elements(self, page, label):
            try:
                for elem_info in self.pages[page]['elements']:
                    try:
                        if elem_info['label'] == label:
                            self.pages[page]['elements'].remove(elem_info)
                            return True
                    except KeyError:
                        print "delete() : problem when deleting element."
            except KeyError:
                print "delete() : page %s doesn't exist." % page
            return False

        def delete_from_elements(self, label):
            if label in self.elements:
                self.elements.pop(label)
                return True
            print "delete() : element %s not in win.elements." % label
            return False

        r1 = delete_from_elements(self, label)
        r2 = delete_from_page_elements(self, page, label)
        return r1 and r2

    def print_page(self, page=None):
        """
            Affiche tous les éléments d'une page donnée
            :return: False si la page n'existe pas, True sinon
        """
        if page is None:
            page = self.current_page
        if page not in self.pages:
            return False
        num = 0
        while num < len(self.pages[page]['elements']):
            num = self.print_elem(num, page)

        if self.is_open():
            pg.display.flip()

        return True

    def print_elem(self, num, page=None):
        """
            Affiche un élément d'une page
        """
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

    def _print_rect(self, num, page=None):
        """
            Affichage d'un rectangle
        """
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
                'x_center': str(p_width / 2),
                'y_center': str(p_height / 2)
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

    def _print_menu(self, num, page=None):
        """
            Affichage un menu
        """
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
            clock.tick(10)  # Ne boucle que 10 fois/sec
            if before_fun is not None:
                vars.update(before_fun(pg, self, vars, menu))

            # Boucle d'événement
            for ep in self.event_posters:
                ep.post_events()
            if 'event_poster' in opt:
                opt['event_poster'].post_events()
            for event in pg.event.get():
                if event.type == QUIT:
                    done = True
                    self.callback_close()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        done = True
                        pressed = True
                    elif event.key == K_UP:
                        choix -= 1
                    elif event.key == K_DOWN:
                        choix += 1
                elif event.type == USEREVENT:  # TODO: Correspond aux Wiimotes (renommer USEREVENT)
                    if event.wiimote_id == 'master' and event.pressed:
                        if event.btn == 'HAUT':
                            choix -= 1
                        elif event.btn == 'BAS':
                            choix += 1
                        elif event.btn == 'A':
                            done = True
                            pressed = True
                elif event.type == VIDEORESIZE:
                    width_win, height_win = event.w, event.h
                    self.open_window(width_win, height_win)  # On re-taille la fenêtre
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
                                                                                    self.fonts[options["font_active"]][
                                                                                        'anti_aliasing'],
                                                                                    self.colors[options[
                                                                                        "color_active"]].get_rgb(),
                                                                                    self.colors[options[
                                                                                        "border_active"]].get_rgb())
                        else:
                            txt = self.fonts[options["font_active"]]['font'].render(py_encode_font_txt(text),
                                                                                    self.fonts[options["font_active"]][
                                                                                        'anti_aliasing'],
                                                                                    self.colors[options[
                                                                                        "color_active"]].get_rgb())
                    else:
                        if options["border"] is not None:
                            txt = self.fonts[options["font"]]['font'].render(py_encode_font_txt(text),
                                                                             self.fonts[options["font_active"]][
                                                                                 'anti_aliasing'],
                                                                             self.colors[options["color"]].get_rgb(),
                                                                             self.colors[options["border"]].get_rgb())
                        else:
                            txt = self.fonts[options["font"]]['font'].render(py_encode_font_txt(text),
                                                                             self.fonts[options["font_active"]][
                                                                                 'anti_aliasing'],
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

    def _print_circle(self, num, page=None):
        """
            Affichage d'un cercle
        """
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

    def event(self, before_fun=None, event_fun=None, after_fun=None, vars=None, page=None, fps=10):
        """
            Créé un événement
        """
        if vars is None:
            vars = {}
        done = False
        clock = pg.time.Clock()
        while not done:
            clock.tick(fps)  # Limite le framerate

            if before_fun is not None:
                done = done or before_fun(pg, self, vars)

            for ep in self.event_posters:
                ep.post_events()
            if 'event_poster' in vars:
                vars['event_poster'].post_events()
            for event in pg.event.get():
                if event.type == QUIT:
                    done = True
                    self.callback_close()
                elif event.type == VIDEORESIZE:
                    self.open_window(event.w, event.h)
                if event_fun is not None:
                    done = done or event_fun(pg, self, vars, event)

            if after_fun is not None:
                done = done or after_fun(pg, self, vars)

            if self.is_open():
                pg.display.flip()
            if not self.is_open():
                break
        if not self.is_open():
            self.close()

    def register_event_poster(self, event_poster):
        """
        Enregistre un Event Poster, c'est-à-dire un objet qui va ajouter des éléments dans pygame.event
        :param event_poster: Un objet ayant une fonction post_events()
        """
        self.event_posters.append(event_poster)
        print "Event poster added : %s" % event_poster

    def remove_event_poster(self, event_poster):
        """
        Supprime un Event Poster, c'est-à-dire un objet qui ajoute des éléments dans pygame.event
        :param event_poster: Un objet ayant une fonction post_events()
        """
        try:
            self.event_posters.remove(event_poster)
            print "Event poster removed : %s" % event_poster
        except ValueError:
            print "Event poster absent from list : %s" % event_poster

    def reset(self):
        """
            Enlève les éléments de la page
        """
        try:
            color = self.colors[self.pages[self.current_page]['bg']]
        except KeyError:
            # TODO: Utiliser une erreur perso
            print "Can't reset(), either no current page or no background color."
        else:
            self.win.fill(color.get_rgb())

    def refresh(self):
        """
            Rafréchit la page courante
        """
        self.reset()
        self.print_page()

    def dump_elements(self, page=None):
        """
            Supprime tous les éléments d'une page
            param: page, par défaut l'actuelle
        """
        if page is None:
            page = self.current_page
        if page not in self.pages:
            print "dump_elements() : la page %s n'existe pas" % page
            return
        try:
            for label in [e['label'] for e in self.pages[page]['elements']]:
                r = self.delete(label, page)
                print "Element %s deleted : %s" % (label, r)
        except KeyError:
            print 'dump_elements() : la page %s est invalide' % page

    def delete_page(self, page=None):
        """
            Supprime tous les éléments d'une page
            param: page, par défaut l'actuelle
        """
        if page is None:
            page = self.current_page
        if page == self.current_page:
            self.current_page = -1
        if page not in self.pages:
            print "delete_page() : the page %s doesn't exists" % page
            return False
        self.dump_elements(page)
        self.pages.pop(page)
        print "Page %s deleted." % page
        return True

    def fill(self, color):
        """
            Remplie la page courante d'une couleur donnée
            param: color str couleur à remplir
        """
        self.win.fill(self.colors[color].get_rgb())

    def exists(self, label):
        """
            Retourne si un élément existe
        """
        return label in self.elements.keys()

    def execute(self, line, mode='def'):
        """
            Exécute une ligne du langage skt
        """
        mode = '#' + mode
        lines = [mode, line]
        self.parse_template(lines)

    def parse_template(self, name, lines, file=None, opt=None):
        """
            Parser de skt
        """
        if opt is None:
            opt = {}
        options = {}
        options.update(opt)
        mode = None
        page = {
            'title': None,
            'label': None,
            'width': None,
            'height': None,
            'bg': None
        }
        elements = {'colors_and_fonts': {}, 'def': {}, 'placing': []}
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
                    possible_def = re.findall(
                        "(text|rect|img|circle|font|color)\s*:\s*(\w+)\((.*)\)\s*(\"([\w\d\s]*)\")?\s*",
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
                        if type == 'color' or type == 'font':
                            sub_mode = 'colors_and_fonts'
                        else:
                            sub_mode = mode
                        elements[sub_mode][label] = {
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
            if self.current_page == -1:
                raise ValueError('No active page found. Use the go_to method before importing the template file.')
            label_page = self.current_page
        else:
            label_page = self.new_page(page['title'], page['width'], page['height'], label=page['label'], bg=page['bg'])

        if name not in self.templates:
            self.templates[name] = {'page': None, 'elements': []}
        self.templates[name]['page'] = label_page

        # On ajoute les couleurs et fonts
        for label, elem in elements['colors_and_fonts'].items():
            if elem['type'] == 'color':
                try:
                    if len(elem['params']) == 3 and elem['params'][0].isdigit() and elem['params'][1].isdigit() and \
                            elem['params'][2].isdigit():
                        self.new_color((int(elem['params'][0]), int(elem['params'][1]), int(elem['params'][2])), label)
                    elif len(elem['params']) == 1:
                        self.new_color(int(elem['params'][0]), label)
                except Exception as e:
                    if file is not None:
                        raise ValueError(
                            'The options for ' + label + ' in the file ' + file + ' are incorrect. : %s' % e)
                    else:
                        raise ValueError('The options for ' + label + ' are incorrect : %s' % e)
            elif elem['type'] == 'font':
                try:
                    self.new_font(elem['params'][0], int(elem['params'][1]), label)
                except Exception as e:
                    if file is not None:
                        raise ValueError(
                            'The options for ' + label + ' in the file ' + file + ' are incorrect : %s' % e)
                    else:
                        raise ValueError('The options for ' + label + ' are incorrect : %s' % e)
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
                elem['params'][0] = elem['params'][0].replace('IMG_FOLDER', options['IMG_FOLDER']).replace('\\', '/')
                if len(elem['params']) == 2 and elem['params'][1] == 'True':
                    self.new_img(elem['params'][0], alpha=elem['params'][1], label=label)
                else:
                    self.new_img(elem['params'][0], label=label)

        # On ajoute à la page
        for info in elements['placing']:
            label = info['label']
            self.templates[name]['elements'].append(label)
            if label not in self.elements:
                print "parse_template('%s') : Le label %s n'existe pas." % (name, label)
                continue
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

    def import_template(self, name, filename=None,
                        opt=None):  # TODO: ajouter le page_label pour dire dans quelle page ajouter les éléments
        """
            Importe un fichier .skt
        """

        project_dir = os.path.abspath('/'.join((os.path.dirname(os.path.abspath(__file__)), '..')))

        if opt is None:
            opt = {}
        options = {
            'IMG_FOLDER': project_dir + '/res',
            'SKT_FOLDER': project_dir + '/templates'
        }
        options.update(opt)

        if filename is None:
            # if re.match('.*\.skt', name) is None:
            options['SKT_FOLDER'] = options['SKT_FOLDER'].replace('\\', '/')
            filename = options['SKT_FOLDER'] + '/' + name + '.skt'

        with open(filename, 'r') as file:
            lines = file.readlines()
            self.parse_template(name, lines, filename, options)

    def undo_template(self, name):
        """
        Supprime tous les éléments ajoutés par le dernier import_template à la vue
        :return: False si le template label n'existe pas, sinon True
        """
        if name not in self.templates:
            return False
        for element_label in self.templates[name]['elements']:
            self.delete(element_label, self.templates[name]['page'])

    def get_unused_label(self):
        new_label = len(self.elements)
        while new_label in self.elements:
            new_label += 1
        return new_label
