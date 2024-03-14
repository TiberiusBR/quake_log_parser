import re
from .player import Player
from app.enums.mod_enum import MeanOfDeath


class Game:
    def __init__(self, *args, **kwargs) -> None:
        self.players = kwargs["players"] if kwargs.get("players") else []
        self.game_id = kwargs["game_id"] if kwargs.get("game_id") else 0
        self.total_kills = kwargs["total_kills"] if kwargs.get("total_kills") else 0
        self.world_kills = kwargs["world_kills"] if kwargs.get("world_kills") else 0
        self.game_number = kwargs["game_number"] if kwargs.get("game_number") else 0
        self.death_methods = (
            kwargs["death_methods"] if kwargs.get("death_methods") else {}
        )

    @staticmethod
    def update_score(log_parser, log_line: str):
        """
        Updates the score for the current game in the log parser, from the current line.
        Adds a kill for the total score. If the killer is the <world>, adds a point to it.
        Removes a point from the player that died to the <world>
        Updates the Mean Of Death (MOD) dictionary for the current game.

            Parameters:
                log_parser(LogParser): A LogParser object.
                log_line(str): A line from a quake game log.
        """
        killer, died, mod = re.findall(r"Kill: (\d+) (\d+) (\d+)", log_line)[0]
        log_parser.current_game.add_total_kill()
        if killer == "1022":
            log_parser.current_game.add_world_kill()
            log_parser.current_game.get_player(died).score -= 1
        else:
            if killer != died:
                log_parser.current_game.get_player(killer).score += 1

        mod_name = MeanOfDeath(int(mod)).name
        try:
            log_parser.current_game.death_methods[mod_name] += 1
        except KeyError:
            log_parser.current_game.death_methods.update({mod_name: 1})

    def get_player(self, id) -> Player | None:
        """
        Searches for a player in the game and returns it.
        
            Parameters:
                id(str): Player supposed id.
            
            Returns:
                player(Player)
            
            Raises:
                IndexError: If the player isn't found.
        """
        try:
            return [player for player in self.players if player.id == id][0]
        except IndexError:
            return None

    def add_player(self, player):
        """
        Add a player to the game.

            Parameters:
                player(Player): A Player object.
        """
        self.players.append(player)

    def remove_player(self, player_name):
        """
        Remove a player from the game.

            Parameters:
                player_name(str): A player name. 
        """
        self.players.remove(player_name)

    def add_total_kill(self):
        """
        Add a kill point to the total_kills counter.
        """
        self.total_kills += 1

    def add_world_kill(self):
        """
        Add a kill point to the world_kills counter.
        """
        self.world_kills += 1

    def generate_game_report(self) -> dict:
        """
        Generate a game report containg multiple information from the game.
        """
        return {
            "game_id": self.game_id,
            "total_kills": self.total_kills,
            "world_kills": self.world_kills,
            "players": [p.name for p in self.players],
            "kills": {
                player_name: score
                for (player_name, score) in [p.tuple_info() for p in self.players]
            },
        }

    def generate_mod_report(self) -> dict:
        """
        Generate a game report containg all used death methods in the game.
        """
        return {
            "kills_by_means": self.death_methods,
        }
