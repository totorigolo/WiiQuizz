# coding: utf8

from colorHelper import colorHelper
from windowsHelper import windowsHelper
import os
import time

window = windowsHelper(600, 600, title="Première fenêtre", bg=colorHelper("white"))
window.add_color("rect", colorHelper("salmon"))

# def addRect(self, color, x1, y1, x2, y2, border_width, page = None, label = None)
window.add_rect("rect", 10, 10, 50, 50, 2, label="rectangle")

window.add_circle("rect", 100, 100, 20, 2, label="circle")