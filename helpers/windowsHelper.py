# coding: utf8

import pygame as pg
from pygame.locals import *
from colorHelper import colorHelper
from tools import py_encode_font_txt, py_encode_title
from inspect import isfunction
import time

class windowsHelper:
    """ Lance une fenêtre de taille width x height """
    def __init__(self, width, height, title = None, resizable = True, autoFlip = True):
        pg.init()
        if resizable:
            self.window = pg.display.set_mode((width, height), RESIZABLE)
        else:
            self.window = pg.display.set_mode((width, height))
            
        
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
        
        self.addFont("Arial", 10, "default")
        self.addColor("white", colorHelper("white"))
        self.addColor("black", colorHelper("black"))
        self.goTo(0)
        
        
    def __del__(self):
        self.quit()
        
        
    def quit(self, temps = 1):
        time.sleep(temps)
        pg.display.quit()
        pg.quit()
    
    
    """ Ajoute une police 
        param: nom string police de caratère default : Arial
        param: size int taille de la police default : 10
        param: label string label de la police default: None """
    def addFont(self, nom = "Arial", size = 10, label = None):
        if label is None:
            label = nom + str(size)
        self.fonts[label] = pg.font.SysFont(nom, size)
    
    
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
    def addText(self, text, font, color, x=0, y=0, page = None, label = None, opt = {}):
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
        text = self.fonts[font].render(py_encode_font_txt(text), True, self.colors[color])
        if options["widthcentered"]:
            x = (width - text.get_rect().width) / 2
        if options["heightcentered"]:
            y = (height - text.get_rect().height) / 2
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
        self.elements[page][label] = (text, None, None, None, x, y)
        if page == self.page: # Si l'on est sur la page du texte, on l'affiche directement
            self.window.blit(text, (x, y))
            if self.autoFlip:
                pg.display.flip()
    
    
    """ Ajoute une l'image url à x, y (point ancrage haut gauche), colorkey de type colorHelper"""
    def addImg(self, url, x, y, page = None, convert = True, alpha = False, colorkey = False, label = None):
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
        
    """
        [["Menu 1", function, param1, param2], ["Menu 2", "addText", param1, param2, ...]]
    """
    def addMenu(self, x=0, y=0, menu = [], opt = {}):
        options = {
            "font": "default",
            "color": "white",
            "border": None,
            "colorActive": "white",
            "borderActive": None,
            "fontActive": "default",
            "widthcentered": False,
            "margin" : 20
        }
        options.update(opt)
        width_win, height_win = pg.display.get_surface().get_size()
        choix = 0
        cont = True
        pressed = False
        ax, ay = x, y
        while cont:
            x, y = ax, ay
            for event in pg.event.get():
                if event.type == QUIT:
                    cont = False
                if event.type == KEYDOWN:
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        cont = False
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
                            if i != len(m)-1:
                                callback += ", "
                        callback += ")"
                        eval(callback)
                    if pressed and choix == k and not isfunction(callback):
                        params = "("
                        for i in range(2, len(m)):
                            params += str(m[i])
                            if i != len(m)-1:
                                params += ", "
                        params += ")"
                        callback(eval(params))
                else:
                    text = m
                
                if choix == k:
                    if options["borderActive"] is not None:
                        txt = self.fonts[options["fontActive"]].render(py_encode_font_txt(text), True, self.colors[options["colorActive"]], self.colors[options["borderActive"]])
                    else:
                        txt = self.fonts[options["fontActive"]].render(py_encode_font_txt(text), True, self.colors[options["colorActive"]])
                else:
                    if options["border"] is not None:
                        txt = self.fonts[options["font"]].render(py_encode_font_txt(text), True, self.colors[options["color"]], self.colors[options["border"]])
                    else:
                        txt = self.fonts[options["font"]].render(py_encode_font_txt(text), True, self.colors[options["color"]])

                if options["widthcentered"]:
                    x = (width_win - txt.get_rect().width) / 2
                self.window.blit(txt, (x, y))
                y += txt.get_rect().height + options["margin"]
                    
                k += 1
                
            
            pg.display.flip()
            # Baisse les FPS
            time.sleep(1. / 25)
        return choix
                
    
    
    def delElement(self, i, page = None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        self.reset(keepElem = True)
        del self.elements[page][i]
        for k in range(len(self.elements[page])):
            self.printElem(k, page)
        if self.autoFlip:
            pg.display.flip()
    
    
    """ Remplie la fenêtre d'une couleur voulue """
    def fill(self, color, page = None):
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
    
    
    def printElem(self, i, page = None, autoFlip = False):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        bg, convert, alpha, colorkey, x, y = self.elements[page][i]
        self.window.blit(bg, (x, y))
        if autoFlip:
            pg.display.flip()
    
    
    """ Ajoute une nouvelle page
        param: title string titre de la page
        param: goTo boolean si True, la fenêtre ira vers cette page après appel default: True"""
    def newPage(self, title = None, goTo = True):
        self.lastPage += 1 
        self.elements.append({})
        self.titles.append(title)
        self.actions.append([])
        if goTo:
            self.reset(keepElem = True)
            self.page = self.lastPage


    """ Ouvre la page k """
    def goTo(self, k):
        self.page = k
        self.reset(keepElem = True)
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
    def getElement(self, i, page = None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        return self.elements[page][i][0]
        
    
    """ Renvoie l'instance Rect de l'élément demandé """
    def getInfoElement(self, i, page = None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        return self.elements[page][i][0].get_rect()
        

    def moveElement(self, i, x, y, page = None):
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
    def listElements(self, page = None):
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        return self.elements[page]


    """ Renvoie une fenêtre vide """
    def reset(self, keepElem = False, printElem = False, page = None):
        self.fill(colorHelper("black"), page)
        if page is None:
            page = self.page
        if page > self.lastPage:
            page = 0
        if printElem:
            for cle, val in self.elements[page].items():
                self.printElem(cle, page)
        if not keepElem:
            self.elements[page] = {}


    """ Met à jour la fenêtre """
    def flip(self):
        pg.display.flip()
        
        