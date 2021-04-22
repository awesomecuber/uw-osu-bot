import pickle

from . import state


def save_tournament_state() -> None:
    write_file = open("state", "wb")
    pickle.dump(state.tournament, write_file)
    write_file.close()


def load_tournament() -> None:
    with open("state", "rb") as f:
        state.tournament = pickle.load(f)
        print(state.tournament)
