# coding: utf8

from ColorHelper import ColorHelper
from WindowHelper import WindowHelper
import os
import time

win = WindowHelper.Instance()

win.new_page('Test fichier template', 1200, 500, 'page_1', bg='white')
win.go_to('page_1')

# Font importantes
win.new_font('Arial', 40, 'title')
win.new_font('Arial', 30, 'font')
win.new_font('Arial', 20, 'sub_title')
win.new_font('Arial', 70, 'very_big')

# Couleurs utilisées
win.new_color((5, 51, 90), 'dark_blue')
win.new_color((176, 194, 238), 'blue_options')
win.new_color((210, 4, 5), 'red_error')
win.new_color((60, 154, 80), 'green_victory')
win.new_color((255, 0, 96), 'team1')
win.new_color((252, 255, 0), 'team2')
win.new_color((58, 119, 71), 'team3')
win.new_color((255, 162, 0), 'team4')
win.new_color('white')
win.new_color('black')

# Valeurs des points
win.new_text('150', 'title', 'team2', label='team1_result')
win.new_text('150', 'title', 'team1', label='team2_result')
win.new_text('150', 'title', 'team4', label='team3_result')
win.new_text('150', 'title', 'team3', label='team4_result')

# Texte d'équipe
win.new_text('Pastèque', 'very_big', 'team2', label='text_buzz_team1')
win.new_text('Ananas', 'very_big', 'team1', label='text_buzz_team2')
win.new_text('Kiwi', 'very_big', 'team4', label='text_buzz_team3')
win.new_text('Melon', 'very_big', 'team3', label='text_buzz_team4')

win.import_template('options_game')

win.edit_color('option_2', 'team1')

win.refresh()

time.sleep(2)