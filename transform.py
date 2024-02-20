import math
import numpy as np
from constants import VIEWERPOS, HEIGHT, WIDTH

def rotation_matrix_around_point(angle_degrees, pivot):   
    # Convert angle from degrees to radians
    angle_radians = angle_degrees

    # Extract pivot coordinates
    px, py, pz = pivot

    # Translation matrix to move the pivot to the origin
    translate_to_origin = np.array([
        [1, 0, 0, -px],
        [0, 1, 0, -py],
        [0, 0, 1, -pz],
        [0, 0, 0, 1]
    ])

    # Rotation matrix around Y-axis
    rotation_matrix = np.array([
        [np.cos(angle_radians), 0, np.sin(angle_radians), 0],
        [0, 1, 0, 0],
        [-np.sin(angle_radians), 0, np.cos(angle_radians), 0],
        [0, 0, 0, 1]
    ])

    # Translation matrix to move back to the original position
    translate_back = np.array([
        [1, 0, 0, px],
        [0, 1, 0, py],
        [0, 0, 1, pz],
        [0, 0, 0, 1]
    ])

    # Combine the matrices
    rotation_matrix_around_point = np.dot(translate_back, np.dot(rotation_matrix, translate_to_origin))

    return rotation_matrix_around_point

def rotation_matrix(angle_x, angle_y, angle_z):
    # Rotation matrix for X-axis
    rotation_matrix_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])

    # Rotation matrix for Y-axis
    rotation_matrix_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])

    # Rotation matrix for Z-axis
    rotation_matrix_z = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0],
        [np.sin(angle_z), np.cos(angle_z), 0],
        [0, 0, 1]
    ])

    # Combine the rotation matrices by multiplying them
    combined_rotation_matrix = np.dot(rotation_matrix_x, np.dot(rotation_matrix_y, rotation_matrix_z))

    return combined_rotation_matrix

ROTATE_180 = rotation_matrix(0, 0, math.pi)
ROTATE = rotation_matrix(math.pi/5, math.pi/5, math.pi)
ROTATE_0 = rotation_matrix(0, 0, 0)


def rotate_point(point, rotation_matrix):
    # Convert the 3D coordinate to a column vector
    vector = np.array([point[0], point[1], point[2]])

    # Apply the rotation
    rotated_vector = np.dot(rotation_matrix, vector)

    # Convert the result back to a list and return
    rotated_point = rotated_vector.tolist()
    return rotated_point

def transform_point(point, rotation, scale, translation):
    point = rotate_point(point, rotation)
    
    point = [x * scale for x in point]
    point[0] = point[0] + translation[0]
    point[1] = point[1] + translation[1]
    point[2] = point[2] + translation[2]

    return point

def map_to_viewer(pos, viewer_pos=VIEWERPOS):
  x = pos[0] - viewer_pos[0]
  y = pos[1] - viewer_pos[1]
  z = pos[2] - viewer_pos[2]
  return x,y,z

def viewer_to_map(pos, viewer_pos=VIEWERPOS):
  x = pos[0] + viewer_pos[0]
  y = pos[1] + viewer_pos[1]
  z = pos[2] + viewer_pos[2]
    
  return x,y,z

def viewer_to_screen(pos):
  x = pos[0] + WIDTH/2
  y = HEIGHT/2 - pos[1]

  return x, y

def screen_to_viewer(pos, viewer_pos=VIEWERPOS):
  x = pos[0] - viewer_pos[0]
  y = viewer_pos[1] - pos[1]
  z = pos[2]

  return x,y,z