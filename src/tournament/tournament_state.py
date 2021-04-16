from typing import Dict, Optional

from person import Person
from tournament_map import TournamentMap


class TournamentState:
    instance = None  # type: TournamentState

    def __init__(self):
        # player_id : Person
        self.pros = {}  # type: Dict[str: Person]
        self.amateurs = {}  # type: Dict[str: Person]
        # beatmapset_id : Beatmapset
        self.tournamentmaps = {}  # type: Dict[str: TournamentMap]
        TournamentState.instance = self

    def register(self, person: Person) -> None:
        if person.player.rank < 50000:
            self.pros[person.player.player_id] = person
        else:
            self.amateurs[person.player.player_id] = person

    def unregister(self, player_id) -> None:
        if player_id in self.pros:
            self.pros.pop(player_id)
        elif player_id in self.amateurs:
            self.amateurs.pop(player_id)

    def get_person_from_player_id(self, player_id) -> Optional[Person]:
        if player_id in self.pros:
            return self.pros.get(player_id)
        elif player_id in self.amateurs:
            return self.amateurs.get(player_id)
        return None

    def update_ranks(self) -> None:
        people = []
        people.extend(self.pros.values())
        people.extend(self.amateurs.values())
        self.pros = {}
        self.amateurs = {}
        for person in people:
            person.player.update()
            self.register(person)

    def is_running(self) -> bool:
        return len(self.tournamentmaps) > 0
