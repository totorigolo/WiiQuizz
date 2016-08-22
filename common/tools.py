# coding=utf-8

import sys
import os
from random import randint
import re

def py_encode_font_txt(txt):
    if not isinstance(txt, str) or not isinstance(txt, unicode):
        txt = str(txt)
    if isinstance(txt, unicode):
        return txt
    else:
        return unicode(txt, 'utf-8')


def py_encode_title(txt):
    if not isinstance(txt, str) or not isinstance(txt, unicode):
        txt = str(txt)
    if isinstance(txt, unicode):
        return txt.encode('utf-8')
    else:
        return txt


def print_noln(str):
    sys.stdout.write(str)


def prompt_int(min=None, max=None):
    def condition_bad_prompt(choix, min, max):
        try:
            if min is not None and max is not None:
                return not isinstance(choix, int) or not min <= choix <= max
            elif min is not None:
                return not isinstance(choix, int) or not min <= choix
            elif max is not None:
                return not isinstance(choix, int) or not choix <= max
            else:
                return not isinstance(choix, int)
        except:
            return False

    choix = None
    while condition_bad_prompt(choix, min, max):
        try:
            choix = int(raw_input())
        except ValueError:
            pass
    return choix


def permutation(nb):
    print "Should consider using itertools..."
    l = [k for k in range(nb)]
    for k in range(nb):
        i, j = randint(0, nb - 1), randint(0, nb - 1)
        l[i], l[j] = l[j], l[i]
    return l


def clef(dict, val):
    """ Donne la clé d'un dictionnaire pour une valeur donnée """
    for (k, v) in dict.items():
        if v == val:
            return k
    return False


def list_files(files):
    listed_files = os.listdir(files)
    def comp(x, y):
        try:
            x = re.findall("([\d\.]*)\.\w{2,4}", x)
            y = re.findall("([\d\.]*)\.\w{2,4}", y)
            x, y = float(x[0]), float(y[0])
        except:
            raise ValueError("Les fichiers n'ont pas le bon format (float.ext)")
        return cmp(x, y)
    return sorted(listed_files, cmp=comp)

def format_text(text):
    return text.lower().replace(' ', '_').replace('é', 'e').replace('à', 'a').replace('è', 'e')