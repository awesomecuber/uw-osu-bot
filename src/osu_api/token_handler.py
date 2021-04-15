def set_token(token):
    with open("access_token", "w+") as f:
        f.write(token)


def get_token():
    with open("access_token") as f:
        token = f.read()
        return token
