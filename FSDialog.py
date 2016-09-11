# coding=utf-8

"""
FileSystem Dialog : Fichiers ou dossiers
"""

import os

from ListDialog import ListDialog


def get_file_list(path):
    try:
        file_list = []
        for image in os.listdir(path):
            if os.path.isfile(os.path.join(path, image)):
                file_list.append(image)
        return file_list
    except OSError:
        print u"Répertoire introuvable ({}) !".format(path)
        return []


def get_folder_list(path):
    try:
        folders = []
        for folder in os.listdir(os.path.abspath(path)):
            if not os.path.isfile(os.path.join(os.path.abspath(path), folder)):
                folders.append(folder)
        return path, folders
    except OSError:
        print u"Aucun répertoire trouvé !"
        return []


def get_file(directory, question="Sélectionnez un fichier :", cancel=None):
    list_dialog = ListDialog()
    folder, folder_list = get_file_list(directory)
    choix = list_dialog.get_answer(folder_list + ['Annuler'], question)
    if choix >= len(folder_list):
        return cancel
    return folder_list[choix]


def get_folder(directory, question="Sélectionnez un dossier :", cancel=None):
    list_dialog = ListDialog()
    folder, folder_list = get_folder_list(directory)
    choix = list_dialog.get_answer(folder_list + ['Annuler'], question)
    if choix >= len(folder_list):
        return cancel
    return folder_list[choix]
