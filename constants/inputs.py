from constants.my_types import Vector3

#TODO make movement speed dynamic based on zoom / object size

inputs: dict[bytes, Vector3] = {
    b"w": [0, 0, 1],
    b"s": [0, 0, -1],
    b"d": [1, 0, 0],
    b"a": [-1, 0, 0],
    b" ": [0, 1, 0],
    b"c": [0, -1, 0],
}
