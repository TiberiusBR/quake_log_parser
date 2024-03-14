import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.models.logparser import LogParser
from app.application import app
from app.dependencies.dependency import log_parser_dep
from app.models.game import Game


def log_parser_override():
    log_path = str(Path(__file__).resolve().parent) + "/sample_log_2.log"
    log_parser = LogParser(log_path=log_path)
    log_generator = log_parser.read_log()
    [log_parser.parse_log_line(log_line) for log_line in log_generator]
    return log_parser


def resolve_sample_log_path():
    log_sample_path = str(Path(__file__).resolve().parent) + "/sample_log.log"
    return log_sample_path


@pytest.fixture
def get_test_client() -> TestClient:
    app.dependency_overrides[log_parser_dep] = log_parser_override
    return TestClient(app=app)


@pytest.fixture(scope="module")
def create_log_sample():
    log_sample_path = resolve_sample_log_path()
    yield log_sample_path


@pytest.fixture()
def create_log_game():
    return r""" 20:37 InitGame: \sv_floodProtect\1\sv_maxPing\0\sv_minPing\0\sv_maxRate\10000\
        sv_minRate\0\sv_hostname\Code Miner Server\g_gametype\0\sv_privateClients\2\sv_maxclients\16\
            sv_allowDownload\0\bot_minplayers\0\dmflags\0\fraglimit\20\timelimit\15\g_maxGameClients\0\
                capturelimit\8\version\ioq3 1.36 linux-x86_64 Apr 12 2009\protocol\68\mapname\q3dm17\gamename\
                    baseq3\g_needpass\0 """


@pytest.fixture()
def create_log_player():
    logs = [
        r" 21:51 ClientConnect: 3",
        r" 21:51 ClientUserinfoChanged: 3 n\Dono da Bola\t\0\model\sarge/krusade\hmodel\sarge/krusade\g_redteam\\g_blueteam\\c1\5\c2\5\hc\95\w\0\l\0\tt\0\tl\0",
        r" 21:53 ClientUserinfoChanged: 3 n\Mocinha\t\0\model\sarge\hmodel\sarge\g_redteam\\g_blueteam\\c1\4\c2\5\hc\95\w\0\l\0\tt\0\tl\0",
    ]
    return logs


@pytest.fixture()
def create_log_kills():
    logs = [
        r" 22:06 Kill: 2 3 7: Isgalamido killed Mocinha by MOD_ROCKET_SPLASH",
        r" 22:06 Kill: 2 3 7: Isgalamido killed Mocinha by MOD_ROCKET_SPLASH",
        r" 22:18 Kill: 2 2 7: Isgalamido killed Isgalamido by MOD_ROCKET_SPLASH",
        r" 23:06 Kill: 1022 2 22: <world> killed Isgalamido by MOD_TRIGGER_HURT",
    ]
    return logs


@pytest.fixture()
def create_log_parser_with_game():
    test_parser = LogParser()
    test_parser.current_game = Game()
    return test_parser
