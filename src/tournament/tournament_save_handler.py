import pickle

from tournament_state import TournamentState


def save_tournament_state():
    write_file = open("state", "wb")
    pickle.dump(TournamentState.instance, write_file)
    write_file.close()


def load_tournament():
    with open("state", "rb") as f:
        TournamentState.instance = pickle.load(f)
