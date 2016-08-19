# coding: utf8

from ColorHelper import ColorHelper
from WindowHelper import WindowHelper
import os
import time

win = WindowHelper.Instance()

win.new_page

win.new_font('Arial', 30, 'font')
win.new_color('blue', 'blue_color')

win.import_template(os.path.abspath('../templates/test.skt'))

win.go_to('page_1')

time.sleep(2)