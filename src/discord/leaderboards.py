from typing import Any, Dict, List, Tuple

from ..osu_api.score import Score
from ..tournament.person import Person
from ..tournament.tournament_state import TournamentState
from ..utils.calculate_points import calculate_points
from ..utils.sanitizer import sanitize


def get_total_leaderboards(people: List[Person]) -> str:
    tournamentmaps = TournamentState.instance.tournamentmaps
    beatmapset_ids = [tournamentmap.beatmapset.beatmapset_id for tournamentmap in tournamentmaps]

    people_norm_pointss = get_people_normalized_points(people, beatmapset_ids)
    sorted_people_norm_pointss = sort_dict(people_norm_pointss)

    message = ""
    for i in range(len(people)):
        person = sorted_people_norm_pointss[i][0]
        username = sanitize(person.player.username)
        norm_points = sorted_people_norm_pointss[i][1]
        message += f"{i+1}. {username} ({norm_points:.1f})\n"
    return message


def get_map_leaderboards(people: List[Person]) -> str:
    message = ""
    for tournamentmap in TournamentState.instance.tournamentmaps:
        beatmapset = tournamentmap.beatmapset
        beatmapset_id = beatmapset.beatmapset_id

        pointss = get_beatmapset_pointss(people, beatmapset_id)
        norm_pointss = get_beatmapset_normalized_points(people, beatmapset_id)
        sorted_norm_pointss = sort_dict(norm_pointss)

        message += f"__{sanitize(beatmapset.ascii_name)}__\n"

        for i in range(len(people)):
            person = people[i]
            username = sanitize(person.player.username)

            points = pointss[person]
            norm_points = sorted_norm_pointss[i]

            message += f"{i+1}. {username}: {points:.1f} (normalized: {norm_points:.1f})\n"
        message += "\n"
    return message


def get_beatmapset_scores(people: List[Person], beatmapset_id: int) -> Dict[Person, Score]:
    return {person: person.scores[beatmapset_id] for person in people}


def get_beatmapset_pointss(people: List[Person], beatmapset_id: int) -> Dict[Person, float]:
    scores = get_beatmapset_scores(people, beatmapset_id)
    return {person: calculate_points(scores[person]) for person in people}


def get_beatmapset_normalized_points(people: List[Person], beatmapset_id: int) -> Dict[Person, float]:
    pointss = get_beatmapset_pointss(people, beatmapset_id)

    max_points = max(pointss.values())
    # prevent divide by 0 errors
    if max_points == 0:
        max_points = 1

    # most possible points for this beatmapset
    normalization_constant = 1000.0 / len(TournamentState.instance.tournamentmaps)

    return {person: normalization_constant * pointss[person] / max_points for person in people}


def get_people_normalized_points(people: List[Person], beatmapset_ids: List[int]) -> Dict[Person, float]:
    output = {person: 0 for person in people}
    for beatmapset_id in beatmapset_ids:
        beatmapset_norm_pointss = get_beatmapset_normalized_points(people, beatmapset_id)
        for person in people:
            output[person] += beatmapset_norm_pointss[person]
    return output


# Sorts a dict from highest float value to lowest
def sort_dict(in_dict: Dict[Any, float]) -> List[Tuple[Any, float]]:
    in_list = list(in_dict)
    return sorted(in_list, key=lambda entry: entry[1], reverse=True)
