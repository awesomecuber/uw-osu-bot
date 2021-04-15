class State:
    def __init__(self):
        self.pros = {}
        self.amateurs = {}
        self.beatmaps = {}


state = State()


def get_state() -> State:
    return state


def is_running() -> bool:
    return len(state.beatmaps) > 0
