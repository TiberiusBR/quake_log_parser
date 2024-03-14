from fastapi import Request
from app.models.logparser import LogParser
import pathlib


def log_parser_dep():
    """
    Create a LogParser object from a quake game log.

    """
    log_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/data/qgames.log"
    log_parser = LogParser(log_path=log_path)
    log_generator = log_parser.read_log()
    [log_parser.parse_log_line(log_line) for log_line in log_generator]
    return log_parser
