# coding: utf8

from ColorHelper import ColorHelper
from WindowHelper import WindowHelper
import os
import time


window = WindowHelper(800, 800, title="Accueil", bg = ColorHelper("white"))

window.add_font("Arial", 20, "menu")
window.add_font("Arial", 30, "titre")
window.add_color("menu_defaut", ColorHelper("burlywood"))
window.add_color("menu_act", ColorHelper("snow"))
window.add_color("menu_bordure_act", ColorHelper("indianred"))
# def addMenu(self, x=0, y=0, menu = [], opt = {})

window.new_page("page 1", goTo= False)
window.add_text("Page 1", "titre", "menu_defaut", label ="page1", page = 1, opt={"widthcentered": True, "heightcentered": True})
window.new_page("page 2", goTo = False)
window.add_text("Page 2", "titre", "menu_defaut", label ="page2", page = 2, opt={"widthcentered": True, "heightcentered": True})

""" addMenu prend une liste de choix en paramètre, chaque choix est une liste ["text à afficher", callback, param1, param2, ...] 
si callckack est une chaine, elle appelle une fonction propre à la classe windowsHelper, sinon elle execute la fonction """
choix = [["Aller page 1", "goTo", 1], ["Aller page 2", "goTo", 2], ["Fermer la fenêtre", "quit"]]
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
window.add_menu(y = 10, menu = choix, opt = options)