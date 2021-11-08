from tinydb import TinyDB, Query

db = TinyDB("db.json")
players_table = db.table("Players Table")
PlayerQuery = Query()


class Player:
    """Player Model with attributes according to specifications"""

    def __init__(self, first_name="", last_name="", birth_date="", sex="", rank="") -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.rank = rank
        self.name = self.first_name + " " + self.last_name

    def serialize(self):

        player = {}
        player['first_name'] = self.first_name
        player['last_name'] = self.last_name
        player['birth_date'] = self.birth_date
        player['sex'] = self.sex
        player['rank'] = self.rank
        player['name'] = self.first_name + " " + self.last_name

        return player

    @staticmethod
    def unserialize(player: dict):
        player_object = Player()
        player_object.first_name = player['first_name']
        player_object.last_name = player['last_name']
        player_object.birth_date = player['birth_date']
        player_object.sex = player['sex']
        player_object.rank = player['rank']
        player_object.name = player['first_name'] + " " + player['last_name']

        return player_object

    def __str__(self) -> str:
        return self.name

    def save_player(self):
        """Saves a player in the database and return true if he does not already exist"""
        if players_table.get(PlayerQuery.name == self.name) is None:
            players_table.insert(self.serialize())
            return True
        else:
            print("Player already existing in the database - Resubmit current player")
            return False

    def update_player(self, player_values):
        """Overwites a Player storage in the database based on the new values of the Player instance"""
        player_id = self.get_player_db_id()
        players_table.update(player_values, doc_ids=[player_id])
        players_table.update({'name': player_values['first_name'] + " " +
                             player_values['last_name']}, doc_ids=[player_id])

        return True

    def get_player_db_id(self):
        return players_table.get(PlayerQuery.name == self.name).doc_id

    def delete_player(player):
        if players_table.get(PlayerQuery.name == player.name) is not None:
            players_table.remove(PlayerQuery.name == player.name)
        else:
            raise Exception("No player of this name exists in the database")
        return None

    def get_player_by_db_id(player_id: int):
        return Player.unserialize(players_table.get(doc_id=player_id))

    def load_db_players():
        return [Player.unserialize(player) for player in players_table.all()]
