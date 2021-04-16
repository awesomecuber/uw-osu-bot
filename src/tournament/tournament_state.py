from person import Person


class TournamentState:
    instance = None

    def __init__(self):
        # player_id : Person
        self.pros = {}
        self.amateurs = {}
        # beatmapset_id : Beatmapset
        self.beatmaps = {}
        TournamentState.instance = self

    def register(self, person: Person) -> None:
        if person.player.rank < 50000:
            self.pros[person.player.player_id] = person
        else:
            self.amateurs[person.player.player_id] = person

    def update_ranks(self) -> None:
        people = []
        people.extend(self.pros.values())
        people.extend(self.amateurs.values())
        self.pros = {}
        self.amateurs = {}
        for person in people:
            self.register(person)

    def is_running(self) -> bool:
        return len(self.beatmaps) > 0
