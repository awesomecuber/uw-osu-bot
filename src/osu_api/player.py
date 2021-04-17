class Player:
    def __init__(self, player_json):
        self.player_id = player_json["id"]  # type: int
        self.username = player_json["username"]  # type: str
        self.rank = player_json["statistics"]["global_rank"]  # type: int

    async def update(self) -> None:
        from . import api_helper
        new_player = await api_helper.get_player_by_id(self.player_id)
        self.username = new_player.username
        self.rank = new_player.rank
