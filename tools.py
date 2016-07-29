# coding=utf-8

from random import randint


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
