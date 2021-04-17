class Score:
    def __init__(self, play_json):
        self.sr = play_json["pp"]  # type: float
        self.pp = play_json["beatmap"]["difficulty_rating"]  # type: float

    def calculate_points(self) -> float:
        return self.pp * (self.sr ** 2)

    @staticmethod
    def zero() -> "Score":
        zero_dict = {
            "pp": 0,
            "beatmap": {
                "difficulty_rating": 0
            }
        }
        return Score(zero_dict)
