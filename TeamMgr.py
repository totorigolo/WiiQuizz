# coding=utf-8

import os
import random

from Dialog import Dialog
from Singleton import Singleton
from Team import Team
from WindowHelper import WindowHelper


@Singleton
class TeamMgr:
    """
    Cette classe s'occupe de la gestion des équipes. C'est elle qui gère :
     - les scores
     - les pénalités ou bonus
     - les noms des équipes et leur couleur
     - l'affichage des scores
     - la joie à la victoire, et la déception à la défaite
    """

    @staticmethod
    def Instance():
        """
        Cette fonction est un workaround pour bénéficier de l'autocomplétion sur cette classe
        :rtype: TeamMgr
        """
        return TeamMgr.Instance()

    # TODO: J'ai apporté des modifs (max_simult_buzzer=1 obligatoirement). Il faudra rajouter des fonctionnalités, pour QuestionGame par exemple

    def __init__(self):
        """
        self.state peut prendre les valeurs :
          - 'accept' : accepte les buzzes
          - 'waiting_answer' : attend que le buzz soit accepté ou refusé (ou annulé)
          - 'waiting_msg' : affiche un message (perdu ou gagné), et attend skip_msg() pour redevenir 'accept'-ing
          - 'must_pick_one' : il faut appeler la fonction pick_one_buzz()
        :param max_simult_buzzer: nombre de personne pouvant buzzer simultanément (si -1, pas de restrictions)
        """
        self.teams = {}
        self.buzzing_teams = []
        self.wining_points = 0
        self.losing_points = 0
        self.set_score_mode()
        self.state = 'accept'  # voir docstring
        self.state_done = False
        self.waiting_msg = ''  # win ou lose
        self.delete_templates = None
        self.template_imported = False
        self.buzz_fun = self.default_buzz

        self.win = WindowHelper.Instance()
        self.dialog = Dialog.Instance()

        self.win.new_color((255, 0, 96), 'team1')
        self.win.new_color((252, 255, 0), 'team2')
        self.win.new_color((58, 119, 71), 'team3')
        self.win.new_color((255, 162, 0), 'team4')
        self.win.new_color((210, 4, 5), 'red_error')
        self.win.new_color((60, 154, 80), 'green_victory')

        self.win.new_font('Arial', 40, 'title')
        self.win.new_font('Arial', 70, 'very_big')

        self.win.new_sound(os.path.abspath('./res/buzzer.ogg'), 'sound_buzz')
        self.win.new_sound(os.path.abspath('./res/win.ogg'), 'sound_win')
        self.win.new_sound(os.path.abspath('./res/loose.ogg'), 'sound_loose')

        # Couleur des textes
        self.color_correspondence = {
            'team1': 'team2',
            'team2': 'team1',
            'team3': 'team4',
            'team4': 'team4'
        }

    def draw_on(self, page_label):
        """
        Affiche les scores sur la page
        :param page_label: label de la page sur lequel afficher les scores
        """
        if not self.template_imported:
            name_template = '{}_players'.format(len(self.teams))
            self.win.import_template(name_template)
            for id, team in self.teams.items():
                team_num = "team{}".format(id)
                self.win.edit_text('%s_result' % team_num, str(team.points))
                self.win.edit_color('%s_result' % team_num, self.color_correspondence[team_num])
            self.template_imported = True
        else:
            for id, team in self.teams.items():
                self.win.edit_text('team%d_result' % id, str(team.points))

        # Affichage si ce n'est pas déjà fait
        if not self.state_done:
            # Msg d'erreur si must_pick_one n'a pas été géré
            if self.state == 'must_pick_one':
                self.dialog.new_message('error', "Erreur: appeler la méthode pick_one_buzz()")

            # Une équipe vient de buzzer
            elif self.state == 'waiting_answer':
                team_text = "team{}".format(self.buzzing_teams[0])
                color = self.color_correspondence["team{}".format(self.buzzing_teams[0])]

                self.win.new_text(self.teams[self.buzzing_teams[0]].team_name, 'very_big', color,
                                  label="text_buzz_" + team_text)
                self.win.import_template('buzz_' + team_text)

            # Affichage de vrai ou faux
            elif self.state == 'waiting_msg':
                if self.waiting_msg == 'win':
                    self.win.import_template('good_answer')
                elif self.waiting_msg == 'lose':
                    self.win.import_template('bad_answer')

        self.state_done = True

        # Supprime les vieux templates si on a changé d'état
        if self.delete_templates is not None:
            if self.delete_templates == 'waiting_answer':
                for i in range(1, 4):
                    self.win.undo_template('buzz_team%d' % i)
            elif self.delete_templates == 'waiting_msg':
                self.win.undo_template('good_answer')
                self.win.undo_template('bad_answer')
            self.delete_templates = None

    def change_state(self, state):
        self.state_done = False
        if self.state == 'waiting_answer' or self.state == 'waiting_msg':
            self.delete_templates = self.state
        self.state = state

    def add_team(self, id, buzzer, team_name):
        """
        Ajoute un joueur.
        :param id: nom du joueur noms : 1 à 4
        :param buzzer: buzzer de l'équipe.
        :param team_name: Nom de l'équipe apparente (ex: Pastèque, Ananas, ...)
        """
        # TODO: Gérer 'new'
        self.teams[id] = Team(id, buzzer, team_name)
        self.template_imported = False

    def quit_game(self):
        self.template_imported = False

    def set_score_mode(self, mode='add_more', wining_points=None, loosing_points=None):
        """
        Permet de définir comment sont donnés les points pour une bonne ou une mauvaise réponse. La méthode d'ajout
        varie suivant le mode de score, indiqué par how_many.
        Les modes de score disponibles sont :
          - 'add_only' : add=Ajout de 500 points, loose=Retrait de zéro point.
          - 'add_more' : add=Ajout de 500 points, loose=Retrait de 100 point.
          - 'equal' : add=Ajout de 500 points, loose=Retrait de 500 point.
          - 'hardcore' : add=Ajout de 100 points, loose=Retrait de 500 point.
          - 'perso' : utilisation des points fournis en paramètres
        Le mode par défaut est 'add_more'.
        :param mode: nouveau mode à adopter
        :type wining_points: object
        :param loosing_points:
        """
        if mode == 'add_only':
            self.wining_points, self.losing_points = 500, 0
        elif mode == 'add_more':
            self.wining_points, self.losing_points = 500, 100
        elif mode == 'equal':
            self.wining_points, self.losing_points = 300, 300
        elif mode == 'hardcore':
            self.wining_points, self.losing_points = 100, 500
        elif mode == 'perso' and wining_points is not None and loosing_points is not None:
            self.wining_points, self.losing_points = wining_points, loosing_points
        else:
            print "Mode inconnu. Par défaut, mode 'add_more' utilisé."
            self.set_score_mode()

    def set_buzz_fun(self, fun):
        self.buzz_fun = fun

    def add_buzz(self, id, btn):
        self.buzz_fun(id, btn)

    def default_buzz(self, id, btn):
        """
        Ajoute un buzz à la liste. Il faut impérativement appeler pick_one_buzz() pour n'en garder qu'un seul.
        :param id: le buzzer à ajouter
        """
        if self.state == 'accept' or self.state == 'must_pick_one':
            self.buzzing_teams.append(id)
            self.teams[id].is_buzzing = True
            self.change_state('must_pick_one')

    def pick_one_buzz(self):
        """
        Ne garde qu'un seul buzzer, choisi au hasard.
        """
        if self.state == 'must_pick_one':
            random_id = random.choice(self.buzzing_teams)
            self.just_buzzed_now_waiting(random_id)

    def just_buzzed_now_waiting(self, id, display=True):
        self.win.play_sound('sound_buzz')
        self.clear_buzzes()

        self.buzzing_teams.append(id)
        self.teams[id].is_buzzing = True
        self.teams[id].buzzer.vibrer()

        if display:
            self.change_state('waiting_answer')
        else:
            self.change_state('waiting_answer_nodisplay')

    def accept_buzz(self, points=None):
        """
        Accepter un buzz (ex: bonne réponse) et invalide les autres buzzes.
        :param id: id de l'équipe, ou 'random' pour être équitable
        :param points: nombre de point à ajouter. Ne pas fournir points (None) revient à utiliser le score_mode en cours
        :return: nombre de points ajoutés. None si pas de point ajoutés et False si id n'a pas buzzé
        """
        if points is None:
            points = self.wining_points
        if self.buzz_fun != self.default_buzz:
            self.buzz_fun('accept', None)
        try:
            id = random.choice(self.buzzing_teams)
            self.buzzing_teams.remove(id)
        except ValueError:
            return False
        else:
            self.teams[id].add_points(points)
            self.clear_buzzes()
            self.change_state('waiting_msg')
            self.waiting_msg = 'win'
            self.win.play_sound('sound_win')
        return points

    def refuse_buzz(self, points=None):
        """
        Refuser un buzz (ex: mauvaise réponse) et invalide les autres buzzes.
        :param id: id de l'équipe, ou 'random' pour être équitable
        :param points: nombre de point à retirer. Ne pas fournir points (None) revient à utiliser le score_mode en cours
        :return: nombre de points retirés. None si pas de point retirés et False si id n'a pas buzzé
        """
        if points is None:
            points = self.losing_points
        if self.buzz_fun != self.default_buzz:
            self.buzz_fun('refuse', None)
        try:
            id = random.choice(self.buzzing_teams)
            self.buzzing_teams.remove(id)
        except ValueError:
            return False
        else:
            self.teams[id].add_points(-points)
            self.clear_buzzes()
            self.change_state('waiting_msg')
            self.waiting_msg = 'lose'
            self.win.play_sound('sound_loose')
        return -points

    def cancel_buzz(self):
        """
        Annule un buzz.
        :param id: id de l'équipe à annuler
        :return: True si l'annulation a réussi, False sinon.
        """
        if self.buzz_fun != self.default_buzz:
            self.buzz_fun('cancel', None)
        try:
            id = random.choice(self.buzzing_teams)
            self.buzzing_teams.remove(id)
        except ValueError:
            return
        else:
            self.teams[id].is_buzzing = False
            self.change_state('accept')
        return True

    def clear_buzzes(self):
        """
        Annule tous les buzzes.
        """
        for t in self.buzzing_teams:
            self.teams[t].is_buzzing = False
        self.buzzing_teams = []
        self.change_state('accept')

    def skip_msg(self):
        """
        Quand state est 'waiting_msg', passe en attente de buzz (à state = 'accept')
        """
        if self.state == 'waiting_msg':
            self.change_state('accept')

    def awaiting_buzzes(self):
        """
        :return: Renvoie True si au moins un buzzer a buzzé, False sinon.
        """
        return len(self.buzzing_teams) > 0

    def add_points(self, id, points):
        """
        Ajoute des points à une équipe. ATTENTION : utiliser accept_buzz et refuse_buzz pour gérer les buzzers et
        ajouter des points dans le même temps. Cette fonction sert, par exemple, à ajouter des bonus aux équipes.
        :param id: id de l'équipe
        :param points: nombre de points à ajouter. Fournir un nombre négatif pour en enlever.
        """
        self.teams[id].add_points(points)

    def get_best_team(self):
        """
        Permet de connaitre la ou les meilleure(s) équipe, en terme de score.
        :return: Un tableau contenant la meilleure équipe, ou les meilleurs si ex-aequo
        """
        max_points = 0
        best_players = []
        for name, p in self.teams.items():
            if p.points == max_points:
                best_players.append(name)
            elif p.points > max_points:
                best_players = []
                max_points = p.points
        return best_players
