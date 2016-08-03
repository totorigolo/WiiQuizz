# coding: utf8

from colorHelper import colorHelper
from windowsHelper import windowsHelper
import os
import time


window = windowsHelper(800, 800, title="Accueil", bg = colorHelper("white"))

window.addFont("Arial", 20, "menu")
window.addFont("Arial", 30, "titre")
window.addColor("menu_defaut", colorHelper("burlywood"))
window.addColor("menu_act", colorHelper("snow"))
window.addColor("menu_bordure_act", colorHelper("indianred"))
# def addMenu(self, x=0, y=0, menu = [], opt = {})

window.newPage("page 1", goTo= False)
window.addText("Page 1", "titre", "menu_defaut", label = "page1", page = 1, opt={"widthcentered": True, "heightcentered": True})
window.newPage("page 2", goTo = False)
window.addText("Page 2", "titre", "menu_defaut", label = "page2", page = 2, opt={"widthcentered": True, "heightcentered": True})

""" addMenu prend une liste de choix en paramètre, chaque choix est une liste ["text à afficher", callback, param1, param2, ...] 
si callckack est une chaine, elle appelle une fonction propre à la classe windowsHelper, sinon elle execute la fonction """
choix = [["Aller page 1", "goTo", 1], ["Aller page 2", "goTo", 2], ["Fermer la fenêtre", "quit", 0]]
options = {
    "font": "menu",
    "color": "menu_defaut",
    "border": None,
    "colorActive": "menu_act",
    "borderActive": "menu_bordure_act",
    "fontActive": "menu",
    "widthcentered": True,
    "margin" : 20
}

""" Les menus ne s'ajoutent que sur la page courante (pour le moment) """
window.addMenu(y = 10, menu = choix, opt = options)