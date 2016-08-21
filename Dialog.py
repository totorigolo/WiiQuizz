# coding: utf8

from WindowHelper import WindowHelper
from Singleton import Singleton
import time


@Singleton
class Dialog:
    def __init__(self):
        self.messages = []
        self.win = WindowHelper.Instance()

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

    """
        Ajoute un message
    """

    def new_message(self, type, message, mode='intrusive'):
        if type not in self.types:
            type = 'neutral'
        msg = {
            'type' : type,
            'message': message,
            'mode': mode,
            'time': time.time(),
            'active': True
        }
        if mode == 'intrusive':
            self._print_intrusive_msg(type, message)
            msg['active'] = False
        self.messages.append(msg)

    """
        Affiche un message intrusif
    """

    def _print_intrusive_msg(self, type, message):
        self.win.new_rect('dialog_color_shadow_'+type, 0, label='dialog_shadow')
        self.win.new_rect('dialog_color_'+type, 0, label='dialog_holder')
        self.win.new_text(message, 'dialog_font', self.correspondence_type_text_color[type], label='dialog_msg')
        self.win.new_text('Appuyez sur une touche pour continuer...', 'dialog_font_small', self.correspondence_type_text_color[type], label='dialog_msg_info')

        self.win.add('dialog_shadow', [0, 'right'], ['y_center - 75', 150])
        self.win.add('dialog_holder', [0, 'right'], ['y_center - 70', 140])
        self.win.add('dialog_msg', 'centered', 'centered')
        self.win.add('dialog_msg_info', 'centered', 'y_center + 40')

        self.win.refresh()

        def event_fun(pg, win, vars, event):
            if event.type == pg.KEYDOWN:
                return True
            return False

        self.win.event(event_fun=event_fun)  # On attend que quelqu'un appuie sur un bouton

        self.win.delete('dialog_shadow')
        self.win.delete('dialog_holder')
        self.win.delete('dialog_msg')
        self.win.delete('dialog_msg_info')

