from views.view import View
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController
from models.tournament import Tournament
from models.player import Player


class MainController():
    """MainController to start the Home Menu"""

    def start_new_tournament():
        """Starts a new Tournament"""
        TournamentController.start_new_tournament()

    def load_db_tournament():
        """Loads an existing saved tournament"""
        TournamentController.load_db_tournament()

    def show_reports():
        """Shows reports of saved items: tournaments, players, rounds, matchs"""
        choice = View.reports_menu()
        "Saved Players list",  "Saved Tournaments List"
        if choice == "Saved Players list":

            sub_choice = View.saved_players_list_options()
            if sub_choice == "Sort by alphabetical order":
                View.show_players_list(sorted(PlayerController.list_players(
                    Player.load_db_players()), key=lambda player: player[1]))
            elif sub_choice == "Sort by players rank":
                View.show_players_list(sorted(PlayerController.list_players(Player.load_db_players()),
                                              key=lambda player: int(player[2]), reverse=True))

            sub_choice2 = View.saved_players_list_options_after_show()

            if sub_choice2 == "Add Player":
                PlayerController.add_player_to_db()

            elif sub_choice2 == "Modify Player":
                PlayerController.modify_player_by_id()

            elif sub_choice2 == "Back to Home Menu":
                pass

        elif choice == "Saved Tournaments List":
            View.show_db_tournaments_list(
                sorted(TournamentController.list_db_tournaments(), key=lambda tournament: tournament[3]))

            sub_choice = View.saved_tournaments_list_options()

            if sub_choice == "Show Tournament Players":

                try:
                    tournament_id = int(input("Tournament id to show Players for : "))

                    tournament_players_list = TournamentController.tournament_players_list(
                        Tournament.get_tournament_by_db_id(tournament_id))

                    sub_choice2 = View.saved_players_list_options()

                    if sub_choice2 == "Sort by alphabetical order":
                        View.show_players_list_with_scores(
                            sorted(tournament_players_list, key=lambda player: player[1]))
                    elif sub_choice2 == "Sort by players rank":
                        View.show_players_list_with_scores(
                            sorted(tournament_players_list, key=lambda player: int(player[2]), reverse=True))
                except (ValueError, IndexError, TypeError):
                    print("Invalid tournament id")

            elif sub_choice == "Show Tournament Rounds":
                try:
                    tournament_id = input("Tournament id to show Rounds for : ")
                    tournament_rounds = Tournament.get_tournament_by_db_id(int(tournament_id)).rounds
                    tournament_rounds_presentation = [[round.name, round.start_time, round.end_time,
                                                       RoundController.present_round_matchs(round)]
                                                      for round in tournament_rounds]
                    View.show_rounds_list(sorted(tournament_rounds_presentation, key=lambda round: round[0]))
                except (ValueError, TypeError):
                    print("Please Enter a valid tournament id and stop trying to crash my program :-)")
                    return None

            elif sub_choice == "Show Tournament Matchs":
                try:
                    tournament_id = input("Tournament id to show Matchs for : ")
                    tournament_matchs = []
                    for round in Tournament.get_tournament_by_db_id(int(tournament_id)).rounds:
                        tournament_matchs += round.chess_matchs
                    tournament_matchs_presentation = [[Player.get_player_by_db_id(match[0][0]), match[0][1],
                                                       Player.get_player_by_db_id(match[1][0]), match[1][1]]
                                                      for match in tournament_matchs]

                    View.show_matchs_list(tournament_matchs_presentation)
                except (ValueError, TypeError):
                    print("Please Enter a valid tournament id and stop trying to crash my program :-)")
                    return None

    def home_menu():
        """Home Menu controller"""
        choice = ""

        while not choice == "Exit":

            choice = View.home_menu()

            if choice == "Start New Tournament":
                MainController.start_new_tournament()
            elif choice == "Load Tournament":
                MainController.load_db_tournament()
            elif choice == "Reports":
                MainController.show_reports()
            elif choice == "Exit":
                exit
