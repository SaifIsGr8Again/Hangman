"""
Module for the Player Class.
"""

class Player:
    """
    Class for modelling the players in the game. Tracks each player's number of wins and score.
    Provides functions for requesting players' names from the users.
    """
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.total_score = 0
    def add_point(self):
        """
        Adds a point to the player's score and his total score.
        """
        self.total_score += 1
        self.score += 1
    @staticmethod
    def request_player_name(player_num, restrictions):
        """
        Asks the user to type a name to assign to a player.\n
        @param player_num: The number of the player.\n
        @param restrictions: Names that have been already taken.
        """
        name = ""
        name_range = (3, 8)
        restricted = False
        while len(name) < name_range[0] or len(name) > name_range[1] or restricted:
            msg = "Please type the name of player #{} ({}-{} characters): "
            name = input(msg.format(player_num, name_range[0], name_range[1]))
            if name in restrictions:
                restricted = True
                print("\n'{}' has been already taken! Try a different one!\n".format(name))
            else:
                restricted = False
        return name
    @staticmethod
    def get_player_nums(num_range):
        """
        Gets the number of the players from the users.
        """
        num_players = "0"
        while True:
            msg = "Please type the number of players ({}-{}): "
            num_players = input(msg.format(num_range[0], num_range[1]))
            if len(num_players) == 1:
                if ord(num_players) >= ord(str(num_range[0])):
                    if ord(num_players) <= ord(str(num_range[1])):
                        break
        return int(num_players)
    @staticmethod
    def get_players():
        """
        Requests the number of players from the users and to type a name for each player.
        @return: A list of objects for each player.
        """
        player_list = []
        name_list = []
        player_num = Player.get_player_nums((1, 8))
        for i in range(0, player_num):
            player_list.append(Player(Player.request_player_name(i + 1, name_list)))
            name_list.append(player_list[-1].name)
        return player_list
