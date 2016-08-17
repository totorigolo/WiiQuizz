# coding: utf8

from ColorHelper import ColorHelper
from WindowHelper import WindowHelper
import os
import time

win = WindowHelper.Instance()

win.open_window()  # ouvre la fenêtre

# Ajout des pages
win.new_page('Page d\'accueil', label='index', bg='white')
win.new_page('Page 1', label='page_1', bg='sage')
win.new_page('Page 2', label='page_2', bg='white')  # On altèrne les couleurs :D
win.new_page('Page 3', label='page_3', bg='sage')
win.new_page('Page 4', label='page_menu', bg='white')

# Ajout des ressources
win.new_color('blue')  # ColorHelper est directement implémenté
win.new_color('green')
win.new_font('Arial', 30, 'default')

win.new_text('Hello World!', 'default', 'blue', 'test_text')
win.new_text('Hello World!', 'default', 'green', 'test_text_2')
win.new_img(os.path.abspath('../res/sync_buzzer.jpg'), 'test_img')
win.new_rect('blue', 1, 'test_rect')
win.new_circle('blue', 50, 1, 'test_circle')

choices = ['Option 1', 'Option 2', ['Quitter', 'close']]
win.new_menu(choices, 'menu_1')  # On ajoute un menu de façon générale !

# Encrage des ressources aux pages
win.add('test_text_2', page='index')
win.add('test_text', page='page_1')
win.add('test_circle', 60, 60, page='page_1')
win.add('test_img', page='page_2')
win.add('test_rect', [10, 50], [10, 50], page='page_3')  # win.add(label, [x1, x2], [y1, y2], page)
win.add('test_circle', 150, 150, page='page_3')


# Pour les menus, utiliser add_menu
opt = {
    "font": "default",
    "color": "blue",
    "border": None,
    "color_active": "blue",
    "border_active": "sage",
    "font_active": "default",
    "margin": 20
}
win.add_menu('menu_1', page='page_menu', opt=opt)  # possiblilité de donner des fonctions et variables en paramètre !
# Astuce : ajouter le menu à la fin pour afficher les autres éléments lors de l'affichage

win.go_to('index')  # Affichage d'une page

time.sleep(2)

win.go_to('page_1')

time.sleep(2)

win.go_to('page_2')

time.sleep(2)

win.go_to('page_3')

time.sleep(2)

win.go_to('page_menu')
# pour récupérer le choix du menu, appeler win.get_menu_result(label). Ici :
print win.get_menu_result('menu_1')
