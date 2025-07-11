import requests
import json

def fetch_kill_data(character_id):
    url = f"https://zkillboard.com/api/kills/characterID/{character_id}/"
    headers = {"Accept-Encoding": "gzip"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {character_id}")
        return []

def calculate_total_isk(character_ids):
    unique_kills = {}
    
    for character_id in character_ids:
        kills = fetch_kill_data(character_id)
        for kill in kills:
            kill_id = kill['killmail_id']
            isk_value = kill['zkb'].get('destroyedValue', 0)
            kill['zkb'].get('')
            
            if kill_id not in unique_kills:
                unique_kills[kill_id] = isk_value
    
    total_isk = sum(unique_kills.values())
    return total_isk

if __name__ == "__main__":
    character_ids = [
        93382481
        #ADD here your character IDs for example: 93382481 or 2113893486 you can add multiple IDs like this: 93382481, 2113893486, 9999999999 and so on.
        #You can find your character ID in the URL of your zKillboard profile page https://zkillboard.com/
    ]
    total_isk_destroyed = calculate_total_isk(character_ids)
    print(f"Total ISK destroyed (unique kills only): {total_isk_destroyed:,.2f} ISK")
