# coding: utf8

from ColorHelper import ColorHelper
from WindowHelper import WindowHelper
import os
import time

## Initialiser une couleur - colorHelper -

# Par rgb
couleurNoir = ColorHelper((0, 0, 0))
# Par nom
couleurNoirBis = ColorHelper("black")
# Récupérer le code rgb
print couleurNoirBis.get_rgb()

# Initialiser une couleur avec une transparence de 50%
couleurNoirPrime = ColorHelper("black", 0.5)
# Récupérer la transparence
print couleurNoirPrime.get_transparency()

# savoir si une couleur utilise la transparence
print couleurNoirPrime.is_transparent()

## Manipuler des fenêtres - windowHelper -

# Initialiser une fenêtre
width = 500
height = 500
""" title : titre de la page
    autoFlip : si True, à chaque ajout d'élément il s'ajoutera automatiquement, si False, appeler window.flip() 
"""
# def __init__(self, width, height, title = None, resizable = True, autoFlip = True)

window = WindowHelper.Instance()
window.open(width, height, title="Première fenêtre")

# Ajouter une image

# def addImg(self, url, x, y, page = None, convert = True, alpha = False, colorkey = False, label = None)
window.add_img(os.path.abspath('../res/sync_buzzer.jpg'), 10, 10, label="wiimote_info")
""" Par défaut, la page est la page courante """
""" pour le colorKey, utiliser un objet de type colorHelper """

time.sleep(2)

# Ajouter une page

# def newPage(self, title = None, goTo = True)
window.new_page("Page 1")
""" Si goTo vaut True, après l'appel de newPage, la fenêtre ira automatiquement vers cette page """

# Ajouter une police de caractère

# def addFont(self, nom = "Arial", size = 10, label = None)
window.add_font("Arial", 35, "titre")
window.add_font("Arial", 30, "txt")
""" Si le label n'est pas renseigné il sera automatiquement nom + str(size) """

# Ajouter une couleur

# def addColor(self, nom, color)
couleur = ColorHelper("white")
window.add_color("blanc", couleur)
""" Accepte les objets de type couleurHelper ou un tuple (r, g, b) """

# Ajouter un texte

# def addText(self, text, font, color, x = 0, y = 0, page = None, label = None, opt = {})
window.add_text("Hello World", "txt", "blanc", 20, 20, label="hw")
""" Les labels sont propres à chaque page, deux pages différentes peuvent avoir un élément de même label """
""" color est le label de la couleur demandé, de même pour la police """

# Ajouter un texte centré horizontalement
window.add_text("Hello World", "txt", "blanc", label="hw2", opt={"widthcentered": True}, y=50)

# Ajouter un texte centré verticalement
window.add_text("Hello World", "txt", "blanc", label="hw3", opt={"heightcentered": True}, x=20)

time.sleep(2)

# Changer de page
window.go_to_page(0)

""" Les pages sont numérotées à partir de 0 (page d'initialisation) """

# Accéder à l'information d'un élément

# def getElement(self, i, page = None)
""" i est soit un label et si l'élément n'avait pas de label, il est numéroté (à partir de 0) info : seuls les éléments
sans label sont numérotés """
print window.get_element("hw", page=1)
print window.elements[0]
print window.get_element("wiimote_info", page=0)

""" dans le cas d'une image ou forme, on peut récupérer directement l'objet Rect : """
print window.get_element_rect("wiimote_info", 0)

# Bouger un élément

# def moveElement(self, i, x, y, page = None)

time.sleep(1)

window.move_element("wiimote_info", 100, 100, page=0)

# Change titre
window.change_title("Titre fenêtre changée", page=0)
window.change_properties(width=1000)

time.sleep(2)
