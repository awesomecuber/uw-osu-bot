from ..osu_api import api_helper


class Player:
    def __init__(self, player_json):
        self.player_id = player_json["id"]
        self.username = player_json["username"]
        self.rank = player_json["statistics"]["global_rank"]

    def update(self) -> None:
        player = api_helper.get_player_by_id(self.player_id)
        self.player_id = player.player_id
        self.username = player.username
        self.rank = player.rank
