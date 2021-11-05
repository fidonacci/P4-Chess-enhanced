from tinydb import TinyDB, Query
from models.round import Round
from models.player import Player

db = TinyDB("db.json")
tournaments_table = db.table("Tournaments Table")
TournamentQuery = Query()

NUMBER_OF_ROUNDS = 4


class Tournament:
    """Tournament model"""

    def __init__(self,
                 name="",
                 date="",
                 location="",
                 time_control="",
                 description="",
                 number_of_rounds=NUMBER_OF_ROUNDS) -> None:

        self.name = name
        self.date = date
        self.location = location
        self.number_of_rounds = number_of_rounds
        self.rounds = [Round(f"Round {round_number+1}") for round_number in range(self.number_of_rounds)]
        self.players = []
        self.time_control = time_control
        self.description = description

    def serialize(self):
        "Serializes Tournament instance in order to store it in a database - Returns a dict"
        serialized_tournament = {}
        serialized_tournament['name'] = self.name
        serialized_tournament['date'] = self.date
        serialized_tournament['location'] = self.location
        serialized_tournament['time_control'] = self.time_control
        serialized_tournament['description'] = self.description
        serialized_tournament['number_of_rounds'] = self.number_of_rounds
        serialized_tournament['players'] = [player.serialize() for player in self.players]
        serialized_tournament['rounds'] = [round.serialize() for round in self.rounds]

        return serialized_tournament

    @staticmethod
    def unserialize(serialized_tournament: dict):
        "Unserializes a Tournament stored in a database to return a Tournament instance"
        tournament_object = Tournament()
        tournament_object.name = serialized_tournament['name']
        tournament_object.date = serialized_tournament['date']
        tournament_object.location = serialized_tournament['location']
        tournament_object.time_control = serialized_tournament['time_control']
        tournament_object.description = serialized_tournament['description']
        tournament_object.number_of_rounds = serialized_tournament['number_of_rounds']
        tournament_object.players = [Player.unserialize(serialized_player)
                                     for serialized_player in serialized_tournament['players']]
        tournament_object.rounds = [Round.unserialize(serialized_round)
                                    for serialized_round in serialized_tournament['rounds']]

        return tournament_object

    def save_tournament(self):
        """Stores a tournament instance in the database"""
        tournaments_table.insert(self.serialize())

    def get_tournament_db_id(self):
        """Gets the id given by Tinydb to the instance storage"""
        return tournaments_table.get(TournamentQuery.name == self.name).doc_id

    def delete_tournament(tournament):
        """Takes a Tournament to delete its storage in the database based on its name"""
        if tournaments_table.get(TournamentQuery.name == tournament.name) is not None:
            tournaments_table.remove(tournaments_table.name == tournament.name)
        else:
            raise Exception("No tournament of this name exists in the database")
        return None

    def get_tournament_by_db_id(id_tournament: int):
        """Returns a Tournament instance based on its storage id in Tinydb"""
        return Tournament.unserialize(tournaments_table.get(doc_id=id_tournament))

    def update_tournament(self):
        """Overwites a Tournament storage in the database based on the new values of the Tournament instance"""
        tournaments_table.update(self.serialize(), doc_ids=[self.get_tournament_db_id()])

    def load_db_tournaments():
        return [Tournament.unserialize(tournament) for tournament in tournaments_table.all()]
