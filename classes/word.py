"""
Module for generating random words
"""

from random import randint, shuffle
class Word:
    """
    Class for generating a random X-letter word from a directory
    """
    def __init__(self, current_dir, min_letters):
        self.words_dir = current_dir + "words\\"
        self.rand_word(min_letters)
        self.convert_word_to_unknown()
    def rand_word(self, min_letters=3):
        """
        Generates a random word with a number of letters not smaller than min_letters
        """
        word_len = randint(min_letters, 9)
        word_list = ""
        with open("{}\\{}_letters.txt".format(self.words_dir, word_len), "r") as word_reserve:
            word_list = word_reserve.read()
            word_list = word_list.split("\n")
        shuffle(word_list)
        choosen_word = word_list[randint(0, len(word_list) - 1)]
        self.word = choosen_word
    def convert_word_to_unknown(self):
        """
        Converts the randomly generated word to a list of underscores
        with the length of the randomly generated word
        """
        current_word = ["_"] * len(self.word)
        for i in range(0, len(self.word)):
            if self.word[i] == "-":
                current_word[i] = "-"
        self.current_word = current_word
