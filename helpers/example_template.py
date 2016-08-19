# coding: utf8

from ColorHelper import ColorHelper
from WindowHelper import WindowHelper
import os
import time

win = WindowHelper.Instance()

win.new_page('Test fichier template', 800, 500, 'page_1', bg='white')
win.go_to('page_1')

win.new_font('Arial', 30, 'font')
win.new_color('blue')

win.import_template(os.path.abspath('../templates/test.skt'))


time.sleep(2)