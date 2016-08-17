# coding: utf8

import pygame as pg
from pygame.locals import *
from ColorHelper import ColorHelper
from tools import py_encode_font_txt, py_encode_title
from inspect import isfunction

if not pg.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


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
    """ Lance une fenêtre de taille width x height """

    def __init__(self):
        self.bg = None
        self.autoFlip = None
        self.page = 0
        self.lastPage = 0
        self.elements = [{}]
        self.elementsCounter = 0
        self.titles = None
        self.fonts = {}
        self.colors = {}
        self.vars = {}
        self.actions = [[]]
        self.toQuit = False
        self.properties = ()
        self.opened = False

    def open(self, width, height, title=None, resizable=True, autoFlip=True, bg=None):
        if not self.opened:
            pg.init()
        if bg is None:
            bg = ColorHelper("black")
        if resizable:
            self.window = pg.display.set_mode((width, height), RESIZABLE)
        else:
            self.window = pg.display.set_mode((width, height))

        if not isinstance(bg, tuple):
            bg = bg.get_rgb()

        self.properties = (width, height, resizable, autoFlip)
        self.autoFlip = autoFlip
        if not self.opened:
            self.bg = [bg]
            self.titles = [title]

            self.add_font("Arial", 10, "default")
            self.add_color("white", ColorHelper("white"))
            self.add_color("black", ColorHelper("black"))
        else:
            self.bg[self.page] = bg
            self.titles[self.page] = title
        self.reset(keepElem=True)
        self.go_to_page(0)
        self.opened = True

    def __del__(self):
        self.quit()

    def quit(self):
        pg.display.quit()
        pg.quit()
        self.opened = False


    def close(self):
        pg.display.quit()
        self.opened = False

    def is_opened(self):
        return self.opened


    """ Ajoute une police
        param: nom string police de caratère default : Arial
        param: size int taille de la police default : 10
        param: label string label de la police default: None
        param: opt dict options disponibles : bold (def: False), italic (def: False), underline (def: False),
         antialiasing (def: True)"""

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
        if label not in self.fonts.keys():
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
        if nom not in self.colors.keys():
            if isinstance(color, tuple):
                self.colors[nom] = color
            elif isinstance(color, str):
                self.colors[nom] = ColorHelper(color).get_rgb()
            else:
                self.colors[nom] = color.get_rgb()

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
        py_text = self.fonts[font][0].render(py_encode_font_txt(text), self.fonts[font][1], self.colors[color])
        if options["widthcentered"]:
            x = (width - py_text.get_rect().width) / 2
        if options["heightcentered"]:
            y = (height - py_text.get_rect().height) / 2
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
        self.elements[page][label] = (py_text, None, None, None, x, y)
        if page == self.page:  # Si l'on est sur la page du texte, on l'affiche directement
            self.window.blit(py_text, (x, y))
            if self.autoFlip:
                pg.display.flip()

        return py_text.get_rect()

    def edit_text(self, label, page=None, text=None, color=None, x=None, y=None):
        if page is None:
            page = self.page
        if text is not None and isinstance(text, str):
            self.elements[page][label][0] = text
        if isinstance(color, ColorHelper):
            self.elements[page][label]


    """ Ajoute une l'image url à x, y (point ancrage haut gauche), colorkey de type colorHelper"""

    def add_img(self, url, x, y, page=None, convert=True, alpha=False, colorkey=False, label=None, printElem=True):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        if isinstance(colorkey, ColorHelper):
            pg.image.set_colorkey(colorkey.get_rgb())
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
            color = color.get_rgb()
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
            color = color.get_rgb()
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
            color = color.get_rgb()
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
        self.elements[page][label] = ("line", color, o_x, o_y, e_x, e_y, border_width, aa)
        if page == self.page:
            self.print_element(label, page, autoFlip=self.autoFlip)

    """
        [["Menu 1", function, param1, param2], ["Menu 2", "addText", param1, param2, ...]]
        params: before_fun & after_fun : fonction(pygame, win, vars, menu) doit retourner vars (modifiée ou non)
    """

    def add_menu(self, x=0, y=0, menu=None, before_fun=None, after_fun=None, vars=None, opt=None):
        if menu is None:
            menu = []
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
        a_width, a_height, a_resizable, a_autoFlip = self.properties
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
        elif isinstance(color, ColorHelper):
            color = color.get_rgb()
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



window = WindowHelper.Instance()