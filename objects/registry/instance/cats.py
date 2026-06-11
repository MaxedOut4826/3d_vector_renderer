from objects.registry.mesh.cat import cat
from random import randint

cat_1 = cat()

cat_2 = (
    cat()
    .scale(randint(0, 3), randint(0, 3), randint(0, 3))
    .rotate_roll(randint(0, 360))
    .rotate_yaw(randint(0, 360))
    .move(randint(0, 50), randint(0, 50), randint(0, 50))
)

cat_3 = (
    cat()
    .scale(randint(0, 3), randint(0, 3), randint(0, 3))
    .rotate_yaw(randint(0, 360))
    .rotate_roll(randint(0, 360))
    .move(randint(0, 50), randint(0, 50), randint(0, 50))
)
