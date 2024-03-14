from .fixtures import get_test_client


def test_read_main(get_test_client):
    client = get_test_client
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_games(get_test_client):
    expected_response = [
        {
            "game_id": 1,
            "total_kills": 2,
            "world_kills": 1,
            "players": ["Isgalamido", "Dono da Bola"],
            "kills": {"Isgalamido": 0, "Dono da Bola": 0},
        }
    ]
    client = get_test_client
    response = client.get("/log/games")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == expected_response


def test_get_game(get_test_client):
    expected_response = {
        "game_id": 1,
        "total_kills": 2,
        "world_kills": 1,
        "players": ["Isgalamido", "Dono da Bola"],
        "kills": {"Isgalamido": 0, "Dono da Bola": 0},
    }

    client = get_test_client
    response = client.get("/log/game/1")
    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_non_existent_game(get_test_client):
    expected_response = {"status": "No game found in this index."}
    client = get_test_client
    response = client.get("/log/game/3")
    assert response.status_code == 404
    assert response.json() == expected_response


def test_get_games_mod(get_test_client):
    expected_response = [
        {"game_1": {"kills_by_means": {"MOD_TRIGGER_HURT": 1, "MOD_ROCKET_SPLASH": 1}}}
    ]
    client = get_test_client
    response = client.get("/log/games/mod")
    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_game_mod(get_test_client):
    expected_response = {"kills_by_means": {"MOD_TRIGGER_HURT": 1, "MOD_ROCKET_SPLASH": 1}}
    
    client = get_test_client
    response = client.get("/log/game/1/mod")
    assert response.status_code == 200
    assert response.json() == expected_response
