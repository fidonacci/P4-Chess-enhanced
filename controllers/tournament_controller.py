from models.tournament import NUMBER_OF_ROUNDS, Tournament
from models.player import Player
from models.chess_match import ChessMatch
from controllers.player_controller import PlayerController
from views.view import View


class TournamentController:

    def add_player(tournament: Tournament, player: Player):
        """Adds a player given in agrment to a tournament given in argument"""

        tournament.players.append(player)

    def rank_grid(tournament: Tournament, round_number):
        """Returns a list of lists [player id, score, rank] sorted by score then by rank"""

        last_round = tournament.rounds[round_number-1]
        current_round_players = []

        for chess_match in last_round.chess_matchs:
            current_round_players.append(
                chess_match.player1 + [Player.get_player_by_db_id(chess_match.player1[0]).rank])
            current_round_players.append(
                chess_match.player2 + [Player.get_player_by_db_id(chess_match.player2[0]).rank])

        sorted_round_players = sorted(current_round_players, key=lambda player: (player[1], player[2]), reverse=True)

        return sorted_round_players

    def extract_players(tournament: Tournament, chess_matchs):
        matchs_players = []
        for chess_match in chess_matchs:
            matchs_players.append([chess_match[0][0], chess_match[1][0]])
        return matchs_players

    def generate_round_matchs(tournament: Tournament, round_number: int):
        """Generate matchs fo each round according to the Swiss system"""

        if round_number == 1:

            players_grid = sorted(tournament.players, key=lambda player: int(player.rank), reverse=True)

            first_half_grid = players_grid[:int(len(players_grid)/2)]

            second_half_grid = players_grid[int(len(players_grid)/2):]

            tournament.rounds[0].chess_matchs = []

            for position in range(len(first_half_grid)):

                chess_match = ChessMatch([first_half_grid[position].get_player_db_id(), ""],
                                         [second_half_grid[position].get_player_db_id(), ""])
                tournament.rounds[0].chess_matchs.append(chess_match)

        elif round_number > 1:
            ranked_grid = TournamentController.rank_grid(tournament, round_number-1)
            tournament.rounds[round_number-1].chess_matchs = []

            while len(ranked_grid) > 0:

                player_position = 1
                first_player = ranked_grid[0]
                second_player = ranked_grid[player_position]

                match_players_to_verify1 = [first_player[0], second_player[0]]
                match_players_to_verify2 = [second_player[0], first_player[0]]

                for round in tournament.rounds:
                    if match_players_to_verify1 in \
                            TournamentController.extract_players(tournament, round.chess_matchs) \
                            or match_players_to_verify2 in \
                            TournamentController.extract_players(tournament, round.chess_matchs):

                        player_position += 1

                ranked_grid.remove(first_player)
                ranked_grid.remove(second_player)
                tournament.rounds[round_number -
                                  1].chess_matchs.append(ChessMatch([first_player[0], 0], [second_player[0], 0]))

        tournament.update_tournament()

    def enter_round_results(tournament: Tournament, round_number: int):

        View.prompt_for_round_results(round_number)

        for chess_match in tournament.rounds[round_number-1].chess_matchs:

            player1_name = Player.get_player_by_db_id(chess_match.player1[0]).name
            player2_name = Player.get_player_by_db_id(chess_match.player2[0]).name

            match_description = f"{player1_name} to {player2_name}"

            player1_score = float(View.prompt_for_match_result_player1(match_description))

            while player1_score not in [0, 0.5, 1]:
                print("Score should be 0 or 0.5 or 1")
                player1_score = float(View.prompt_for_match_result_player1(match_description))

            chess_match.player1[1] = player1_score

            chess_match.player2[1] = 1 - player1_score

    def calculate_results(tournament: Tournament):

        tournament_players_ranking_list = []

        for player in tournament.players:

            player_score = 0

            for round in tournament.rounds:

                for chess_match in round.chess_matchs:

                    if Player.get_player_db_id(player) == int(chess_match[0][0]):
                        player_score += int(chess_match[0][1])
                    elif Player.get_player_db_id(player) == int(chess_match[1][0]):
                        player_score += int(chess_match[1][1])

            tournament_players_ranking_list.append([Player.get_player_db_id(player), player.name, player_score])

        sorted_tournament_players_ranking_list = sorted(
            tournament_players_ranking_list, key=lambda x: x[2], reverse=True)

        return View.show_tournament_results(sorted_tournament_players_ranking_list)

    def list_db_tournaments():
        db_tournaments_instances = Tournament.load_db_tournaments()
        db_tournaments_list = [[tournament.name, tournament.number_of_rounds, tournament.date,
                                tournament.get_tournament_db_id()]
                               for tournament in db_tournaments_instances]
        return db_tournaments_list

    def process_rounds(tournament: Tournament, start_round_number=1, end_round_number=NUMBER_OF_ROUNDS):

        for round_number in range(start_round_number, end_round_number+1):
            print("round tour ----------------------------------------------")
            TournamentController.generate_round_matchs(tournament, round_number)
            tournament.update_tournament()

            TournamentController.enter_round_results(tournament, round_number)
            tournament.update_tournament()

        TournamentController.calculate_results(tournament)

    def add_new_player(tournament: Tournament, player_number):

        saved = False

        while not saved:

            player_values = View.add_player_prompts(player_number)
            player_instance = Player(**player_values)
            saved = player_instance.save_player()
            if saved:
                TournamentController.add_player(tournament, player_instance)

        tournament.update_tournament()

    def choose_players_method(tournament: Tournament, player_number):

        choice = View.choose_player_method_menu()
        if choice == "Select existing player by id":
            View.player_adding_titile(player_number)
            player_id = input("\n Id of the Player to add : ")

            try:
                player_instance = Player.get_player_by_db_id(int(player_id))
                if int(player_id) in [Player.get_player_db_id(player) for player in tournament.players]:
                    print(f"Player already registred in this tournament - Retry for player {player_number} ")
                    return False

                else:
                    TournamentController.add_player(tournament, player_instance)
            except TypeError:
                print("Unexisting player id please take a look to the players list")
                return False

        elif choice == "Show existing players list":
            View.show_players_list(PlayerController.list_db_players())
            return False
        elif choice == "Add a new Player":
            TournamentController.add_new_player(tournament, player_number)

    def start_new_tournament():
        tournament_values = View.new_tournament_prompts()
        tournament = Tournament(**tournament_values)
        tournament.save_tournament()

        for player_number in range(8):
            valid_player = False
            while valid_player is False:
                valid_player = TournamentController.choose_players_method(tournament, player_number+1)

        TournamentController.process_rounds(tournament)

    def load_db_tournament():
        View.show_db_tournaments_list(TournamentController.list_db_tournaments())
        tournament_id = int(View.load_tournament_prompt())
        try:
            tournament = Tournament.get_tournament_by_db_id(tournament_id)
        except TypeError:
            print('Unrecognized Tournament id, please see valid ids in Saved Tournaments List')
            return None

        choice = View.load_tournament_menu()

        if choice == "Overwrite rounds starting Round number":

            round_number = int(input("Round number to start with : "))
            TournamentController.process_rounds(tournament, round_number)

        elif choice == "Back to Home Menu":
            pass

    def tournament_players_list(tournament: Tournament):

        return [[player.get_player_db_id(), player.name, player.rank]
                for player in tournament.players]
