from app.models.logparser import LogParser
from app.models.game import Game
from app.models.player import Player
from .fixtures import (
    create_log_sample,
    create_log_game,
    create_log_kills,
    create_log_player,
    create_log_parser_with_game,
)


def test_read_log_and_return_the_lines_amount(create_log_sample):
    test_parser = LogParser(log_path=create_log_sample)
    lines = [line for line in test_parser.read_log()]
    assert len(lines) == 148


def test_parse_new_game_line(create_log_game):
    test_parser = LogParser()
    test_parser.parse_log_line(create_log_game)
    assert test_parser.game_count == 1


def test_parse_add_player_id_line_and_update_name(
    create_log_parser_with_game, create_log_player
):
    test_parser = create_log_parser_with_game
    [test_parser.parse_log_line(log_line=line) for line in create_log_player]
    cur_player = test_parser.current_game.players[0]
    assert cur_player.id == "3"
    assert cur_player.name == "Mocinha"


def test_parse_kills(create_log_parser_with_game, create_log_kills):
    test_parser = create_log_parser_with_game
    game = test_parser.current_game
    game.add_player(Player(id="2"))
    [test_parser.parse_log_line(log_line=line) for line in create_log_kills]
    player = game.get_player("2")
    assert player.score == 1
    assert game.total_kills == 4
    assert game.world_kills == 1
