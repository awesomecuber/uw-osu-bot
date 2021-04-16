from typing import List

from ..osu_api.beatmapset import Beatmapset


class TournamentMap:
    def __init__(self, beatmapset: Beatmapset, mods: List[str]):
        self.beatmapset = beatmapset  # type: Beatmapset
        self.mods = mods  # type: List[str]
