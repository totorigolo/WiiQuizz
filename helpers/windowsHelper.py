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
        self.elements = [{}]
        self.elementsCounter = 0
        self.titles = [title]
        self.fonts = {}
        self.colors = {}
        self.vars = {}
        self.actions = [[]]


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
    	params: x, y
    	param: font label de la police choisie (doit être ajouté avec la méthode addFont)
    	param: color label de la couleur choisie (doit être ajouté avec la méthode addColor)
    	param: page int numéro de page à afficher default: page active
    	param: label string label du texte default: le numéro de l'élément """
    def addText(self, text, x, y, font, color, page = None, label = None):
        if page is None:
            page = self.page
        text = self.fonts[font].render(py_encode_font_txt(self.question_txt), True, self.colors[color])
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
       	self.elements[page][label] = (text, None, None, None)
        if page == self.page: # Si l'on est sur la page du texte, on l'affiche directement
            self.window.blit(text, (x, y))
            if self.autoFlip:
                pg.display.flip()


	""" Ajoute une l'image url à x, y (point ancrage haut gauche), colorkey de type colorHelper"""
    def addImg(self, url, x, y, page = None, convert = True, alpha = False, colorkey = False, label = None):
        if page is None:
            page = self.page
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
        if self.page = page:
            self.window.blit(bg, (x, y))
        if self.autoFlip:
            pg.display.flip()
        if label is None:
            label = self.elementsCounter
            self.elementsCounter += 1
        else:
            self.elements[page][label] = (bg, convert, alpha, colorkey)


    def delElement(self, i, page = None):
        if page is None:
            page = self.page
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
    	if self.page == page:
        	self.window.fill(color)
        else:
        	self.actions[page].append("self.fill(" + str(color) + ", " + str(page) + ")")


    def printElem(self, i, page = None, autoFlip = False):
    	if page is None:
    		page = self.page
        bg, convert, alpha, colorkey = self.elements[page][i]
        self.window.blit(bg, (x, y))
        if autoFlip:
            pg.display.flip()


    """ Ajoute une nouvelle page
    	param: title string titre de la page
    	param: goTo boolean si True, la fenêtre ira vers cette page après appel default: True"""
    def newPage(self, title = None, goTo = True):
	    self.LastPage += 1 
	    self.elements.append({})
	    self.titles.append(title)
	    self.actions.append([])
	    if goTo:
	        self.reset()
	        self.page = self.lastPage


    """ Ouvre la page k """
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
	    for cle, val in self.elements[k].items():
	    	self.printElem(cle, k)
	    for action in self.actions[k].values():
	    	eval(action)
	    self.actions[k] = []
	    self.flip()

    """ Renvoie l'élément demandé """
    def getElement(self, i, page = None):
        if page is None:
            page = self.page
        return self.elements[page][i][0]
        
    
    """ Renvoie l'instance Rect de l'élément demandé """
    def getInfoElement(self, i, page = None):
        if page is None:
            page = self.page
        return self.elements[page][i][0].get_rect()

	def moveElement(self, i, x, y, page = None):
        if page is None:
            page = self.page
        rec = self.getInfoElement(i).move(x, y)
        self.window.blit(self.getElement(i), rec)
        self.reset(keepElem = True)
        for k in range(len(self.elements[page])):
            self.printElem(k, page)
        if self.autoFlip:
            pg.display.flip()


    """ Liste les éléments à l'écran de l'indice i à j ; liste tous les éléments si non renseignés """
    def listElements(self, page = None):
        if page is None:
            page = self.page
        return self.elements[page]


    """ Renvoie une fenêtre vide """
    def reset(self, keepElem = False, page = None):
        self.fill(colorHelper("black"), page)
        if page is None:
        	page = self.page
        if not keepElem:
            self.elements[page] = []


    """ Met à jour la fenêtre """
    def flip(self):
        pg.display.flip()
        
        