from colorHelper import colorHelper
from windowsHelper import windowsHelper
import os
import time

## Initialiser une couleur - colorHelper -

# Par rgb
couleurNoir = colorHelper((0, 0, 0))
# Par nom
couleurNoirBis = colorHelper("black")
# Récupérer le code rgb
print couleurNoirBis.getTuple()

# Initialiser une couleur avec une transparence de 50%
couleurNoirPrime = colorHelper("black", 0.5)
# Récupérer la transparence
print couleurNoirPrime.getTransparence()

# savoir si une couleur utilise la transparence
print couleurNoirPrime.isTransparent()


## Manipuler des fenêtres - windowHelper - 

# Initialiser une fenêtre
width = 500
height = 500
""" title : titre de la page
    autoFlip : si True, à chaque ajout d'élément il s'ajoutera automatiquement, si False, appeler window.flip() 
"""
# def __init__(self, width, height, title = None, resizable = True, autoFlip = True)

window = windowHelper(width, height, title="Première fenêtre")

# Ajouter une image

# def setImg(self, url, x, y, page = None, convert = True, alpha = False, colorkey = False, label = None)
window.addImg(os.path.abspath('../res/sync_buzzer.jpg'), 10, 10, label = "wiimote_info")
""" Par défaut, la page est la page courante """
""" pour le colorKey, utiliser un objet de type colorHelper """

time.sleep(2)

# Ajouter une page

# def newPage(self, title = None, goTo = True)
window.newPage("Page 1")
""" Si goTo vaut True, après l'appel de newPage, la fenêtre ira automatiquement vers cette page """

# Ajouter une police de caractère

# def addFont(self, nom = "Arial", size = 10, label = None)
window.addFont("Arial", 35, "titre")
window.addFont("Arial", 30, "txt")
""" Si le label n'est pas renseigné il sera automatiquement nom + str(size) """

# Ajouter une couleur

# def addColor(self, nom, color)
window.addColor("noir", couleurNoirBis)
""" Accepte les objets de type couleurHelper ou un tuple (r, g, b) """

# Changer de page
window.goTo(0) 

""" Les pages sont numérotées à partir de 0 (page d'initialisation) """

# Ajouter un texte

# def addText(self, text, x, y, font, color, page = None, label = None)
window.addText("Hello World", 20, 20, "titre", "noir", label = "titre")
""" Les labels sont propres à chaque page, deux pages différentes peuvent avoir un élément de même label """
""" color est le label de la couleur demandé, de même pour la police """

time.sleep(2)

# Accéder à l'information d'un élément

# def getElement(self, i, page = None)
""" i est soit un label et si l'élément n'avait pas de label, il est numéroté (à partir de 0) info : seuls les éléments
sans label sont numérotés """
print window.getElement("titre", page = 1)
print window.getElement("wiimote_info", page = 0)

""" dans le cas d'une image ou forme, on peut récupérer directement l'objet Rect : """
print window.getInfoElement("wiimote_info", 0)


# Bouger un élément

# def moveElement(self, i, x, y, page = None)

window.moveElement("titre", 50, 50)





