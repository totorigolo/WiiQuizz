# coding: utf8

from colorHelper import colorHelper
from windowsHelper import windowsHelper
import os
import time

window = windowsHelper(600, 600, title="Première fenêtre", bg=colorHelper("white"))
window.addColor("rect", colorHelper("salmon"))

# def addRect(self, color, x1, y1, x2, y2, border_width, page = None, label = None)
window.addRect("rect", 10, 10, 50, 50, 2, label="rectangle")

window.addCircle("rect", 100, 100, 20, 2, label="circle")