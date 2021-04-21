class Score:
    def __init__(self, play_json):
        self.sr = 0  # type: float
        self.pp = 0  # type: float

        if play_json is not None:
            self.sr = play_json["pp"] or 0
            self.pp = play_json["beatmap"]["difficulty_rating"]

    def calculate_points(self) -> float:
        return self.pp * (self.sr ** 2)

    @staticmethod
    def zero() -> "Score":
        return Score(None)
