import re


class Player:
    def __init__(self, *args, **kwargs) -> None:
        self.id = kwargs["id"] if kwargs.get("id") else "0"
        self.name = kwargs["name"] if kwargs.get("name") else ""
        self.score: int = kwargs["score"] if kwargs.get("score") else 0

    @staticmethod
    def create_player(log_parser, log_line):
        """
        Tries to create a player for the specified LogParser, from the current log line.

            Parameters:
                log_parser(LogParser): A LogParser object.
                log_line(str): A line from a quake game log.
        """
        user_id = re.findall(r"Client(Connect|UserinfoChanged): (.)", log_line)[0][1]
        if log_parser.current_game.get_player(user_id):
            return
        log_parser.current_game.add_player(Player(id=user_id))

    @staticmethod
    def update_player(log_parser, log_line):
        """
        Tries to update a player name for the current game in the log parser.
        Parses the player info from the current log line.

            Parameters:
                log_parser(LogParser): A LogParser object.
                log_line(str): A line from a quake game log.
        """
        player_id, new_name = re.findall(
            r"ClientUserinfoChanged: (.) n\\([a-zA-Z\s]+)", log_line
        )[0]
        found_player = log_parser.current_game.get_player(player_id)
        if found_player is not None:
            found_player.rename_player(new_name)

    def __eq__(self, player: object) -> bool:
        return self.id == player.id

    def rename_player(self, new_name):
        """
        Renames the player.
        """
        self.name = new_name

    def tuple_info(self):
        return (self.name, self.score)
