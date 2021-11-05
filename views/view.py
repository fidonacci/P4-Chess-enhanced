from typing import List
from simple_term_menu import TerminalMenu
from datetime import date
import re
from tabulate import tabulate


class View:

    def home_menu():
        options = ["Start New Tournament", "Load Tournament", "Reports", "Exit"]
        terminal_menu = TerminalMenu(options, title="\nHome Menu")
        menu_entry_index = terminal_menu.show()
        return options[menu_entry_index]

    def wrapper_menu(function):

        def wrapper():

            function()
            options = ["Save Tournament", "Continue"]
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            return menu_entry_index

        return wrapper

    def prompt_for_round_results(round_number):
        return print(4*"\n" + f"ROUND {round_number}" + "\n"
                     + "########################################")

    def prompt_for_match_result_player1(match_description):
        return input(f"Match opposing {match_description}" +
                     "  ----  Player1 score: ")

    def prompt_for_match_result_player2(match_description):
        return input(f"Match opposing {match_description} " +
                     " ----  Player2 score: ")

    def show_players_list(db_players_list: List):

        print("\nSaved Players List".upper())
        print("##########################")

        print(tabulate(db_players_list,  headers=['Player Id', 'Player Name', 'Rank']))

    def show_tournament_results(players_ranking_list: List):

        print("\nTournament Results List".upper())
        print("##########################")

        players = []
        for player in players_ranking_list:
            players.append(player)

        print(tabulate(players,  headers=['Player id', 'Name', 'Score']))

    def show_db_tournaments_list(db_tournaments_list: List):

        print("\nSaved Tournaments List".upper())
        print("##########################")

        tournaments_presntation = []

        for tournament in db_tournaments_list:
            tournaments_presntation.append(tournament)

        print(tabulate(tournaments_presntation,  headers=[
              'Tournament Name', 'Number of rounds', 'Date', 'Tournament id']))

    def new_tournament_prompts():

        print("\nNew Tournament".upper())
        print("##########################")

        # Taking a free string as a name

        tournament_name = input("Tournament name :")

        # Enforcing date as DD/MM/YYYY

        tournament_date = input("Tournament date (system date if left empty) :")

        if tournament_date == "":

            tournament_date = date.today().strftime("%d/%m/%Y")

        while not bool(re.search(r"^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$",
                                 tournament_date)):

            print("Not a proper date format! Try a date format DD/MM/YYYY")
            tournament_date = input("Tournament date (system date if left empty) :")

        # Taking a free string as a location

        tournament_location = input("Location :").capitalize()

        # Taking an option as a time control

        options = ["Bullet", "Blitz", "Rapid"]

        terminal_menu = TerminalMenu(options, title="Time Control:", clear_menu_on_exit=False)

        menu_entry_index = terminal_menu.show()

        tournament_time_control = options[menu_entry_index]

        # Taking a free string as a description

        tournament_description = input("Description :")

        return {'name': tournament_name, 'date': tournament_date, 'location': tournament_location,
                'time_control': tournament_time_control, 'description': tournament_description}

    def choose_player_method_menu():
        options = ["Select existing player by id", "Show existing players list", "Add a new Player"]
        terminal_menu = TerminalMenu(options, title="Loaded Tournament Menu")
        menu_entry_index = terminal_menu.show()
        return options[menu_entry_index]

    def player_adding_titile(player_number):
        print(f"\nPlayer {player_number}".upper())
        print("##########################")

    def add_player_prompts(player_number):

        View.player_adding_titile(player_number)

        # Taking a free string as a first name

        player_first_name = input("Player first name : ")

        # Taking a free string as a last name

        player_last_name = input("Player last name : ")

        # Enforcing date as DD/MM/YYYY

        player_birth_date = input("Birth date : ")

        while not bool(re.search(r"^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$",
                                 player_birth_date)):

            print("Not a proper date format! Try a date format DD/MM/YYYY")
            player_birth_date = input("Tournament date (system date if left empty) :")

        # Taking an option as a sex

        options = ["Male", "Female"]

        terminal_menu = TerminalMenu(options, title="Sex : ", clear_menu_on_exit=False)

        menu_entry_index = terminal_menu.show()

        player_sex = options[menu_entry_index]

        # Enforcing date as DD/MM/YYYY

        player_rank = input("Rank :")

        while not bool(re.search(r"^\d+$", player_rank)):

            print("Not a proper rank entry! Rank must be a digit")

            player_rank = input("Rank :")

        return {'first_name': player_first_name, 'last_name': player_last_name,
                'birth_date': player_birth_date, 'sex': player_sex, 'rank': player_rank}

    def load_tournament_prompt():
        return input("\nEnter tournament id to load : ")

    def load_tournament_menu():
        options = ["Overwrite rounds starting Round number",  "Back to Home Menu"]
        terminal_menu = TerminalMenu(options, title="\nLoaded Tournament Menu")
        menu_entry_index = terminal_menu.show()
        return options[menu_entry_index]

    def saved_players_list_options():
        options = ["Sort by alphabetical order",  "Sort by players rank", ]
        terminal_menu = TerminalMenu(options, title="\nLoaded Tournament Menu")
        menu_entry_index = terminal_menu.show()
        return options[menu_entry_index]

    def saved_tournaments_list_options():
        options = ["Show Tournament Players",  "Show Tournament Rounds", "Show Tournament Matchs"]
        terminal_menu = TerminalMenu(options, title="\nLoaded Tournament Menu")
        menu_entry_index = terminal_menu.show()
        return options[menu_entry_index]

    def saved_tournaments_players_list_options():
        options = ["Sort by alphabetical order",  "Sort by players rank"]
        terminal_menu = TerminalMenu(options, title="\nLoaded Tournament Menu")
        menu_entry_index = terminal_menu.show()
        return options[menu_entry_index]

    def reports_menu():
        options = ["Saved Players list",  "Saved Tournaments List"]
        terminal_menu = TerminalMenu(options, title="\nLoaded Tournament Menu")
        menu_entry_index = terminal_menu.show()
        return options[menu_entry_index]

    def show_rounds_list(tournament_rounds_list):
        print("\nTournament Rounds List".upper())
        print("##########################")

        print(tabulate(tournament_rounds_list,  headers=['Round name', 'Matchs']))

    def show_matchs_list(tournament_matchs_list):
        print("\nTournament Rounds List".upper())
        print("##########################")

        print(tabulate(tournament_matchs_list,  headers=['Player 1', 'Score Player 1', 'Player 2', 'Score Player 2']))
