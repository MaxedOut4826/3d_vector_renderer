import math

radius = 0.25
lat_segments = 20
lon_segments = 20

vertices = []

# Generate vertices
for i in range(lat_segments + 1):
    theta = math.pi * i / lat_segments  # 0 → π
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)

    for j in range(lon_segments + 1):
        phi = 2 * math.pi * j / lon_segments  # 0 → 2π
        sin_p = math.sin(phi)
        cos_p = math.cos(phi)

        x = radius * sin_t * cos_p
        y = radius * cos_t
        z = radius * sin_t * sin_p

        vertices.append([x, y, z])

# Helper to convert grid coords to index
def idx(i, j):
    return i * (lon_segments + 1) + j

indices = []

# Quad faces
for i in range(lat_segments):
    for j in range(lon_segments):
        a = idx(i, j)
        b = idx(i, j + 1)
        c = idx(i + 1, j + 1)
        d = idx(i + 1, j)

        indices.append([a, b, c, d])

# Edge lines (wireframe style)
edges = []

# horizontal
for i in range(lat_segments + 1):
    for j in range(lon_segments):
        edges.append([idx(i, j), idx(i, j + 1)])

# vertical
for i in range(lat_segments):
    for j in range(lon_segments + 1):
        edges.append([idx(i, j), idx(i + 1, j)])