# coding: utf8

import threading
import time
from Queue import Queue

from Dialog import Dialog

try:
    import cwiid
    cwiid_found = True
except ImportError:
    cwiid_found = False

# TODO: Support de Windows (et Mac)

BOUTONS = {
    'no': 0,
    'A': 8,
    'B': 4,
    'HAUT': 2048,
    'BAS': 1024,
    'GAUCHE': 256,
    'DROITE': 512,
    'UP': 2048,
    'DOWN': 1024,
    'LEFT': 256,
    'RIGHT': 512,
    '+': 4096,
    '-': 16,
    'HOME': 128,
    '1': 2,
    '2': 1
}


# TODO: Détecter la déconnexion
class Buzzer:
    def __init__(self, team, dummy=False):
        self.wiimote = None
        self.connected = False
        self.dummy = dummy
        self.team = team
        self.async_connection_thread = None
        self.quit = False
        self.event_queue = Queue()  # Voir Buzzer.get_events()
        self.btn_state = {  # True correspond à down
            'A': False,
            'B': False,
            'HAUT': False,
            'BAS': False,
            'GAUCHE': False,
            'DROITE': False,
            '+': False,
            '-': False,
            'HOME': False,
            '1': False,
            '2': False
        }

        if not cwiid_found:
            self.dummy = True
            print "CWiid non trouvé, passage en mode dummy !"

    def __del__(self):
        """
        Attend la fermeture du thread de connexion asynchrone
        """
        t = self.async_connection_thread
        if t is not None:
            print "Attente du thread de connexion asynchrone...",
            self.quit = True
            t.join()
            print "terminé !"

    def wait_for_connection(self, tries=4, overwrite=False):
        """
        Attend qu'une Wiimote se connecte
        :param tries: Nombre de tentatives à effectuer avant de passer en mode dummy
        :param overwrite: Si cette instance de Buzzer a est déjà connectée à une wiimote, on supprime la connexion
        """
        if self.wiimote is not None:
            if overwrite:
                try:
                    self.wiimote.close()
                finally:
                    self.wiimote = None
            else:  # Déjà connecté et pas d'overwrite, donc on ne fait rien
                return

        while tries > 0 and not self.dummy and not self.quit:
            print "Tentative...",
            try:
                self.wiimote = cwiid.Wiimote()
            except RuntimeError:
                tries -= 1
                print "tentative échouée !"
            else:
                # Nous désirons avoir accès à l'état des boutons, à l'accéléromêtre et au Nunchuck
                # TODO: Gérer les évènements Nunchuck
                self.wiimote.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK

                # Gère les LEDs suivant le rôle de la wiimote et vibre pour notifier de la connexion
                if self.team == 'master':
                    self.allumer_led([1, 1, 1, 1])
                elif isinstance(self.team, int) and 1 <= self.team <= 4:
                    state = [0] * 4
                    state[self.team - 1] = 1
                    self.allumer_led(state)
                else:
                    self.allumer_led([1, 0, 0, 1])
                self.vibrer()
                self.connected = True
                print "Manette connectée !"

                # Initialise btn_state
                for btn, state in self.btn_state.items():
                    self.btn_state[btn] = self.is_down(btn)

                return
        else: # Echec
            if not self.dummy:
                print "Echec des tentatives de connexion, passage en mode dummy !"
                self.dummy = True

        if self.dummy:
            time.sleep(0.2)
            self.connected = True
            print "Manette connectée (dummy mode) !"
            return

        dialog = Dialog.Instance()
        dialog.new_message('error', 'Impossible de connecter la manette.')
        # TODO: Ne fonctionne pas
        raise RuntimeError('Impossible de connecter la manette.')

    def async_wait(self):
        """
        Démarre un thread qui va attendre la connexion d'une wiimote.
        """
        t = self.async_connection_thread
        if t is not None:
            print "Attente de l'ancien thread de connexion asynchrone...",
            t.join()
            print "terminé !"
        t = threading.Thread(target=self.wait_for_connection)
        t.start()

    def vibrer(self, temps=0.5):
        """
        Fait vibrer le Buzzer pendant un laps de temps défini.
        ATTENTION : Cette méthode est bloquante.
        :param temps: Le nombre de secondes pendant lequel vibrer.
        """
        if not self.dummy:
            self.wiimote.rumble = 1
            time.sleep(temps)
            self.wiimote.rumble = 0

    def allumer_led(self, tab):
        if not self.dummy:
            led = sum([((2 * tab[i]) ** i) * tab[i] for i in xrange(len(tab))])
            self.wiimote.led = led

    def is_down(self, btn):
        if self.dummy:
            return False
        if btn == 'any':
            return bool(self.wiimote.state['buttons'] != 0)
        else:
            return bool(self.wiimote.state['buttons'] & Buzzer.to_cwiid(btn))

    def update_events(self):
        """
        Ajoute les nouveaux évènements à la file. Voir Buzzer.get_events() pour le format des évènements.
        """
        for btn, old_state in self.btn_state.items():
            new_state = self.is_down(btn)
            self.btn_state[btn] = new_state
            if new_state != old_state:
                self.event_queue.put((btn, new_state))  # (id_btn, pressed)

    def get_events(self):
        """
        Renvoie la liste des nouveaux évènements en la vidant. Il n'y a pas besoin d'appeler update_events()
        avant celle-ci.
        Les éléments de la file sont des tuples comme ceci : (id_du_bouton: 1 à 4 ou 'master', pressé: boolean)
        :return: Une liste contenant les nouveaux évènements.
        """
        self.update_events()
        l = []
        while self.event_queue.qsize() > 0:
            l.append(self.event_queue.get())
        return l

    @staticmethod
    def to_cwiid(btn):
        btn = btn.upper()
        if btn in BOUTONS:
            return BOUTONS[btn]
        else:
            return 0
