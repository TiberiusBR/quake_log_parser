import re
from typing import Generator
from app.exceptions.exceptions import NoneTypeCaught
from .game import Game
from .player import Player


class LogParser:
    def __init__(self, *args, **kwargs) -> None:
        self.log_path = kwargs["log_path"] if kwargs.get("log_path") else None
        self.current_game: Game | None = None
        self.game_count = 0
        self.games = []

    def get_game(self, game_id) -> Game:
        """
        Searches for a specified game by its id.

            Parameters:
                game_id(int): A game identifier.
            
            Returns:
                game(Game)
                None: if the game isn't found.
        """
        for game in self.games:
            if game.game_id == game_id:
                return game
        return None

    def read_log(self) -> Generator:
        """
        Reads a log file containg a quake game log.

            Returns:
                line(str)
        """
        with open(self.log_path) as log:
            for line in log:
                yield line

    def add_game(self):
        """
        Adds the current game to the games list.
        """
        self.game_count += 1
        self.current_game = Game(game_number=self.game_count, game_id=self.game_count)
        self.games.append(self.current_game)

    def parse_log_line(self, log_line):
        """
        Resolve a quake log event based on the current log line.
        The event can be divided upon:
        'InitGame' - Creates a new game and adds to the counter.
        'ClientConnect' - Adds the id of a new player to the current game.
        'ClientUserinfoChanged' - Changes the player name found by id
        'Kill' - Adds a kill from the player or the <world> to the current game.
        """
        event_pattern = re.compile(r"(^.{0,7})([a-zA-Z]*)")
        try:
            event_type = event_pattern.search(log_line).group(2)
            if not event_type:
                return
        except IndexError:
            return

        match event_type:
            case "InitGame":
                # Create a new Game.
                self.add_game()
            case "ClientConnect":
                # Create a new User by its ID.
                Player.create_player(self, log_line)
            case "ClientUserinfoChanged":
                # Update name of existent user ID.
                Player.update_player(self, log_line)
            case "Kill":
                # Add a score to a certain user, or diminish a point.
                Game.update_score(self, log_line)

    def generate_games_report(self):
        """
        Generates a report for all games parsed.

            Returns:
                game_report(list[dict]): Info from all games.
        """
        game_report = []
        for game in self.games:
            game_report.append(
                {f"game_{game.game_number}": game.generate_game_report()}
            )
        return game_report
