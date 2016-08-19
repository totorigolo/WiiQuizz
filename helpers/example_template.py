# coding: utf8

from ColorHelper import ColorHelper
from WindowHelper import WindowHelper
import os
import time

win = WindowHelper.Instance()

win.new_page('Test fichier template', 800, 600, 'page_1', bg='white')
win.go_to('page_1')

win.new_font('Arial', 40, 'title')
win.new_font('Arial', 30, 'font')
win.new_font('Arial', 20, 'sub_title')

win.new_color((5, 51, 90), 'dark_blue')
win.new_color((255, 0, 96), 'team1')
win.new_color((252, 255, 0), 'team2')
win.new_color((33, 199, 11), 'team3')
win.new_color((255, 162, 0), 'team4')
win.new_color('white')
win.new_color('black')
win.new_text('150', 'title', 'black', label='team4_result')

#
win.import_template('four_players')

win.refresh()


time.sleep(2)