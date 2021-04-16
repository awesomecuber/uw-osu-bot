from ..osu_api.score import Score


def calculate_points(score: Score) -> float:
    return score.pp * (score.sr ** 2)
