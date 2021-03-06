# coding: utf8

from Dialog import Dialog
from WindowHelper import WindowHelper

win = WindowHelper.Instance()
dialog = Dialog.Instance()

dialog.new_message('success', "Hé salut toi ! :)")

win.new_page('Test fichier template', 960, 600, 'page_1', bg='white')
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

# Valeurs des points (templates num_players)
win.new_text('150', 'title', 'team2', label='team1_result')
win.new_text('150', 'title', 'team1', label='team2_result')
win.new_text('150', 'title', 'team4', label='team3_result')
win.new_text('150', 'title', 'team3', label='team4_result')

# Texte d'équipe (templates buzz_teams)
win.new_text('Pastèque', 'very_big', 'team2', label='text_buzz_team1')
win.new_text('Ananas', 'very_big', 'team1', label='text_buzz_team2')
win.new_text('Kiwi', 'very_big', 'team4', label='text_buzz_team3')
win.new_text('Melon', 'very_big', 'team3', label='text_buzz_team4')

# Texte réponse (template options_game)
win.new_text('Réponse haut', 'font', 'dark_blue', label='option_up_text')
win.new_text('Réponse gauche', 'font', 'dark_blue', label='option_left_text')
win.new_text('Réponse bas', 'font', 'dark_blue', label='option_down_text')
win.new_text('Réponse droite', 'font', 'dark_blue', label='option_right_text')

win.import_template('buzz_team1')


# win.edit_color('option_left', 'team1')

win.refresh()


def event_fun(pg, win, vars, event):
    if event.type == pg.KEYDOWN:
        return True
    return False

win.event(event_fun=event_fun)