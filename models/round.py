from models.chess_match import ChessMatch


class Round:
    def __init__(self, name) -> None:
        self.name = name
        self.chess_matchs = []
        self.start_time = ""
        self.end_time = ""

    def serialize(self):
        round = {}
        round['name'] = self.name
        round['chess_matchs'] = [chess_match.serialize() for chess_match in self.chess_matchs]
        round['start_time'] = self.start_time
        round['end_time'] = self.end_time
        return round

    def unserialize(round: dict):
        round_object = Round(round['name'])
        round_object.chess_matchs = [ChessMatch.unserialize(chess_match) for chess_match in round['chess_matchs']]
        round_object.start_time = round['start_time']
        round_object.end_time = round['end_time']
        return round_object
