"""
Module that contains the game class, responsible for coordinating all methods of word generation,
user-input, players' scores, drawing and typing text
"""
from random import shuffle
import pygame as pg
from gallow import Gallow
from player import Player
from word import Word

class Game:
    """
    The class used to initaite a new game, enabling (1-8) players to play the game.
    """
    pg.init()
    colors = {"black": (0, 0, 0), "white": (255, 255, 255), "blue": (130, 130, 255),
              "gold": (255, 255, 100), "red": (255, 0, 0), "green": (0, 255, 0)}
    monitor_dims = (pg.display.Info().current_w, pg.display.Info().current_h)
    min_letters_map = {"2": 3, "4": 5, "6": 7, "7": 8, "8": 8}
    max_wrong_guesses = 8
    font = "hand-writing.ttf"
    def __init__(self, current_dir, title, fps, window_dims=(0, 0), aspect_ratio=True):
        pg.display.set_caption(title)
        self.current_dir = current_dir
        self.player_list = Player.get_players()
        self.window_dims = window_dims
        self.font = self.current_dir + Game.font
        if window_dims != (0, 0):
            if aspect_ratio:
                height = round((Game.monitor_dims[1] / Game.monitor_dims[0]) * window_dims[0])
                self.window_dims = (window_dims[0], height)
            self.window = pg.display.set_mode(self.window_dims)
        else:
            self.window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
            self.window_dims = pg.display.get_surface().get_size()
        self.size_adjust = self.window_dims[0] / Game.monitor_dims[0]
        background_img = pg.image.load(self.current_dir + "images\\background.jpg")
        self.background = pg.transform.scale(background_img, self.window_dims)
        self.first_line = 0.55
        self.second_line = self.first_line + 0.10
        width = self.window_dims[0]
        height = self.window_dims[1]
        self.origin = (0, 0)
        self.gallow = Gallow(self.current_dir, self.window, self.origin,
                             self.size_adjust, self.first_line * height)
        self.layout_thickness = 7 * self.size_adjust
        self.hang_seperator_1 = 0.58
        self.hang_seperator_2 = self.hang_seperator_1 + 0.25
        x_box = width - (width -  self.hang_seperator_2 * width  - self.layout_thickness) / 2
        y_box = (self.first_line * height) / 2
        self.letter_box_center = (x_box, y_box)
        self.mistake_timeout = 0
        self.msg = "Welcome to the game!"
        self.current_letter = ""
        self.guessed_letters = []
        self.last_guess = False
        self.wrong_guesses = 0
        self.wins = [0, 0]
        self.choosen_word = ""
        self.rope_fully_down = False
        if self.main_loop(fps):
            self.exit_game()
            pg.quit()
    @staticmethod
    def check_for_events():
        """
        Checks if the user presses the exit button or the ESC key.\n
        @return: 'Q' or 'P' respectively (for 'Quit' and 'Pause').
        """
        keys = pg.key.get_pressed()
        if keys[pg.K_LALT] or keys[pg.K_RALT]:
            if keys[pg.K_F4]:
                return "EXIT"
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "EXIT"
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return "MIN"
                if event.key == pg.K_RETURN:
                    return "ENTER"
                return event.unicode
        return "NONE"
    def guess(self, num_player):
        """
        Evaluates the guess of a player.\n
        @param num_player: The index of the player in the player list.
        """
        if not self.current_letter:
            return False
        if self.current_letter in self.guessed_letters:
            self.msg = "You've already guessed '{}'! Try a different letter!"
            self.msg = self.msg.format(self.current_letter)
            return False
        self.guessed_letters.append(self.current_letter)
        if self.current_letter in self.choosen_word.word:
            player_name = self.player_list[num_player].name
            self.msg = "Correct guess! Player {} gets a point!".format(player_name)
            self.last_guess = True
            for i in range(0, len(self.choosen_word.current_word)):
                if self.choosen_word.word[i] == self.current_letter:
                    self.choosen_word.current_word[i] = self.current_letter
        else:
            left = Game.max_wrong_guesses - self.wrong_guesses - 1
            self.msg = "Wrong guess! {} wrong guesses left!".format(left)
            self.last_guess = False
        return True
    def type_text(self, txt, size, location, clr):
        """
        Types the given text on the screen.\n
        """
        font_size = round(size * self.size_adjust)
        font = pg.font.Font(self.font, font_size)
        txt_surface = font.render(txt, True, clr)
        txt_rect = txt_surface.get_rect()
        txt_rect.center = (location[0], location[1])
        self.window.blit(txt_surface, txt_rect)
    def draw_layout(self):
        """
        Draws the lines dictating the layout of the screen.
        """
        line_clr = Game.colors["white"]
        width = (self.hang_seperator_2 - self.hang_seperator_1) * self.window_dims[0]
        pg.draw.rect(self.window, line_clr,
                     (0, self.first_line * self.window_dims[1],
                      self.window_dims[0], self.layout_thickness))
        pg.draw.rect(self.window, line_clr,
                     (0, self.second_line * self.window_dims[1],
                      self.window_dims[0], self.layout_thickness))
        hang_sep_height = self.first_line * self.window_dims[1]
        pg.draw.rect(self.window, line_clr, (self.hang_seperator_1 * self.window_dims[0],
                                             0, self.layout_thickness, hang_sep_height))
        pg.draw.rect(self.window, line_clr, (self.hang_seperator_2 * self.window_dims[0],
                                             0, self.layout_thickness, hang_sep_height))
        hang_sep_1_start = (self.hang_seperator_1 * self.window_dims[0])
        score_sep_1_x = hang_sep_1_start + self.layout_thickness + (width * (3 / 6))
        score_sepy_y = self.first_line * self.window_dims[1] - 65 * self.size_adjust
        pg.draw.rect(self.window, line_clr, (score_sep_1_x,
                                             0, self.layout_thickness, score_sepy_y))
        score_sep_2_x = hang_sep_1_start + self.layout_thickness + (width * (4 / 6))
        pg.draw.rect(self.window, line_clr, (score_sep_2_x,
                                             0, self.layout_thickness, score_sepy_y))
        pg.draw.rect(self.window, line_clr, (self.hang_seperator_1 * self.window_dims[0],
                                             score_sepy_y, width, self.layout_thickness))
    def draw_letter_box(self):
        """
        Draws the box in which the letters the user guess are typed.
        """
        window_width = self.window_dims[0]
        width = (window_width - (self.hang_seperator_2 * window_width + self.layout_thickness)) / 2
        height = self.letter_box_center[1]
        rect = (self.letter_box_center[0] - width / 2,
                self.letter_box_center[1] - height / 2, width, height)
        pg.draw.rect(self.window, Game.colors["blue"], rect, round(7 * self.size_adjust))
    def draw_all(self):
        """
        Draws all the objects on the screen.
        """
        self.gallow.draw_all()
        self.draw_layout()
        self.draw_letter_box()
    def sort_player_list(self):
        """
        Returns a sorted list of the players by each player's total score.
        """
        current_list = self.player_list[:]
        sorted_list = []
        while current_list:
            biggest = -1
            biggest_index = 0
            for i in range(0, len(current_list)):
                if current_list[i].total_score >= biggest:
                    biggest_index = i
                    biggest = current_list[i].total_score
            sorted_list.append(current_list.pop(biggest_index))
        return sorted_list
    def type_stats(self):
        """
        Types the stats of the players (Total score of each player,the score of
        each player in the current round, and the number of times the players won).
        """
        sorted_list = self.sort_player_list()
        beginning_space = 20 * self.size_adjust
        first_sep = self.hang_seperator_1 * self.window_dims[0]
        second_sep = self.hang_seperator_2 * self.window_dims[0]
        width = second_sep - (first_sep + self.layout_thickness)
        x_pos = first_sep + self.layout_thickness
        height = self.first_line * self.window_dims[1]
        row_height = (1 / 9) * height
        font_size = 40
        font_color = Game.colors["gold"]
        for i in range(0, len(sorted_list)):
            name = sorted_list[i].name
            this_x = x_pos + (1.02 / 4) * width
            y_pos = row_height * i
            self.type_text(name, font_size, (this_x, y_pos + beginning_space), font_color)
        for i in range(0, len(sorted_list)):
            score = sorted_list[i].score
            this_x = x_pos + (3.6 / 6) * width
            y_pos = row_height * i
            self.type_text(str(score), font_size, (this_x, y_pos + beginning_space), font_color)
        for i in range(0, len(sorted_list)):
            total = sorted_list[i].total_score
            this_x = x_pos + (5.1 / 6) * width
            y_pos = row_height * i
            self.type_text(str(total), font_size, (this_x, y_pos + beginning_space), font_color)
        msg = "Wins: " + str(self.wins[0]) + " / " + str(self.wins[1])
        this_x = x_pos + width / 2
        this_y = height - row_height / 2
        self.type_text(msg, 60, (this_x, this_y), Game.colors["white"])
    def type_all(self):
        """
        Types all the text-data on the screen.
        """
        layout_first_line = self.first_line * self.window_dims[1]
        layout_second_line = self.second_line * self.window_dims[1]
        first_line_end = layout_first_line + self.layout_thickness
        second_line_end = layout_second_line + self.layout_thickness
        mid_lower_screen = second_line_end + (self.window_dims[1] - second_line_end) / 2
        between_lines = first_line_end + (layout_second_line - first_line_end) / 2
        text_location = (self.window.get_rect().center[0], mid_lower_screen)
        font_clr = None
        finished = self.wrong_guesses >= Game.max_wrong_guesses
        finished = finished or not "_" in self.choosen_word.current_word
        if not finished:
            font_clr = Game.colors["gold"]
        elif self.last_guess:
            font_clr = Game.colors["green"]
        else:
            font_clr = Game.colors["red"]
        self.type_text(" ".join(self.choosen_word.current_word), 175,
                       text_location, font_clr)
        text_location = (self.window.get_rect().center[0], between_lines)
        self.type_text(self.msg, 50, text_location, Game.colors["white"])
        self.type_text(self.current_letter, 175, self.letter_box_center, Game.colors["white"])
        self.type_stats()
    def exit_game(self):
        """
        Exits the game.
        """
    def lower_rope(self):
        """
        Smoothly lowers the hanging rope by a certain amount (self.mistake_timeout)
        """
        rope_speed = 0.5
        if self.mistake_timeout > 0:
            self.mistake_timeout -= rope_speed
            self.gallow.hang_progress += rope_speed
        else:
            self.mistake_timeout = 0
        if self.wrong_guesses >= Game.max_wrong_guesses and self.gallow.hang_progress < 100:
            self.gallow.hang_progress += rope_speed
        elif self.gallow.hang_progress >= 100:
            leg_inter = self.gallow.gallow_data["parts"]["man"]["leg_intersection"]
            new_y = leg_inter[1] - 20 * self.size_adjust
            self.gallow.gallow_data["parts"]["man"]["leg_intersection"] = (leg_inter[0], new_y)
            self.rope_fully_down = True
    def new_word(self):
        """
        Generates a new random word. The length of the word is based on the number of the players.
        The more the players are, the longer the word is.
        """
        for case in Game.min_letters_map:
            if len(self.player_list) <= int(case):
                self.choosen_word = Word(self.current_dir, Game.min_letters_map[case])
                break
    def main_loop(self, fps):
        """
        Coordinates everything that happens during the game and calls all the
        functions responsible for drawing, text, input, and scores.\n
        @param fps: The number of Frames Per Second.
        """
        self.new_word()
        self.gallow.pre_load_gallow_parts()
        rand_player_list = list(range(0, len(self.player_list)))
        shuffle(rand_player_list)
        just_guessed = False
        first = True
        finished = False
        while True:
            pg.time.delay(round(1000 / fps))
            self.window.blit(self.background, (0, 0))
            if self.wrong_guesses >= self.max_wrong_guesses:
                if self.rope_fully_down:
                    self.gallow.tremble()
            if not self.rope_fully_down:
                self.lower_rope()
            self.type_all()
            self.draw_all()
            pg.display.flip()
            if first:
                pg.time.delay(1500)
                first = False
            event = Game.check_for_events()
            player_name = self.player_list[rand_player_list[0]].name
            if not just_guessed and not finished:
                self.msg = "Please guess a letter, {}.".format(player_name)
            if len(event) == 1 and not just_guessed:
                if ord(event.lower()) >= 97 and ord(event.lower()) <= 122:
                    self.current_letter = event.lower()
            if event == "EXIT":
                pg.quit()
                return False
            if event == "MIN":
                pg.display.iconify()
            elif event == "ENTER":
                if just_guessed:
                    just_guessed = False
                    continue
                if finished:
                    if self.current_letter == "y":
                        rand_player_list = list(range(0, len(self.player_list)))
                        shuffle(rand_player_list)
                        just_guessed = False
                        self.new_word()
                        self.guessed_letters = []
                        self.gallow.hang_progress = 0
                        self.rope_fully_down = False
                        self.gallow.pre_load_man()
                        self.wrong_guesses = 0
                        self.mistake_timeout = 0
                        finished = False
                        for player in self.player_list:
                            player.score = 0
                    elif self.current_letter == "n":
                        pg.quit()
                        return False
                    continue
                if self.guess(rand_player_list[0]) and self.current_letter:
                    if self.last_guess:
                        self.player_list[rand_player_list[0]].score += 1
                        self.player_list[rand_player_list[0]].total_score += 1
                    else:
                        self.wrong_guesses += 1
                        self.mistake_timeout += 100 / Game.max_wrong_guesses
                    rand_player_list.pop(0)
                    if not rand_player_list:
                        rand_player_list = list(range(0, len(self.player_list)))
                        shuffle(rand_player_list)
                    if self.wrong_guesses >= Game.max_wrong_guesses:
                        self.msg = "You've lost! The man has been hanged!"
                        self.choosen_word.current_word = self.choosen_word.word.split()
                        finished = True
                    elif "_" not in self.choosen_word.current_word:
                        self.msg = "You've won! You've saved the man!"
                        self.wins[0] += 1
                        finished = True
                    if finished:
                        self.wins[1] += 1
                        just_guessed = False
                        self.msg += " Play again? (Y / N)"
                        continue
                if self.current_letter:
                    just_guessed = True
        return True
            