from models.player import Player
from views.view import View


class PlayerController:
    """Holds methods to handles players instances saved in the db"""
    def list_players(players_instances):
        """Returns a list of all players saved in db with choosen information: id, name, rank"""

        db_players_list = [[player.get_player_db_id(), player.name, player.rank]
                           for player in players_instances]
        return db_players_list

    def add_player_to_db():
        """Adds directly a players to db"""
        saved = False

        while not saved:  # handling existing player homonyms thanks to save_player() return

            player_values = View.add_player_prompts()
            player_instance = Player(**player_values)
            saved = player_instance.save_player()

    def modify_player_by_id():

        try:
            player_id = int(input("Player id to modify : "))
            player = Player.get_player_by_db_id(player_id)
            print(player)
            saved = False
            while not saved:
                player_values = View.add_player_prompts()
                saved = player.update_player(player_values)

        except (ValueError):
            print("Invalid Player Id")
