from constants.my_types import Vector3


def convert_obj(path: str, scale: Vector3 = [1, 1, 1]) -> None:
    vertices: list[Vector3] = []
    indices: list[Vector3] = []

    with open(f"assets/raw/{path}.obj", "r") as object:
        object = object.read()

        lines: list[str] = object.split("\n")

        for line in lines:
            parts = line.strip().split(" ")

            if parts[0] == "v":
                vertices.append(
                    [
                        float(parts[1]) / scale[0],
                        float(parts[2]) / scale[1],
                        float(parts[3]) / scale[2],
                    ]
                )
                continue

            if parts[0] == "f":
                indices.append([int(p.split("/")[0]) - 1 for p in parts[1:]])
                continue

            continue

    with open(f"objects/registry/mesh/{path}.py", "x") as f:
        f.write(
            "from render_pipeline.objects import Object\n\n"
            f"{path} = Object(\n{{\n"
            f"'vertices': {vertices},\n"
            f"'indices': {indices}\n}}\n)"
        )


"""
TODO: Consider adding a separate function that creates the file 
TODO: main function just returns the vertices and indices
? this may be called when an object is instanciated
"""
