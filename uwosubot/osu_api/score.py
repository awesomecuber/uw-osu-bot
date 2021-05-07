from .. import state

class Score:
    def __init__(self, play_json):
        self.sr: float = 0
        self.acc: float = 0
        self.max_combo: int = 0
        self.max_possible_combo: int = 1
        self.misses: int = 0

        if play_json is not None:
            self.sr = play_json["beatmap"]["difficulty_rating"]
            self.acc = play_json["accuracy"]
            self.max_combo = play_json["max_combo"]
            self.misses = play_json["statistics"]["count_miss"]

            map_id = play_json["beatmap"]["id"]
            mapset_id = play_json["beatmapset"]["id"]
            tournamentmap = state.tournament.get_tournamentmap_by_beatmapset_id(mapset_id)

            self.max_possible_combo = tournamentmap.beatmapset.max_combos[map_id]

    # points take into account the difficulty of the map
    def calculate_points(self) -> float:
        return self.calculate_score() * (self.sr ** 2)

    # score doesn't take into account the difficulty of the map
    def calculate_score(self) -> float:
        acc_part = self.acc ** 10
        combo_part = (0.95 ** self.misses) * (self.max_combo / self.max_possible_combo)
        return acc_part * 500 + combo_part * 500 # total of 1000

    @staticmethod
    def zero() -> "Score":
        return Score(None)
