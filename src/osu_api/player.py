class Player:
    def __init__(self, player_json):
        self.player_id = player_json["id"]  # type: int
        self.username = player_json["username"]  # type: str
        self.rank = player_json["statistics"]["global_rank"]  # type: int
