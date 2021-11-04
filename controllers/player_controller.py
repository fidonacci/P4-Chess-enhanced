
from models.player import Player


class PlayerController:
    def list_players(players_instances=Player.load_db_players()):

        db_players_list = [[player.get_player_db_id(), player.name, player.rank]
                           for player in players_instances]
        return db_players_list
