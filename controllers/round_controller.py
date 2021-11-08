from models.round import Round
from models.player import Player


class RoundController():
    """Handles methods to manage rounds"""

    def present_round_matchs(round: Round):

        matchs_presentation_string = ""

        for match in round.chess_matchs:
            import pdb; pdb.set_trace()
            player1_name = Player.get_player_by_db_id(match.player1[0]).name
            player1_score = match.player1[1]
            player2_name = Player.get_player_by_db_id(match.player2[0]).name
            player2_score = match.player2[1]

            matchs_presentation_string += f"\nPlayer 1: {player1_name} vs .Player 2: {player2_name} \
                                            Result: {player1_score} - {player2_score}"

        return matchs_presentation_string
