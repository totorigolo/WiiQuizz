# coding: utf8

import threading
import time

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

        if not cwiid_found:
            self.dummy = True
            print "CWiid non trouvé, passage en mode dummy !"

    def wait_for_connection(self, tries=4, overwrite=False):
        """ Attend qu'une Wiimote se connecte """
        if self.wiimote is not None:
            if overwrite:
                try:
                    self.wiimote.close()
                finally:
                    self.wiimote = None
            else: # Déjà connecté et pas d'overwrite, donc on ne fait rien
                return

        while tries > 0 and not self.dummy:
            print "Tentative..."
            try:
                self.wiimote = cwiid.Wiimote()
            except:
                tries -= 1
            else:
                self.wiimote.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK

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
                break
        else: # Echec
            if not self.dummy:
                print "Echec des tentatives de connexion, passage en mode dummy !"
                self.dummy = True

        if self.dummy:
            time.sleep(2)
            self.connected = True
            print "Manette connectée (dummy mode) !"
            return

    def async_wait(self):
        t = threading.Thread(target=self.wait_for_connection)
        t.start()
        # TODO: Faire un t.join() dans le destructeur

    def vibrer(self, temps=0.5):
        self.wiimote.rumble = 1
        time.sleep(temps)
        self.wiimote.rumble = 0

    def allumer_led(self, tab):
        led = sum([((2 * tab[i]) ** i) * tab[i] for i in xrange(len(tab))])
        self.wiimote.led = led

    def is_pressed(self, btn):
        if btn == 'any':
            return bool(self.wiimote.state['buttons'] != 0)
        else:
            return bool(self.wiimote.state['buttons'] & Buzzer.to_cwiid(btn))

    @staticmethod
    def to_cwiid(btn):
        if btn in BOUTONS:
            return BOUTONS[btn]
        else:
            return 0
