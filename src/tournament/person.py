from ..tournament import tournament_state
from ..osu_api.score import Score


class Person:
    def __init__(self, discord_id, player):
        self.discord_id = discord_id
        self.player = player
        self.scores = {}
        self.reset_scores()

    def reset_scores(self) -> None:
        tournament_beatmaps = tournament_state.get_state().beatmaps
        self.scores = {beatmapset: Score(0, 0) for beatmapset in tournament_beatmaps}
