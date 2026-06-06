from objects.registry.mesh.human import human
from random import randint

human_1 = human()

human_2 = (
    human()
    .scale([randint(0, 3), randint(0, 3), randint(0, 3)])
    .rotate_roll(randint(0, 360))
    .rotate_yaw(randint(0, 360))
    .move([randint(0, 50), randint(0, 50), randint(0, 50)])
)

human_3 = (
    human()
    .scale([randint(0, 3), randint(0, 3), randint(0, 3)])
    .rotate_roll(randint(0, 360))
    .rotate_yaw(randint(0, 360))
    .move([randint(0, 50), randint(0, 50), randint(0, 50)])
)
