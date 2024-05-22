from tinydb import TinyDB, Query
import os
import json
from datetime import datetime

JSON_DATA_PLAYERS_PATH = "data/data_players.json"


class Player:

    def __init__(self):
        """Initialisation de la base de données des joueurs"""

        self.db_player = TinyDB(
            JSON_DATA_PLAYERS_PATH, indent=4, encoding="utf-8"
            )
        self.players = self.db_player.table("Players")
        if not os.path.exists(JSON_DATA_PLAYERS_PATH):
            with open(JSON_DATA_PLAYERS_PATH, "w") as f:
                json.dump([], f)

    def write_player(self, surname, name, birth_date, national_id):
        """ Écriture des données d'un joueur dans la base de données"""

        self.data = {
            "surname": surname,
            "name": name,
            "birth_date": birth_date,
            "national_id": national_id,
        }
        self.players.insert(self.data)
        return national_id

    def player_exists(self, national_id):
        """recherche si le joueur existe dans la DB"""

        existing_player = self.players.get(Query().national_id == national_id)
        if existing_player:
            return True
        else:
            return False

    def find_player(self, national_id):
        """Recherche d'un joueur par son ID national"""

        player_data = self.players.search(Query().national_id == national_id)
        if player_data:
            return player_data[0]
        else:
            return None

    def get_all_player_id(self):
        """Retourne tout les ID des joueurs"""

        player_data = self.players.all()
        sorted_id = sorted(player_data, key=lambda x: x["national_id"])
        players_ids = []
        for ids in sorted_id:
            players_ids.append(ids["national_id"])
        return players_ids

    def get_all_player_name(self):
        """Retourne tout les noms des joueurs"""

        player_name = []
        player_data = self.players.all()
        sorted_name = sorted(player_data, key=lambda x: x["name"])
        for name in sorted_name:
            player_name.append(name["name"])
        return player_name

    def remove_player(self, national_id):
        """Supprime un joueur de la DB"""

        self.players.remove(Query().national_id == national_id)
        player_data = self.players.search(Query().national_id == national_id)
        if not player_data:
            return True  # retourne true si le joueur est suppr

    def check_birday(self):
        """Vérifie si c'est l'anniversaire d'un joueur"""

        player_data = self.players.all()
        today = datetime.today()
        for player in player_data:
            birth_date = datetime.strptime(
                player.get("birth_date", ""), "%d-%m-%Y"
                )
            if birth_date.month == today.month and birth_date.day == today.day:
                player_name = (
                    f"{player.get('name', '')} {player.get('surname', '')}"
                    )
                return player_name
        return None


if __name__ == "__main__":
    pass
