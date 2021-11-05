
from models.player import Player


class PlayerController:
    """Holds methods to handles players instances saved in the db"""
    def list_players(players_instances=Player.load_db_players()):
        """Returns a list of all players saved in db with choosen information: id, name, rank"""
        db_players_list = [[player.get_player_db_id(), player.name, player.rank]
                           for player in players_instances]
        return db_players_list
