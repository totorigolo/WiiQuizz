# coding: utf8

import pygame as pg
from pygame.locals import *
from colorHelper import colorHelper
from tools import py_encode_font_txt, py_encode_title
from inspect import isfunction
import time


class windowsHelper:
    """ Lance une fenêtre de taille width x height """
    def __init__(self, width, height, title=None, resizable=True, autoFlip=True, bg=colorHelper("black")):
        pg.init()
        if resizable:
            self.window = pg.display.set_mode((width, height), RESIZABLE)
        else:
            self.window = pg.display.set_mode((width, height))

        if not isinstance(bg, tuple):
            bg = bg.getTuple()

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

        self.reset(keepElem=True)

        self.addFont("Arial", 10, "default")
        self.addColor("white", colorHelper("white"))
        self.addColor("black", colorHelper("black"))
        self.goTo(0)


    def __del__(self):
        self.quit()


    def quit(self, temps=1):
        time.sleep(temps)
        pg.display.quit()
        pg.quit()


    """ Ajoute une police 
        param: nom string police de caratère default : Arial
        param: size int taille de la police default : 10
        param: label string label de la police default: None """

    def addFont(self, nom="Arial", size=10, label=None, opt={}):
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

    def addColor(self, nom, color):
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

    def addText(self, text, font, color, x=0, y=0, page=None, label=None, opt={}):
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


    """ Ajoute une l'image url à x, y (point ancrage haut gauche), colorkey de type colorHelper"""

    def addImg(self, url, x, y, page=None, convert=True, alpha=False, colorkey=False, label=None):
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
        if self.page == page:
            self.window.blit(bg, (x, y))
        if self.autoFlip:
            pg.display.flip()
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
        self.elements[page][label] = (bg, convert, alpha, colorkey, x, y)


    def addRect(self, color, x1, y1, x2, y2, border_width, page=None, label=None):
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
            self.printElem(label, page, autoFlip=self.autoFlip)


    def addCircle(self, color, c_x, c_y, radius, border_width, page=None, label=None):
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
            self.printElem(label, page, autoFlip=self.autoFlip)


    """
    param: aa bool anti-aliasing
    """

    def addLine(self, color, o_x, o_y, e_x, e_y, border_width, aa=True, page=None, label=None):
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
            self.printElem(label, page, autoFlip=self.autoFlip)


    """
        [["Menu 1", function, param1, param2], ["Menu 2", "addText", param1, param2, ...]]
    """

    def addMenu(self, x=0, y=0, menu=[], opt={}):
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
                    if pressed and choix == k and isfunction(callback):
                        params = "("
                        for i in range(2, len(m)):
                            params += str(m[i])
                            if i != len(m) - 1:
                                params += ", "
                        params += ")"
                        callback(eval(params))
                else:
                    text = m

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
                self.window.blit(txt, (x, y))
                y += txt.get_rect().height + options["margin"]

                k += 1

            pg.display.flip()
        return choix


    def delElement(self, i, page=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        self.reset(keepElem=True)
        del self.elements[page][i]
        for k in range(len(self.elements[page])):
            self.printElem(k, page)
        if self.autoFlip:
            pg.display.flip()


    """ Remplie la fenêtre d'une couleur voulue """

    def fill(self, color, page=None):
        if not isinstance(color, tuple):
            color = color.getTuple()
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        if self.page == page:
            self.window.fill(color)
        else:
            self.actions[page].append("self.fill(" + str(color) + ", " + str(page) + ")")


    def printElem(self, i, page=None, autoFlip=False):
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
            if aa: # anti-aliasing
                pg.draw.aaline(self.window, color, [o_x, o_y], [e_x, e_y], border_width)
            else:
                pg.draw.line(self.window, color, [o_x, o_y], [e_x, e_y], border_width)
        else:
            bg, convert, alpha, colorkey, x, y = self.elements[page][i]
            self.window.blit(bg, (x, y))
        if autoFlip:
            pg.display.flip()


    """ Ajoute une nouvelle page
        param: title string titre de la page
        param: goTo boolean si True, la fenêtre ira vers cette page après appel default: True"""

    def newPage(self, title=None, bg=None, goTo=True):
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


    """ Ouvre la page k """

    def goTo(self, k):
        self.page = k
        self.reset(keepElem=True)
        title = self.titles[k]
        if title is not None:
            py_encode_title(title)

        for cle, val in self.elements[k].items():
            self.printElem(cle, k)
        for action in self.actions[k]:
            eval(action)
        self.actions[k] = []
        self.flip()

    """ Renvoie l'élément demandé """

    def getElement(self, i, page=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        return self.elements[page][i][0]


    """ Renvoie l'instance Rect de l'élément demandé """

    def getInfoElement(self, i, page=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        return self.elements[page][i][0].get_rect()


    def moveElement(self, i, x, y, page=None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        rec = self.getInfoElement(i, page).move(x, y)
        self.window.blit(self.getElement(i, page), rec)
        bg, convert, alpha, colorkey, ax, ay = self.elements[page][i]
        self.elements[page][i] = bg, convert, alpha, colorkey, x, y
        self.reset(True, page)
        for cle, val in self.elements[page].items():
            self.printElem(cle, page)
        if self.autoFlip:
            pg.display.flip()


    """ Liste les éléments à l'écran de l'indice i à j ; liste tous les éléments si non renseignés """

    def listElements(self, page=None):
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
                self.printElem(cle, page)
        if not keepElem:
            self.elements[page] = {}


    """ Met à jour la fenêtre """

    def flip(self):
        pg.display.flip()
        
        