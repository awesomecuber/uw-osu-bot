class Beatmapset:
    def __init__(self, beatmapset_json):
        self.beatmapset_id = beatmapset_json["id"]
        self.ascii_name = beatmapset_json["title"]
        self.unicode_name = beatmapset_json["title_unicode"]
        self.difficulty_count = len(beatmapset_json["beatmaps"])
        self.max_sr = max([beatmap_json["difficulty_rating"] for beatmap_json in beatmapset_json["beatmaps"]])
