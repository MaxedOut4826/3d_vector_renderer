from constants.my_types import Vector3


def convert_obj(path: str) -> None:
    vertices: list[Vector3] = []
    indices: list[Vector3] = []

    with open(f"objects/raw/{path}.obj", "r") as object:
        object = object.read()
    
        lines: list[str] = object.split("\n")

        for line in lines:
            parts = line.strip().split(" ")

            if parts[0] == "v":
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                continue

            if parts[0] == "f":
                indices.append([int(p.split("/")[0]) - 1 for p in parts[1:]])
                continue

            continue

    with open(f"objects/output/{path}.py", "x") as f:
        f.write(f"vertices = {vertices}\nindices = {indices}")