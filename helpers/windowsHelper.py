<<<<<<< Updated upstream:helpers/windowsHelper.py
# coding: utf8

import pygame as pg
from pygame.locals import *
from colorHelper import colorHelper
from tools import py_encode_font_txt, py_encode_title
from inspect import isfunction

if not pg.font: print 'Warning, fonts disabled'


class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class windowsHelper:
    """ Lance une fenêtre de taille width x height """

    def __init__(self):
        pg.init()

    def open(self, width, height, title=None, resizable=True, autoFlip=True, bg=None):
        if bg is None:
            bg = colorHelper("black")
        if resizable:
            self.window = pg.display.set_mode((width, height), RESIZABLE)
        else:
            self.window = pg.display.set_mode((width, height))

        if not isinstance(bg, tuple):
            bg = bg.getTuple()

        self.ppties = (width, height, resizable, autoFlip)
        self.bg = [bg]
        self.page = 0
        self.lastPage = 0
        self.autoFlip = autoFlip
        self.elements = [{}]
        self.elementsCounter = 0
        self.titles = [title]
        self.fonts = {}
        self.colors = {}
        self.vars = {}
        self.actions = [[]]
        self.toQuit = False

        self.reset(keepElem=True)

        self.add_font("Arial", 10, "default")
        self.add_color("white", colorHelper("white"))
        self.add_color("black", colorHelper("black"))
        self.go_to_page(0)

    def __del__(self):
        self.quit()

    def quit(self):
        pg.display.quit()
        pg.quit()

    """ Ajoute une police
        param: nom string police de caratère default : Arial
        param: size int taille de la police default : 10
        param: label string label de la police default: None """

    def add_font(self, nom="Arial", size=10, label=None, opt=None):
        if opt is None:
            opt = {}
        options = {
            "bold": False,
            "italic": False,
            "underline": False,
            "antialiasing": True
        }
        options.update(opt)
        if label is None:
            label = nom + str(size)
        self.fonts[label] = (pg.font.SysFont(nom, size), options["antialiasing"])
        if options["bold"]:
            self.fonts[label][0].set_bold()
        if options["italic"]:
            self.fonts[label][0].set_italic()
        if options["underline"]:
            self.fonts[label][0].set_underline()

    """ Ajoute une couleur
        param: nom string label de la couleur
        param: color tuple | colorHelper """

    def add_color(self, nom, color):
        if isinstance(color, tuple):
            self.colors[nom] = color
        else:
            self.colors[nom] = color.getTuple()

    """ Ajoute du texte
        param: text string texte à ajouter
        param: font label de la police choisie (doit être ajouté avec la méthode addFont)
        param: color label de la couleur choisie (doit être ajouté avec la méthode addColor)
        params: x, y default: 0, 0
        param: page int numéro de page à afficher default: page active
        param: label string label du texte default: le numéro de l'élément 
        param: opt dict options : widthcentered et heightcentered"""

    def add_text(self, text, font, color, x=0, y=0, page=None, label=None, opt=None):
        if opt is None:
            opt = {}
        options = {
            "widthcentered": False,
            "heightcentered": False
        }
        options.update(opt)
        width, height = pg.display.get_surface().get_size()
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        text = self.fonts[font][0].render(py_encode_font_txt(text), self.fonts[font][1], self.colors[color])
        if options["widthcentered"]:
            x = (width - text.get_rect().width) / 2
        if options["heightcentered"]:
            y = (height - text.get_rect().height) / 2
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
        self.elements[page][label] = (text, None, None, None, x, y)
        if page == self.page:  # Si l'on est sur la page du texte, on l'affiche directement
            self.window.blit(text, (x, y))
            if self.autoFlip:
                pg.display.flip()

        return text.get_rect()

    """ Ajoute une l'image url à x, y (point ancrage haut gauche), colorkey de type colorHelper"""

    def add_img(self, url, x, y, page=None, convert=True, alpha=False, colorkey=False, label=None, printElem=True):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        if colorkey != False:
            if not isinstance(colorkey, tuple):
                colorkey = colorkey.getTuple()
            pg.image.set_colorkey(colorkey.getTuple())
        if alpha:
            bg = pg.image.load(url).convert_alpha()
        elif convert:
            bg = pg.image.load(url).convert()
        else:
            bg = pg.image.load(url)
        if printElem:
            if self.page == page:
                self.window.blit(bg, (x, y))
            if self.autoFlip:
                pg.display.flip()
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
        self.elements[page][label] = (bg, convert, alpha, colorkey, x, y)


    def edit_img(self, label, page=None, x=None, y=None):
        if page is None:
            page = self.page
        if x is not None:
            self.elements[page][label][4] = x
        if y is not None:
            self.elements[page][label][5] = y


    def add_rect(self, color, x1, y1, x2, y2, border_width, page=None, label=None):
        if page is None:
            page = self.page
        if isinstance(color, str):
            color = self.colors[color]
        elif not isinstance(color, tuple):
            color = color.getTuple()
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
        self.elements[page][label] = ("rect", color, x1, y1, x2, y2, border_width)
        if page == self.page:
            self.print_element(label, page, autoFlip=self.autoFlip)


    def add_circle(self, color, c_x, c_y, radius, border_width, page=None, label=None):
        if page is None:
            page = self.page
        if isinstance(color, str):
            color = self.colors[color]
        elif not isinstance(color, tuple):
            color = color.getTuple()
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
        self.elements[page][label] = ("circle", color, c_x, c_y, radius, border_width)
        if page == self.page:
            self.print_element(label, page, autoFlip=self.autoFlip)

    """
    param: aa bool anti-aliasing
    """

    def add_line(self, color, o_x, o_y, e_x, e_y, border_width, aa=True, page=None, label=None):
        if page is None:
            page = self.page
        if isinstance(color, str):
            color = self.colors[color]
        elif not isinstance(color, tuple):
            color = color.getTuple()
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
        self.elements[page][label] = ("line", color, o_x, o_y, e_x, e_y, border_width, aa)
        if page == self.page:
            self.print_element(label, page, autoFlip=self.autoFlip)

    """
        [["Menu 1", function, param1, param2], ["Menu 2", "addText", param1, param2, ...]]
    """

    def add_menu(self, x=0, y=0, menu=[], before_fun=None, after_fun=None, vars=None, opt=None):
        if opt is None:
            opt = {}
        if vars is None:
            vars = {}
        if len(menu) == 0:
            return False
        options = {
            "font": "default",
            "color": "white",
            "border": None,
            "colorActive": "white",
            "borderActive": None,
            "fontActive": "default",
            "widthcentered": False,
            "margin": 20
        }
        options.update(opt)
        width_win, height_win = pg.display.get_surface().get_size()
        choix = 0
        done = False
        pressed = False
        ax, ay = x, y
        clock = pg.time.Clock()
        while not done:
            clock.tick(25)  # Ne boucle que 25 fois/sec
            x, y = ax, ay
            if before_fun is not None:
                vars.update(before_fun(pg, self, vars, menu))
            for event in pg.event.get():
                if event.type == QUIT:
                    done = True
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

            self.reset(True, True)

            if after_fun is not None:
                vars.update(after_fun(pg, self, vars, menu))

            for m in menu:
                if isinstance(m, list):
                    text = m[0]
                    callback = m[1]
                    if pressed and choix == k and isinstance(callback, str):
                        callback = "self." + callback + "("
                        for i in range(2, len(m)):
                            callback += str(m[i])
                            if i != len(m) - 1:
                                callback += ", "
                        callback += ")"
                        eval(callback)
                    elif pressed and choix == k and isfunction(callback):
                        params = "("
                        for i in range(2, len(m)):
                            params += str(m[i])
                            if i != len(m) - 1:
                                params += ", "
                        params += ")"
                        callback(eval(params))
                else:
                    text = m
                if not done:
                    if choix == k:
                        if options["borderActive"] is not None:
                            txt = self.fonts[options["fontActive"]][0].render(py_encode_font_txt(text),
                                                                              self.fonts[options["fontActive"]][1],
                                                                              self.colors[options["colorActive"]],
                                                                              self.colors[options["borderActive"]])
                        else:
                            txt = self.fonts[options["fontActive"]][0].render(py_encode_font_txt(text),
                                                                              self.fonts[options["fontActive"]][1],
                                                                              self.colors[options["colorActive"]])
                    else:
                        if options["border"] is not None:
                            txt = self.fonts[options["font"]][0].render(py_encode_font_txt(text),
                                                                        self.fonts[options["fontActive"]][1],
                                                                        self.colors[options["color"]],
                                                                        self.colors[options["border"]])
                        else:
                            txt = self.fonts[options["font"]][0].render(py_encode_font_txt(text),
                                                                        self.fonts[options["fontActive"]][1],
                                                                        self.colors[options["color"]])

                    if options["widthcentered"]:
                        x = (width_win - txt.get_rect().width) / 2
                    if k == 0:
                        if 'x' in vars.keys():
                            x = vars['x']
                        if 'y' in vars.keys():
                            y = vars['y']

                    self.window.blit(txt, (x, y))
                    y += txt.get_rect().height + options["margin"]

                    k += 1

            pg.display.flip()
        return choix

    def event(self, fun_bef, fun_events, fun_after, opt=None):
        if opt is None:
            opt = {}
        done = False
        clock = pg.time.Clock()
        while not done:
            clock.tick(25)
            done = fun_bef(pg, self, opt)
            for event in pg.event.get():
                if event.type == QUIT:
                    done = True
                done = fun_events(event, pg, self, opt)

            done = fun_after(pg, self, opt)

            pg.display.flip()
        if self.toQuit:
            self.quit()

    def change_title(self, title, page=None):
        if page is None:
            page = self.page
        self.titles[page] = title
        if page == self.page:
            pg.display.set_caption(py_encode_title(title))

    def change_properties(self, width=None, height=None, resizable=None, autoFlip=None, bg=None):
        a_width, a_height, a_resizable, a_autoFlip = self.ppties
        a_bg = self.bg[self.page]
        if width is not None:
            a_width = width
        if height is not None:
            a_height = height
        if resizable is not None:
            a_resizable = resizable
        if autoFlip is not None:
            a_autoFlip = autoFlip
        if bg is not None:
            a_bg = bg
        if a_resizable:
            self.window = pg.display.set_mode((a_width, a_height), RESIZABLE)
        else:
            self.window = pg.display.set_mode((a_width, a_height))
        self.autoFlip = a_autoFlip
        self.bg[self.page] = bg
        self.go_to_page(self.page)

    def del_element(self, i, page=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        self.reset(keepElem=True)
        del self.elements[page][i]
        for k in range(len(self.elements[page])):
            self.print_element(k, page)
        if self.autoFlip:
            pg.display.flip()

    """ Remplie la fenêtre d'une couleur voulue """

    def fill(self, color, page=None):
        if color is None:
            color = (0, 0, 0)
        if isinstance(color, str):
            color = self.colors[color]
        elif not isinstance(color, tuple):
            color = color.getTuple()
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        if self.page == page:
            self.window.fill(color)
        else:
            self.actions[page].append("self.fill(" + str(color) + ", " + str(page) + ")")

    def print_element(self, i, page=None, autoFlip=False, x=None, y=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        if self.elements[page][i][0] == "rect":
            type, color, x1, y1, x2, y2, border_width = self.elements[page][i]
            pg.draw.rect(self.window, color, [x1, y1, x2, y2], border_width)
        elif self.elements[page][i][0] == "circle":
            type, color, c_x, c_y, radius, border_width = self.elements[page][i]
            pg.draw.circle(self.window, color, [c_x, c_y], radius, border_width)
        elif self.elements[page][i][0] == "line":
            type, color, o_x, o_y, e_x, e_y, border_width, aa = self.elements[page][i]
            if aa:  # anti-aliasing
                pg.draw.aaline(self.window, color, [o_x, o_y], [e_x, e_y], border_width)
            else:
                pg.draw.line(self.window, color, [o_x, o_y], [e_x, e_y], border_width)
        else:
            bg, convert, alpha, colorkey, nx, ny = self.elements[page][i]
            if x is not None:
                nx = x
            if y is not None:
                ny = y
            self.window.blit(bg, (nx, ny))
        if autoFlip:
            pg.display.flip()

    """ Ajoute une nouvelle page
        param: title string titre de la page
        param: goTo boolean si True, la fenêtre ira vers cette page après appel default: True"""

    def new_page(self, title=None, bg=None, goTo=True):
        if bg is None:
            bg = self.bg[-1]
        self.lastPage += 1
        self.elements.append({})
        self.titles.append(title)
        self.actions.append([])
        self.bg.append(bg)
        if goTo:
            self.reset(keepElem=True)
            self.page = self.lastPage
            if title is not None:
                pg.display.set_caption(py_encode_title(title))

    """ Ouvre la page k """

    def go_to_page(self, k):
        self.page = k
        self.reset(keepElem=True)
        title = self.titles[k]
        if title is not None:
            pg.display.set_caption(py_encode_title(title))
        for cle, val in self.elements[k].items():
            self.print_element(cle, k)
        for action in self.actions[k]:
            eval(action)
        self.actions[k] = []
        self.flip()

    """ Renvoie l'élément demandé """

    def get_element(self, i, page=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        return self.elements[page][i][0]

    """ Renvoie l'instance Rect de l'élément demandé """

    def get_element_rect(self, i, page=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        return self.elements[page][i][0].get_rect()

    def move_element(self, i, x, y, page=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        rec = self.get_element_rect(i, page).move(x, y)
        self.window.blit(self.get_element(i, page), rec)
        bg, convert, alpha, colorkey, ax, ay = self.elements[page][i]
        self.elements[page][i] = bg, convert, alpha, colorkey, x, y
        self.reset(True, page)
        for cle, val in self.elements[page].items():
            self.print_element(cle, page)
        if self.autoFlip:
            pg.display.flip()

    """ Liste les éléments à l'écran de l'indice i à j ; liste tous les éléments si non renseignés """

    def list_elements(self, page=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        return self.elements[page]

    """ Renvoie une fenêtre vide """

    def reset(self, keepElem=False, printElem=False, page=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        self.fill(self.bg[page], page)
        if printElem:
            for cle, val in self.elements[page].items():
                self.print_element(cle, page)
        if not keepElem:
            self.elements[page] = {}

    """ Retourne si un élément existe déjà """

    def exists(self, i, page=None):
        if page is None:
            page = self.page
        if i in self.elements[page].keys():
            return True
        return False

    """ Met à jour la fenêtre """

    def flip(self):
        pg.display.flip()
=======
# coding: utf8

import pygame as pg
from pygame.locals import *
from ColorHelper import ColorHelper
from tools import py_encode_font_txt, py_encode_title
from inspect import isfunction

if not pg.font: print 'Warning, fonts disabled'
if not pg.mixer: print 'Warning, sound disabled'


class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class WindowHelper:

    def __init__(self):
        self.elements = {}  # éléments (toute sorte !)
        self.colors = {}  # couleurs
        self.musics = {}  # musiques
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
        self.quit()

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
        self.new_font('Arial', 30, 'default')
        self.new_color('black')
        self.new_color('white')

    """
        Ferme la fenêtre
    """
    def close(self):
        pg.display.quit()

    """
        Ferme la session pygame
    """
    def quit(self):
        self.close()
        pg.quit()
        self.opened = False

    """
        Ajoute une page
        param: title titre de la page
        param: label optional (default: num)
        param: bg optional couleur de fond (default: black)
        returns: label donné
    """

    def new_page(self, title, width=None, height=None, label=None, bg=None):
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
            elem['font'].set_bold()
        if elem['italic']:
            elem['font'].set_italic()
        if elem['underline']:
            elem['font'].set_underline()
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
            'obj': self.fonts[font]['font'].render(py_encode_font_txt(text), self.fonts[font]['anti_aliasing'], self.colors[color].get_rgb())
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
            'obj': bg
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
            'border': border
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
            'border': border
        }
        if add_to_page == 'current':
            self.add(self.current_page)
        elif isinstance(add_to_page, int) or isinstance(add_to_page, str):
            self.add(add_to_page)
        self.elements[label] = elem
        return label

    """
        Ajoute un menu dans la liste des éléments
    """

    def new_menu(self, choices, label=None, add_to_page=False):
        if label is None:
            label = len(self.elements)
        elem = {
            'type': 'menu',
            'choices': choices,
            'result': None
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
        return  self.elements[label]['result']

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
        Affiche tous les éléments d'une page donnée
    """

    def print_page(self, page=None):
        if page is None:
            page = self.current_page
        for num in range(len(self.pages[page]['elements'])):
            self.print_elem(num, page)

    """
        Affiche un élément d'une page
    """

    def print_elem(self, num, page=None):
        if page is None:
            page = self.current_page
        elem_info = self.pages[page]['elements'][num]
        if elem_info['visible']:  # Si l'élément est visible
            if elem_info['nb_recursion'] != 0:  # nb de récursion déterminé et infinie (-1)
                if elem_info['nb_recursion'] > 0:
                    self.pages[page]['elements'][num]['nb_recursion'] -= 1
                elem = self.elements[elem_info['label']]
                if elem['type'] == 'rect':  # Si rectangle à afficher
                    self._print_rect(num, page)
                elif elem['type'] == 'circle':  # Si cercle à afficher
                    self._print_circle(num, page)
                elif elem['type'] == 'menu':  # Si menu à afficher
                    self._print_menu(num, page)
                else:  # Tout autre ressource à afficher
                    p_width, p_height = pg.display.get_surface().get_size()
                    x = elem_info['x']
                    y = elem_info['y']
                    if x == 'centered':
                        x = (p_width - elem['obj'].get_rect().width) / 2
                    if y == 'centered':
                        y = (p_height - elem['obj'].get_rect().height) / 2
                    self.win.blit(elem['obj'], (x, y))
                    pg.display.flip()
                if elem_info['nb_recursion'] is not None:
                    self.pages[page]['elements'][num]['nb_recursion'] += 1

    """
        Affichage d'un rectangle
    """

    def _print_rect(self, num, page=None):
        if page is None:
            page = self.current_page
        elem_info = self.pages[page]['elements'][num]
        if elem_info['visible']:  # Si l'élément est visible
            elem = self.elements[elem_info['label']]
            x = elem_info['x']
            y = elem_info['y']
            if not isinstance(x, list) or not isinstance(x, list):
                raise
            color = self.colors[elem['color']].get_rgb()
            pg.draw.rect(self.win, color, [x[0], y[0], x[1], y[1]], elem['border'])
            pg.display.flip()

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
            clock.tick(25)  # Ne boucle que 25 fois/sec
            if before_fun is not None:
                vars.update(before_fun(pg, self, vars, menu))

            # Boucle d'événement
            for event in pg.event.get():
                if event.type == QUIT:
                    done = True
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

            self.refresh()  # On raffréchit la page

            if after_fun is not None:
                vars.update(after_fun(pg, self, vars, menu))

            for m in menu:
                if isinstance(m, list):
                    text = m[0]
                    callback = m[1]
                    if pressed and choix == k and isinstance(callback, str):
                        callback = "self." + callback + "("
                        for i in range(2, len(m)):
                            callback += str(m[i])
                            if i != len(m) - 1:
                                callback += ", "
                        callback += ")"
                        eval(callback)
                    elif pressed and choix == k and isfunction(callback):
                        params = "("
                        for i in range(2, len(m)):
                            params += str(m[i])
                            if i != len(m) - 1:
                                params += ", "
                        params += ")"
                        callback(eval(params))
                else:
                    text = m
                if not done:
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
            pg.display.flip()
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
            x = elem_info['x']
            y = elem_info['y']
            radius = elem['radius']
            if x == 'centered':
                x = p_width - elem['radius']
            if y == 'centered':
                y = p_height - elem['radius']
            color = self.colors[elem['color']].get_rgb()
            pg.draw.circle(self.win, color, [x, y], radius, elem['border'])
            pg.display.flip()

    """
        Créé un événement
    """

    def event(self, before_fun=None, event_fun=None, after_fun=None, vars=None, page=None):
        if vars is None:
            vars = {}
        done = False
        clock = pg.time.Clock()
        while not done:
            clock.tick(25)  # 25 img/sec
            done = before_fun(pg, self, vars)
            for event in pg.event.get():
                if event.type == QUIT:
                    done = True
                done = event_fun(pg, self, vars, event)

            done = after_fun(pg, self, vars)
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
>>>>>>> Stashed changes:helpers/WindowHelper.py
