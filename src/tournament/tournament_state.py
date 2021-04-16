from typing import Dict, List, Optional

from .person import Person
from .tournament_map import TournamentMap
from ..utils.update_player import update_player


class TournamentState:
    instance = None  # type: TournamentState

    def __init__(self):
        self.pros = {}  # type: Dict[str: Person]
        self.amateurs = {}  # type: Dict[str: Person]
        self.tournamentmaps = {}  # type: Dict[str: TournamentMap]
        TournamentState.instance = self

    def register(self, person: Person) -> None:
        if person.player.rank < 50000:
            self.pros[person.player.player_id] = person
        else:
            self.amateurs[person.player.player_id] = person

    def unregister(self, player_id: int) -> None:
        if player_id in self.pros:
            self.pros.pop(player_id)
        elif player_id in self.amateurs:
            self.amateurs.pop(player_id)

    def get_people(self) -> List[Person]:
        output = []  # type: List[Person]
        output.extend(self.pros.values())
        output.extend(self.amateurs.values())
        return output

    def get_person_by_player_id(self, player_id: int) -> Optional[Person]:
        if player_id in self.pros:
            return self.pros[player_id]
        elif player_id in self.amateurs:
            return self.amateurs[player_id]
        return None

    def update_ranks(self) -> None:
        people = []  # type: List[Person]
        people.extend(self.pros.values())
        people.extend(self.amateurs.values())
        self.pros = {}
        self.amateurs = {}
        for person in people:
            update_player(person.player)
            self.register(person)

    def is_running(self) -> bool:
        return len(self.tournamentmaps) > 0


TournamentState()
