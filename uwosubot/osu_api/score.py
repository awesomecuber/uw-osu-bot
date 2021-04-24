class Score:
    def __init__(self, play_json):
        self.sr: float = 0
        self.pp: float = 0

        if play_json is not None:
            self.sr = play_json["beatmap"]["difficulty_rating"]
            self.pp = play_json["pp"] or 0

    def calculate_points(self) -> float:
        return self.pp * (self.sr ** 2)

    @staticmethod
    def zero() -> "Score":
        return Score(None)
