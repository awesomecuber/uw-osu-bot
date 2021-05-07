class Beatmapset:
    def __init__(self, beatmapset_json):
        self.beatmapset_id: int = beatmapset_json["id"]
        self.ascii_name: str = beatmapset_json["title"]
        self.unicode_name: str = beatmapset_json["title_unicode"]
        self.difficulty_count: int = len(beatmapset_json["beatmaps"])
        beatmap_jsons = beatmapset_json["beatmaps"]
        self.max_sr: float = max(beatmap_json["difficulty_rating"] for beatmap_json in beatmap_jsons)
        self.max_combos: dict[int, int] = {
            beatmap_json["id"]: beatmap_json["max_combo"]
            for beatmap_json in beatmap_jsons
        }
