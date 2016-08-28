# coding: utf8

import time

from ElementWatcher import ElementWatcher
from Singleton import Singleton
from WindowHelper import WindowHelper


@Singleton
class Dialog:
    @staticmethod
    def Instance():
        """
        Cette fonction est un workaround pour bénéficier de l'autocomplétion sur cette classe
        :rtype: Dialog
        """
        return Dialog.Instance()

    def __init__(self):
        self.messages = []
        self.win = WindowHelper.Instance()

        if self.win.current_page == -1:  # Si pas de page d'ouverte
            self.win.new_page('Erreur', label='dialog_default')
            self.win.go_to('dialog_default')

        self.templates_options = {
        }

        self.types = ['error', 'success', 'warning', 'neutral']

        self.correspondence_type_text_color = {
            'error': 'white',
            'success': 'white',
            'warning': 'black',
            'neutral': 'black'
        }

        self.win.new_font('Arial', 30, 'dialog_font')
        self.win.new_font('Arial', 16, 'dialog_font_small')

        self.win.new_color('white')
        self.win.new_color('black')

        self.win.new_color((238, 69, 69), 'dialog_color_error')
        self.win.new_color((203, 38, 38), 'dialog_color_shadow_error')

        self.win.new_color((66, 188, 68), 'dialog_color_success')
        self.win.new_color((42, 144, 45), 'dialog_color_shadow_success')

        self.win.new_color((243, 221, 74), 'dialog_color_warning')
        self.win.new_color((218, 179, 44), 'dialog_color_shadow_warning')

        self.win.new_color((217, 217, 217), 'dialog_color_neutral')
        self.win.new_color((111, 111, 111), 'dialog_color_shadow_neutral')

    def settings(self, opt=None):
        self.templates_options.update(opt)

    def new_message(self, type, message, mode='intrusive'):
        """
            Ajoute un message
        """
        if type not in self.types:
            type = 'neutral'
        msg = {
            'type': type,
            'message': message,
            'mode': mode,
            'time': time.time(),  # TODO: Ajouter des messages temporels
            'active': True
        }
        if mode == 'intrusive':
            self._print_intrusive_msg(type, message)
            msg['active'] = False
        self.messages.append(msg)

    def _print_intrusive_msg(self, type, message):
        """
            Affiche un message intrusif
        """
        with ElementWatcher('dialog_watcher'):
            self.win.new_rect('dialog_color_shadow_' + type, 0, label='dialog_shadow')
            self.win.new_rect('dialog_color_' + type, 0, label='dialog_holder')
            self.win.new_text(message, 'dialog_font', self.correspondence_type_text_color[type], label='dialog_msg')
            self.win.new_text('Appuyez sur une touche pour continuer...', 'dialog_font_small',
                              self.correspondence_type_text_color[type], label='dialog_msg_info')

            self.win.import_template('dialog_messages', opt=self.templates_options)

            self.win.refresh()

            def event_fun(pg, win, vars, event):
                if event.type == pg.KEYDOWN or (
                                    event.type == pg.USEREVENT and event.wiimote_id == 'master' and event.pressed == True):
                    return True
                return False

            self.win.event(event_fun=event_fun)  # On attend que quelqu'un appuie sur un bouton
