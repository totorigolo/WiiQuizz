import pygame as pg
from pygame.locals import *
from colorHelper import colorHelper
from tools import py_encode_font_txt, py_encode_title

class windowHelper:
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
        self.elements = [[]]
        self.elementsLabeled = [dict()]
        self.titles = [title]
        self.fonts = {}
        self.colors = {}
        
        self.goTo(0)
      
        
        
    def addFont(self, nom = "Arial", size = 10, label = None):
        if label is None:
            label = nom + str(size)
        self.fonts[label] = pg.font.SysFont(nom, size)
        
        
    def addColor(self, nom, color):
        if isinstance(color, tuple):
            self.colors[nom] = color
        else:
            self.colors[nom] = color.getTuple()
       
        
        
    def addText(self, text, x, y, font, color, page = None, label = None):
        if page is None:
            page = self.page
        text = self.fonts[font].render(py_encode_font_txt(self.question_txt), True, self.colors[color])
        if label is not None:
            self.elementsLabeled[page][label] = (text, None, None, None)
        else:
            self.elements[page].append((text, None, None, None))
        if page == self.page:
            self.window.blit(text, (x, y))
            if self.autoFlip:
                pg.display.flip()
        
        
    
    """ Remplie la fenêtre d'une couleur voulue """
    def fill(self, color):
        self.window.fill(color.getTuple())
        
        
    """ Renvoie une fenêtre vide """
    def reset(self, keepElem = False):
        self.fill(colorHelper("black"))
        if not keepElem:
            self.elements[self.page] = []
            self.elementsLabeled[self.page] = {}
            
    
    """ Ajoute une l'image url à x, y (point ancrage haut gauche), colorkey de type colorHelper"""
    def setImg(self, url, x, y, page = None, convert = True, alpha = False, colorkey = False, label = None):
        if page is None:
            page = self.page
        if colorkey != False:
            pg.image.set_colorkey(colorkey.getTuple())
        if alpha:
            bg = pg.image.load(url).convert_alpha()
        elif convert:
            bg = pg.image.load(url).convert()
        else:
            bg = pg.image.load(url)
        if self.page = page:
            self.window.blit(bg, (x, y))
        if self.autoFlip:
            pg.display.flip()
        if label is not None:
            self.elementsLabeled[self.page][label] = (bg, convert, alpha, colorkey)
        else:
            self.elements[self.page].append((bg, convert, alpha, colorkey))
            
            
    
    def newPage(self, title = None, goTo = True):
        self.LastPage += 1 
        self.elements.append([])
        self.elementsLabeled.append(dict())
        self.titles.append(title)
        if goTo:
            self.reset()
            self.page = self.lastPage
            
            
    def goTo(self, k):
        self.page = k
        self.reset()
        title = self.titles[k]
        if title is not None:
            if not isinstance(title, str) or not isinstance(title, unicode):
                title = str(title)
            if isinstance(title, unicode):
                pg.display.set_caption(py_encode_title(title.encode('utf-8')))
            else:
                pg.display.set_caption(py_encode_title(title))
        
        
        
     
    def printElem(self, i, autoFlip = False):
        if isinstance(i, int):
            bg, convert, alpha, colorkey = self.elements[self.page][i]
        else:
            bg, convert, alpha, colorkey = self.elementsLabeled[self.page][i]
        self.window.blit(bg, (x, y))
        if autoFlip:
            pg.display.flip()
            
        
    
    """ Liste les éléments à l'écran de l'indice i à j ; liste tous les éléments si non renseignés """
    def listElements(self, i=None, j=None, page = None):
        if page is None:
            page = self.page
        return self.elements[page][i:j][0]
        
    
    """ Renvoie l'élément demandé """
    def getElement(self, i, page = None):
        if page is None:
            page = self.page
        if isinstance(i, str):
            return self.elementsLabeled[page][i][0]
        return self.elements[page][i][0]
        
    
    """ Renvoie l'instance Rect de l'élément demandé """
    def getInfoElement(self, i, page = None):
        if page is None:
            page = self.page
        if isinstance(i, str):
            return self.elementsLabeled[page][i][0].get_rect()
        return self.elements[page][i][0].get_rect()
        
    
        
    def moveElement(self, i, x, y, page = None):
        if page is None:
            page = self.page
        rec = self.getInfoElement(i).move(x, y)
        self.window.blit(self.getElement(i), rec)
        self.reset(keepElem = True)
        for k in range(len(self.elements[page])):
            self.printElem(k)
        for k in range(len(self.elementsLabeled[page])):
            self.printElem(k)
        if self.autoFlip:
            pg.display.flip()
            
            
        
    def delElement(self, i, page = None):
        if page is None:
            page = self.page
        self.reset(keepElem = True)
        for k in range(len(self.elements[page])):
            if isinstance(i, str) or i != k:
                self.printElem(k)
        for k in range(len(self.elementsLabeled[page])):
            if isinstance(i, int) or i != k:
                self.printElem(k)
        if self.autoFlip:
            pg.display.flip()
        
        
    """ Met à jour la fenêtre """
    def flip(self):
        pg.display.flip()
        
        