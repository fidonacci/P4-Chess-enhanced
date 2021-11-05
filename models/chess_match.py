from typing import List, NamedTuple


class ChessMatch(NamedTuple):

    player1: List
    player2: List

    def serialize(self):
        match_dict = {}
        match_dict['player1'] = self.player1
        match_dict['player2'] = self.player2
        return match_dict

    @staticmethod
    def unserialize(match_dict):
        return ChessMatch(player1=match_dict['player1'], player2=match_dict['player2'])
