# from assets.cube import cube
from random import randint
from math import pi
from render_pipeline.render_handler import Renderer, MAX_FPS
from objects.objects_manager import Prefab, ObjectInstance
from intervals.intervals_manager import run_interval

# * EXAMPLE

# ? Cube Definition
cube = Prefab(
    {
        "vertices": [
            [0.25, 0.25, 0.25],
            [-0.25, 0.25, 0.25],
            [-0.25, -0.25, 0.25],
            [0.25, -0.25, 0.25],
            [0.25, 0.25, -0.25],
            [-0.25, 0.25, -0.25],
            [-0.25, -0.25, -0.25],
            [0.25, -0.25, -0.25],
        ],
        "indices": [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7],
        ],
    }
)

# ? Define Animation DefiFnitions


def animate(object: ObjectInstance) -> None:
    delta_time = Renderer.delta_time

    object.rotate_roll(pi * 0.08 * delta_time).rotate_yaw(pi * 0.2 * delta_time)


# ? Cube Instances
cube_1 = cube()

cube_2 = (
    cube()
    .scale([randint(0, 10), randint(0, 10), randint(0, 10)])
    .rotate_roll(randint(0, 360))
    .rotate_yaw(randint(0, 360))
    .move([randint(0, 30), randint(0, 30), randint(0, 30)])
)

cube_3 = (
    cube()
    .scale([randint(0, 10), randint(0, 10), randint(0, 10)])
    .rotate_roll(randint(0, 360))
    .rotate_yaw(randint(0, 360))
    .move([randint(0, 30), randint(0, 30), randint(0, 30)])
)

cube_4 = (
    cube()
    .scale([randint(0, 10), randint(0, 10), randint(0, 10)])
    .rotate_roll(randint(0, 360))
    .rotate_yaw(randint(0, 360))
    .move([randint(0, 30), randint(0, 30), randint(0, 30)])
)

cube_5 = (
    cube()
    .scale([randint(0, 10), randint(0, 10), randint(0, 10)])
    .rotate_roll(randint(0, 360))
    .rotate_yaw(randint(0, 360))
    .move([randint(0, 30), randint(0, 30), randint(0, 30)])
)

# ? Call Cube animates
run_interval(lambda: [animate(obj) for obj in Prefab.instances], 1 / MAX_FPS)
