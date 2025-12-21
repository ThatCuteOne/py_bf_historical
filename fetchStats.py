import requests
from requests import RequestException
from typing import Any, Dict, Optional
from datetime import datetime

import sqlUtils

def get_json(url: str, params: Optional[Dict[str, Any]] = None, timeout: float = 5.0) -> Dict[str, Any]:
    """Send a GET request to the given URL and parse the response as JSON."""
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except RequestException as exc:
        raise exc
    except ValueError:
        raise ValueError(f"Response from {url} was not valid JSON.")

def fetchCloudStats():
    data = get_json("https://blockfrontapi.vuis.dev/api/v1/cloud_data")
    print("\nFetch Process: Fetched cloud stats")
    print("\nFetch Process: Storing stats in database...")
    data_tuple = (
        datetime.now().isoformat(),
        data.get("players_online"),
        data.get("game_player_count").get("dom"),
        data.get("game_player_count").get("tdm"),
        data.get("game_player_count").get("inf"),
        data.get("game_player_count").get("gg"),
        data.get("game_player_count").get("ttt"),
        data.get("game_player_count").get("boot"),
    )
    sqlUtils.add_stats(data_tuple)

def fetchMatchStats(name):
    data = get_json("https://blockfrontapi.vuis.dev/api/v1/player_status?name=" + name)
    if data.get("online") == False:
        print("Player is offline.")
        return f"{name} is offline."
    if not data.get('match'):
        print("No match data found for player.")
        return "Name not found or player is not in a match."
    bulk_uuid = []
    count = 0
    for test in data.get('match').get('players'):
        print(test['uuid'])
        count += 1
        bulk_uuid.append(test['uuid'])
    print("\nFetch Process: Fetched player UUIDs")
    print(str(bulk_uuid).strip("[]").replace("'", "").replace(" ", ""))
    players_in_match_data=requests.post("https://blockfrontapi.vuis.dev/api/v1/player_data/bulk", data=str(bulk_uuid).strip("[]").replace("'", "").replace(" ", ""))

    return players_in_match_data.json(), count

if __name__ == "__main__":
    fetchMatchStats("SleepNeeded24_7")

def fetchStats():
    fetchCloudStats()