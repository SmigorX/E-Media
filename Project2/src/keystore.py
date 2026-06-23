import json

def save_keys(path: str, public_key: tuple, private_key: tuple) -> None:
    e, n = public_key
    d, _ = private_key
    with open(path, "w") as f:
        json.dump({"e": str(e), "d": str(d), "n": str(n)}, f)

def load_keys(path: str) -> tuple:
    with open(path) as f:
        data = json.load(f)
    e, d, n = int(data["e"]), int(data["d"]), int(data["n"])
    return (e, n), (d, n)
