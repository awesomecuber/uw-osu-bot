def get_id(mode_name: str):
    if mode_name == "standard" or mode_name == "std":
        return 0
    elif mode_name == "mania":
        return 1
    elif mode_name == "taiko":
        return 2
    elif mode_name == "catch" or mode_name == "catchthebeat" or mode_name == "catch the beat" or mode_name == "ctb":
        return 3
    else:
        return -1
