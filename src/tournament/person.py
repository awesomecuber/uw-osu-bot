from ..osu_api.player import Player
from ..osu_api.score import Score
from ..tournament.tournament_state import TournamentState


class Person:
    def __init__(self, discord_id, player: Player):
        self.discord_id = discord_id
        self.player = player
        self.scores = {}
        self.reset_scores()

    def reset_scores(self) -> None:
        tournament_beatmaps = TournamentState.instance.beatmaps
        self.scores = {beatmapset.beatmapset_id: Score(0, 0) for beatmapset in tournament_beatmaps}
