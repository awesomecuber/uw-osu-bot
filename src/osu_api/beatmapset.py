class Beatmapset:
    def __init__(self, beatmapset_json):
        self.beatmapset_id = beatmapset_json["id"]  # type: int
        self.ascii_name = beatmapset_json["title"]  # type: str
        self.unicode_name = beatmapset_json["title_unicode"]  # type: str
        self.difficulty_count = len(beatmapset_json["beatmaps"])  # type: int
        beatmap_jsons = beatmapset_json["beatmaps"]
        self.max_sr = max(beatmap_json["difficulty_rating"] for beatmap_json in beatmap_jsons)  # type: float
