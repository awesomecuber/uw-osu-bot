from typing import Dict

from ..osu_api.player import Player
from ..osu_api.score import Score


class Person:
    def __init__(self, discord_id: int, player: Player):
        self.discord_id = discord_id  # type: int
        self.player = player  # type: Player
        self.scores = {}  # type: Dict[int, Score]
        self.reset_scores()

    def reset_scores(self) -> None:
        from ..tournament.tournament_state import TournamentState
        tournamentmaps = TournamentState.instance.tournamentmaps.values()
        beatmapset_ids = [tournamentmap.beatmapset.beatmapset_id for tournamentmap in tournamentmaps]
        self.scores = {beatmapset_id: Score.zero() for beatmapset_id in beatmapset_ids}
