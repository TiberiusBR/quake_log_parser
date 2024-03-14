# Quake Log Parser

A log parser made in Python that collects relevant information from quake games logs and serves them in a RestAPI.


## Getting Started

It's recommended to create a virtual environment to locally install your packages:
```
python -m venv venv
```
After, activate your venv and install the packages:
``` 
pip install -r requirements.txt
```
And start the API:
```
uvicorn main:app
```
## Tests
To check and run all tests, first install the dev packages:
```
pip install -r requirements-dev.txt
```
Then, simply run:
```
pytest -s
```
For the code coverage, run:
```
coverage run -m pytest -s
coverage report
```
A ``.coverage`` file will be created at the root folder.
## Routes

All routes and return types can also be accessed with more details from "/docs".
### GET: `/log/game/{id}`
**Return a report from a single specified quake game.**
**Status Code:** ``200`` | ``204``
**Response Example:**
```
{
	"game_id":7,
	"total_kills":130,
	"world_kills":27,
	"players":[
		"Oootsimo",
		"Isgalamido",
		"Zeh",
		"Dono da Bola",
		"Mal",
		"Assasinu Credi",
		"Chessus"
	],
	"kills":{
		"Oootsimo":20,
		"Isgalamido":14,
		"Zeh":8,
		"Dono da Bola":10,
		"Mal":-3,
		"Assasinu Credi":19,
		"Chessus":0}
	}
}
```
### GET: `` /log/game/{id}/mod  ``
**Return a report about all Means of Death that appeared in a specific game.**
**Status Code:** ``200`` 
**Response Example:**
```
{
   "kills_by_means":{
      "MOD_TRIGGER_HURT":12,
      "MOD_ROCKET":27,
      "MOD_ROCKET_SPLASH":32,
      "MOD_SHOTGUN":6,
      "MOD_RAILGUN":10,
      "MOD_MACHINEGUN":7,
      "MOD_FALLING":1
   }
}
```
### GET: ``/log/games  `` 
**Return a report for all quake games.**
**Status Code:** ``200`` | ``204``
**Response Example:**
```
[
	{
		"game_id":1,
		"total_kills":0,
		"world_kills":0,
		"players":["Isgalamido"],
		"kills":{
			"Isgalamido":0
		}
	},
	{
		"game_id":2,
		"total_kills":11,
		"world_kills":8,
		"players":["Isgalamido","Mocinha"],
		"kills":{
			"Isgalamido":-7,
			"Mocinha":0
			}
	},
	{
		"game_id":3,
		"total_kills":4,
		"world_kills":3,
		"players":["Dono da Bola","Isgalamido","Zeh"],
		"kills":{
			"Dono da Bola":-1,
			"Isgalamido":1,
			"Zeh":-2
			}
	},
...]
```


### GET: ``/log/games/mod  ``
**Return a report about all Means of Death that appeared in all games.**
**Status Code:** ``200`` 
**Response Example:**
```
[
   {
      "game_1":{
         "kills_by_means":{
            
         }
      }
   },
   {
      "game_2":{
         "kills_by_means":{
            "MOD_TRIGGER_HURT":7,
            "MOD_ROCKET_SPLASH":3,
            "MOD_FALLING":1
         }
      }
   },
   {
      "game_3":{
         "kills_by_means":{
            "MOD_ROCKET":1,
            "MOD_TRIGGER_HURT":2,
            "MOD_FALLING":1
         }
      }
   }
...]
```
