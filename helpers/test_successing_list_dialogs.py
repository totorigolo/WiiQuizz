# coding: utf8

from ListDialog import ListDialog

dialog = ListDialog()

print dialog.get_answer(["1", "2"], "Choisissez :", "avec attention...")
print dialog.get_answer(["T'as pas le choix coco !"], "Perdu !")
