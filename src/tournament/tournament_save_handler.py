import pickle

import tournament_state


def save_tournament_state():
    write_file = open("state", "wb")
    pickle.dump(tournament_state.get_state(), write_file)
    write_file.close()
