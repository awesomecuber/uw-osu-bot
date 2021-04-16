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
        tournamentmaps = TournamentState.instance.tournamentmaps
        beatmapset_ids = [tournamentmap.beatmapset.beatmapset_id for tournamentmap in tournamentmaps]
        self.scores = {beatmapset_id: Score(0, 0) for beatmapset_id in beatmapset_ids}
