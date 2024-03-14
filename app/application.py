from fastapi import FastAPI, Depends, Response
from typing import Annotated
from app.exceptions.exceptions import NoneTypeCaught
from app.models.logparser import LogParser
from app.dependencies.dependency import log_parser_dep
from app.schemas.game import GameSchema

app = FastAPI(
    title="QuakeLogParser",
    summary="Rest API that generates reports on quake games log.",
    contact={"name": "Felipe Freire", "email": "souza.freire@ftc.edu.br"},
)


@app.get(
    "/log/games",
    status_code=200,
    response_model=list[GameSchema],
    summary="Create a Report for all Games",
)
def get_games(
    response: Response, log_parser: Annotated[LogParser, Depends(log_parser_dep)]
):
    games = log_parser.games
    if not games:
        response.status_code = 204
        return
    return [game.generate_game_report() for game in games]


@app.get(
    "/log/game/{id}",
    status_code=200,
    response_model=dict,
    summary="Create a Report for one Game",
)
def get_game_report(
    id: int,
    response: Response,
    log_parser: Annotated[LogParser, Depends(log_parser_dep)],
):
    game = log_parser.get_game(id)
    if game is None:
        response.status_code = 404
        return {"status": "No game found in this index."}
    return game.generate_game_report()


@app.get(
    "/log/games/mod",
    status_code=200,
    response_model=list[dict],
    summary="Create a MOD report for all games",
)
def get_games_mod(log_parser: Annotated[LogParser, Depends(log_parser_dep)]):
    mod_report = [
        {f"game_{str(count+1)}": game.generate_mod_report()}
        for count, game in enumerate(log_parser.games)
    ]
    return mod_report


@app.get(
    "/log/game/{id}/mod",
    status_code=200,
    response_model=dict,
    summary="Create a mod report for one game",
)
def get_game_mod_report(
    id: int,
    response: Response,
    log_parser: Annotated[LogParser, Depends(log_parser_dep)],
):
    game = log_parser.get_game(id)
    if game is None:
        response.status_code = 404
        return {"status": "No game found in this index."}
    return game.generate_mod_report()


@app.get("/")
def health_check():
    return {"status": "ok"}


# This allow us to create a different log parser instance for our testing.
