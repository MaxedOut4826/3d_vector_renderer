from math import cos, sin
from render_pipeline import Vector3


class Vertex:
    @staticmethod
    def get_rotated(vertex: Vector3, rotation_vector: Vector3) -> Vector3:
        yaw, pitch, roll = rotation_vector
        rotated_vertex = vertex

        rotated_vertex = Vertex.get_rotated_yaw(rotated_vertex, yaw)
        rotated_vertex = Vertex.get_rotated_pitch(rotated_vertex, pitch)
        rotated_vertex = Vertex.get_rotated_roll(rotated_vertex, roll)

        return rotated_vertex

    @staticmethod
    def get_rotated_yaw(vertex: Vector3, yaw: float) -> Vector3:
        cos_angle = cos(yaw)
        sin_angle = sin(yaw)
        x, y, z = vertex

        return [
            x * cos_angle - z * sin_angle,
            y,
            x * sin_angle + z * cos_angle,
        ]

    @staticmethod
    def get_rotated_pitch(vertex: Vector3, pitch: float) -> Vector3:
        cos_angle = cos(pitch)
        sin_angle = sin(pitch)
        x, y, z = vertex

        return [
            x * cos_angle - y * sin_angle,
            x * sin_angle + y * cos_angle,
            z,
        ]

    @staticmethod
    def get_rotated_roll(vertex: Vector3, roll: float) -> Vector3:
        cos_angle = cos(roll)
        sin_angle = sin(roll)
        x, y, z = vertex

        return [
            x,
            y * cos_angle - z * sin_angle,
            y * sin_angle + z * cos_angle,
        ]

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
