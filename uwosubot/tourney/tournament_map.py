from ..osu_api.beatmapset import Beatmapset


class TournamentMap:
    def __init__(self, beatmapset: Beatmapset, mods: list[str]):
        self.beatmapset: Beatmapset = beatmapset
        self.mods: list[str] = mods
