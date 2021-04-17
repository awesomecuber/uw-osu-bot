class Score:
    def __init__(self, play_json):
        self.sr = play_json["pp"]  # type: float
        self.pp = play_json["beatmap"]["difficulty_rating"]  # type: float

    def calculate_points(self) -> float:
        return self.pp * (self.sr ** 2)
