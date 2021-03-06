from ..osu_api import api_request
from ..osu_api.beatmapset import Beatmapset
from ..utils import modes


def _generate_sql_dates(months: list[str]) -> list[str]:
    sql_dates = []
    for month in months:
        date_month, date_year = month.split("/")
        if len(date_month) == 1:
            date_month = "0" + date_month
        sql_dates.append(f"20{date_year}-{date_month}")
    return sql_dates


async def get_good_beatmapsets(mode: str, months: list[str]) -> list[Beatmapset]:
    sql_dates = _generate_sql_dates(months)
    mode_id = modes.get_id(mode)
    beatmapsets = await api_request.get_ranked_beatmapsets(mode_id, sql_dates)

    results = []
    for beatmapset in beatmapsets:
        if beatmapset.difficulty_count >= 5 and beatmapset.max_sr >= 5:
            results.append(beatmapset)
    return results
