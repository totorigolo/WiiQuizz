# coding=utf-8

import random
from Queue import Queue

import pygame as pg

from Buzzer import Buzzer
from Singleton import Singleton
from WindowHelper import WindowHelper

WIIMOTE_EVENT = pg.USEREVENT  # Type d'évènement correspondant à un buzzer. Voir BuzzerMgr.post_events()


@Singleton
class BuzzerMgr:
    """
    Cette classe s'occupe de la gestion des Wiimotes. C'est elle qui gère :
     - la connexion / déconnexion
     - les évènements
    """

    def __init__(self, dummy=False):
        """
        Initialise le BuzzerMgr
        """
        ''' Déclaration et initialisation des attributs '''
        self.buzzers = dict()
        self.unused_buzzers = []  # liste de tuple : (ancienne fonction [1-4,'master], Buzzer)
        self.nb_wiimote = 0
        self.need_master = None
        self.dummy = dummy
        self.event_queue = Queue()

    def __reinit(self):
        """ Supprime les manettes et réinitialise les connexions. NE RECONNECTE PAS les wiimotes. """
        for __, b in self.buzzers.iteritems():
            b.close()
        self.buzzers = dict()

        for b in self.unused_buzzers:
            b[1].close()
        self.unused_buzzers = []

        self.nb_wiimote = 0

    def set_dummy(self, dummy):
        # TODO: Reconnecter les manettes selon
        self.dummy = dummy
        if dummy:
            print "Vous devriez redémarrer si vous désirer connecter des manettes précédemment dummy, car" \
                  "cette fonctionnalité n'est pas encore supportée."

    def connect_master(self):
        """
        Connecte uniquement la wiimote master
        """
        if 'master' not in self.buzzers:
            # Cherche si on a un vieux master en mémoire
            for role, buzzer in self.unused_buzzers:
                if role == 'master':
                    self.buzzers['master'] = buzzer
                    return

            # Connecte un nouveau master
            self.__connect_buzzer('master', 'Master')

    def require(self, nb_joueuses_requises, need_master=True):
        """
        Cette méthode sert à indiquer que nous avons besoin de nb_wiimote wiimotes, avec EN PLUS une wiimote master
        si need_master est True.
        :param nb_joueuses_requises: Le nombre de wiimotes JOUEUSES requises. Peut être 1 à 4 ou 'ask'
        :param need_master: Indique s'il faut EN PLUS une wiimote master
        """

        # Nombre de wiimotes
        # TODO: permettre de renseigner des bornes pour ask
        if nb_joueuses_requises == 'ask':
            nb_joueuses_requises = self._prompt_nb_wiimotes(need_master)

        # Si on est déjà initialisé, on regarde combien de wiimotes on a de trop pour les désactiver
        if nb_joueuses_requises - self.nb_wiimote < 0:
            # Désactive les wiimotes joueuses dont on a plus besoin
            for b in self.buzzers:
                if b not in range(1, nb_joueuses_requises):
                    self.__idle_buzzer(b)

            # Désactive le master
            if not need_master and 'master' in self.buzzers:
                self.__idle_buzzer('master')

            # Vérifie que l'on dispose des bonnes manettes
            erreur_d_attribution = False
            for i in range(1, nb_joueuses_requises + 1):
                if i not in self.buzzers or not self.buzzers[i].connected:
                    erreur_d_attribution = True
                    break

            # Pas d'erreur, on a fini
            if not erreur_d_attribution:
                    # On a les manettes, c'est bon
                    return

        # On connecte le master si besoin
        if need_master and 'master' not in self.buzzers:
            self.connect_master()
        elif not need_master and 'master' in self.buzzers:
            self.__idle_buzzer('master')

        # On connecte les wiimotes joueuses manquantes
        for i in range(1, nb_joueuses_requises + 1):
            if i not in self.buzzers or not self.buzzers[i].connected:
                self.__connect_buzzer(i, i)

    def __connect_buzzer(self, key, name):
        """
        Interface de connexion de manette
        :param key: avec quelle key sera stockée le buzzer dans self.buzzers
        :param name: le nom qui sera affiché à l'écran
        """

        # Si on a déjà un Buzzer du même nom, on le récupère
        buzzer_en_attente = None
        if key in self.buzzers:
            buzzer_en_attente = self.buzzers[key]
        else:
            buzzer_en_attente = Buzzer(key, dummy=self.dummy)

        # Démarre la connexion de façon asynchrone
        buzzer_en_attente.async_wait()

        # Ouvre une fenêtre
        win = WindowHelper.Instance()
        win.new_page('Page de connexion', label='connect_buzzer', bg='white')
        win.go_to('connect_buzzer')

        win.import_template('wiimote_connexion')

        win.edit_text('text_connexion_team', 'Télécommande {}'.format(name))  # à modifier

        win.refresh()

        # Variable d'execution
        vars = {
            'buzzer_en_attente': buzzer_en_attente,
            'self': self
        }

        # Attend que la manette soit connectée
        def waiting_connection(pg, win, vars, event):
            if event.type == pg.KEYDOWN and event.key == pg.K_d:
                vars['buzzer_en_attente'].dummy = True
            return vars['buzzer_en_attente'].connected

        win.event(event_fun=waiting_connection, vars=vars)  # On attend que quelqu'un appuie sur un bouton

        # Stocke le nouveau buzzer
        self.buzzers[key] = buzzer_en_attente

    def __idle_buzzer(self, key):
        """
        Met un buzzer en veille
        :param key: la clé du buzzer à mettre en veille. Doit être dans self.buzzers
        """
        if key in self.buzzers:
            self.buzzers[key].allumer_led([1, 0, 0, 1])
            self.unused_buzzers.append((key, self.buzzers[key]))
            self.buzzers.pop(key)
        else:
            raise KeyError('Le buzzer "{}" n\'est actuellement pas connecté !'.format(key))

    def button_down(self, which, btn):
        """
        Indique si le bouton btn est actuellement pressé sur la wiimote which
        :param which: wiimote dont on souhaite connaitre l'état. Peut être 1 à 4 ou master.
        :param btn: le bouton. Doit être dans la liste BOUTONS du fichier Buzzers.py
        :return: un boolean correspondant à l'état du bouton btn sur la wiimote which
        """
        if which not in self.buzzers.keys() or self.buzzers[which].dummy:
            return False
        return self.buzzers[which].is_down(btn)

    def buzzers_which(self, btn):
        """
        Renvoie la liste des buzzers qui ont le bouton btn pressé.
        :param btn: le bouton. Doit être dans la liste BOUTONS du fichier Buzzers.py
        :return: Un array contenant les wiimotes qui ont btn pressé. Il peut contenir 1 à 4 et / ou 'master'
        """
        list_which = []
        for __, b in self.buzzers.iteritems():
            if b.is_down(btn):
                list_which.append(b)
        return list_which

    def get_nb_buzzers(self, count_master=True):
        """
        :param: count_master: Compter la master ?
        :return: Retourne le nombre de manettes
        """
        return self.nb_wiimote - (0 if count_master and 'master' in self.buzzers else 1)

    def post_events(self):
        """
        Ajoute les évènements des buzzers à la file de PyGame.
        Les évènements ajoutés sont du type WIIMOTE_EVENT (pg.USEREVENT). Les attributs sont :
          - wiimote_id : 1 à 4 ou 'master'
          - btn : le bouton ayant généré l'évènement. Voir BOUTONS dans Buzzer.py
          - pressed : True si l'évènement correspond à une touche qui vient d'être pressée
        """
        for id, buzzer in self.buzzers.items():
            events = buzzer.get_events()
            for e in events:
                pg.event.post(pg.event.Event(WIIMOTE_EVENT, wiimote_id=id, btn=e[0], pressed=e[1]))

    def any_of(self, buzzers, master_first=True):
        """
        Fonction statique : renvoi une wiimote au hasard dans la liste buzzers. Sert quand plusieurs buzzers ont
        pressé une touche en même temps, et qu'il faut déterminer une gagnante équitablement.
        :param buzzers: la liste de wiimotes dont on veut un pseudo-plus-rapide
        :param master_first: la wiimote master est prioritaire si True
        :return: une wiimote. Peut être 1 à 4 ou 'master', ou None si buzzers est vide
        """
        if len(buzzers) == 0:
            return None
        if master_first:
            for b in buzzers:
                if b.team == 'master':
                    return b
        return random.choice(buzzers)

    def _prompt_nb_wiimotes(self, need_master):
        """
        Fonction privée statique : Demande le nombre de wiimotes joueuses requises.
        :param need_master: Pour afficher un message au joueurs comme quoi il faut une wiimote de plus
        :return: un int correspondant au nombre TOTAL (dont master) de wiimotes
        """
        from ListDialog import ListDialog
        dialog = ListDialog()

        question = u'Combien de Wiimotes joueuses ?'
        sous_texte = ''
        offset = 0
        if need_master:
            sous_texte = "une manette supplémentaire est requise pour le contrôle du jeu"
            offset = 1
        return dialog.get_answer([i for i in range(1, 5)], question, sous_texte) + offset
