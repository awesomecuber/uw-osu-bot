class Player:
    def __init__(self, player_json):
        self.player_id: int = player_json["id"]
        self.username: str = player_json["username"]
        self.rank: int = player_json["statistics"]["global_rank"]

    async def update(self) -> None:
        from . import api_helper
        new_player = await api_helper.get_player_by_id(self.player_id)
        self.username = new_player.username
        self.rank = new_player.rank
