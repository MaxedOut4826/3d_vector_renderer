from math import cos, sin
from render_pipeline import Vector3


class Vertex:
    @staticmethod
    def get_rotated(vertex: Vector3, rotation_vector: Vector3) -> Vector3:
        rotation_y, rotation_x, rotation_z = rotation_vector
        x, y, z = vertex

        cos_x, sin_x = cos(rotation_x), sin(rotation_x)
        cos_y, sin_y = cos(rotation_y), sin(rotation_y)
        cos_z, sin_z = cos(rotation_z), sin(rotation_z)

        return [
            (cos_x * cos_z + sin_x * sin_y * sin_z) * x
            + (-cos_x * sin_z + sin_x * sin_y * cos_z) * y
            + (sin_x * cos_y) * z,
            (cos_y * sin_z) * x + (cos_y * cos_z) * y + (-sin_y) * z,
            (-sin_x * cos_z + cos_x * sin_y * sin_z) * x
            + (sin_x * sin_z + cos_x * sin_y * cos_z) * y
            + (cos_x * cos_y) * z,
        ]

    # @staticmethod
    # def get_rotated_yaw(vertex: Vector3, yaw: float) -> Vector3:
    #     cos_angle = cos(yaw)
    #     sin_angle = sin(yaw)
    #     x, y, z = vertex

    #     return [
    #         x * cos_angle - z * sin_angle,
    #         y,
    #         x * sin_angle + z * cos_angle,
    #     ]

    # @staticmethod
    # def get_rotated_pitch(vertex: Vector3, pitch: float) -> Vector3:
    #     cos_angle = cos(pitch)
    #     sin_angle = sin(pitch)
    #     x, y, z = vertex

    #     return [
    #         x * cos_angle + z * sin_angle,
    #         y,
    #         -x * sin_angle + z * cos_angle,
    #     ]

    # @staticmethod
    # def get_rotated_roll(vertex: Vector3, roll: float) -> Vector3:
    #     cos_angle = cos(roll)
    #     sin_angle = sin(roll)
    #     x, y, z = vertex

    #     return [
    #         x,
    #         y * cos_angle - z * sin_angle,
    #         y * sin_angle + z * cos_angle,
    #     ]

    @staticmethod
    def get_translated(vertex: Vector3, offset: Vector3) -> Vector3:
        offset_x, offset_y, offset_z = offset
        x, y, z = vertex

        return [x + offset_x, y + offset_y, z + offset_z]

    @staticmethod
    def get_scaled(vertex: Vector3, scalar: Vector3) -> Vector3:
        scale_x, scale_y, scale_z = scalar
        x, y, z = vertex

        return [x * scale_x, y * scale_y, z * scale_z]
