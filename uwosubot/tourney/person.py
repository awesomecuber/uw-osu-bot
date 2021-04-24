from ..osu_api.player import Player
from ..osu_api.score import Score


class Person:
    def __init__(self, discord_id: int, player: Player):
        self.discord_id: int = discord_id
        self.player: Player = player
        self.scores: dict[int, Score] = {}
        self.reset_scores()

    def reset_scores(self) -> None:
        from ..state import tournament # TODO: investigate why this has to be a thing
        tournamentmaps = tournament.get_tournamentmaps()
        beatmapset_ids = [tournamentmap.beatmapset.beatmapset_id for tournamentmap in tournamentmaps]
        self.scores = {beatmapset_id: Score.zero() for beatmapset_id in beatmapset_ids}
