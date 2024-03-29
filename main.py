#!/usr/bin/env python3

import pygame
import random
import numpy as np
import math
from readObject import readObject
from transform import *
from configs import *

# OBJECT_FILE = "objects/teapot.obj"
# OBJECT_FILE = "objects/teddy.obj"
# OBJECT_FILE = "objects/pumpkin.obj"
# OBJECT_FILE = "objects/test.obj"
# OBJECT_FILE = "objects/square.obj"
OBJECT_FILE = "objects/cube.obj"

viewer_pos = VIEWERPOS


def projected_pos(point):
    x = point[0]
    y = point[1]
    z = point[2]

    if z == 0:
        return x, y

    dx = (K * x) / z
    dy = (K * y) / z

    return dx, dy


def get_xy(point):
    return (point[0], point[1])


vertices, faces = readObject(OBJECT_FILE)

feetVertices, bin = readObject("objects/feet.obj")


class Cube:

    def __init__(self, rotation, scale, translation):
        self.rotation = rotation
        self.scale = scale
        self.translation = translation


objects = [
    Cube([0, 0, 0], 150, [0, 150, 200]),
    # Cube([0, 0, 0], 150, [0, 450, 200]),
    # Cube([0, 0, 0], 150, [400, 150, 200]),
    # Cube([0, 0, 0], 150, [0, 150, 550]),
    # Cube([0, 0, 0], 150, [0, 450, 550]),
    # Cube([0, 0, 0], 150, [400, 150, 550]),
    # Cube([0, 0, 0], 150, [0, 750, 200]),
    # Cube([0, 0, 0], 150, [0, 1050, 200]),
    # Cube([0, 0, 0], 150, [0, 1350, 200]),
    # Cube([0, 0, 0], 150, [0, 1650, 200]),
]

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Macgyver")
    clock = pygame.time.Clock()  ## For syncing the FPS

    ## Game loop
    running = True
    isJumping = False
    jumpCount = 10
    pivot_rotation = 0
    while running:
        clock.tick(FPS)

        # calulate facing angle
        xratio = (pygame.mouse.get_pos()[0] / WIDTH) - 0.5
        xpivot_rotation = -xratio * 2 * math.pi

        yratio = (pygame.mouse.get_pos()[1] / WIDTH) - 0.5
        ypivot_rotation = -yratio * 2 * math.pi

        # EVENTS
        for (
            event
        ) in (
            pygame.event.get()
        ):  # gets all the events which have occured till now and keeps tab of them.
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    isJumping = True

        pressed = pygame.key.get_pressed()

        # Movement
        if pressed[pygame.K_w]:
            viewer_pos = move_at_angle(xpivot_rotation, SPEED, viewer_pos)
        elif pressed[pygame.K_s]:
            viewer_pos = move_at_angle(math.pi + xpivot_rotation, SPEED, viewer_pos)
        if pressed[pygame.K_a]:
            viewer_pos = move_at_angle(math.pi / 2 + xpivot_rotation, SPEED, viewer_pos)
        elif pressed[pygame.K_d]:
            viewer_pos = move_at_angle(xpivot_rotation - math.pi / 2, SPEED, viewer_pos)

        if isJumping:
            if jumpCount >= -10:
                neg = 1
                if jumpCount < 0:
                    neg = -1

                viewer_pos[1] += 5 * jumpCount**2 * 0.1 * neg
                jumpCount -= 1
            else:
                isJumping = False
                jumpCount = 10

        # RESET SCREEN
        screen.fill(BLACK)

        # Draw standing square
        corns = [
            transform_point(
                vertex, rotation_matrix(0, -xpivot_rotation, 0), 25, [0, 0, 0]
            )
            for vertex in feetVertices
        ]

        corns = [
            [point[0] + viewer_pos[0], point[1], point[2] + viewer_pos[2]]
            for point in corns
        ]

        corns = [map_to_viewer(point, viewer_pos) for point in corns]
        Rcorns = [
            rotate_point(point, rotation_matrix(ypivot_rotation, xpivot_rotation, 0))
            for point in corns
        ]

        corns = [projected_pos(point) for point in Rcorns]
        corns = [viewer_to_screen(point) for point in corns]

        skip = False
        for corner in Rcorns:
            if corner[2] < 0:
                skip = True

        if not skip:
            pygame.draw.polygon(screen, RED, corns)

        pygame.draw.line(screen, GREEN, [0, HEIGHT / 2], [WIDTH, HEIGHT / 2])

        # PROCESS WORLD
        for cube in objects:
            rotation = rotation_matrix(
                cube.rotation[0], cube.rotation[1], cube.rotation[2]
            )
            translation = cube.translation
            scale = cube.scale

            # draw edges
            for face in faces:
                world_plane = [
                    transform_point(vertices[vertex - 1], rotation, scale, translation)
                    for vertex in face
                ]

                relative_plane = [
                    map_to_viewer(point, viewer_pos) for point in world_plane
                ]
                relative_plane = [
                    rotate_point(
                        point, rotation_matrix(ypivot_rotation, xpivot_rotation, 0)
                    )
                    for point in relative_plane
                ]

                plane = [projected_pos(point) for point in relative_plane]
                plane = [viewer_to_screen(point) for point in plane]

                if relative_plane[0][2] > 0 and relative_plane[1][2] > 0:
                    pygame.draw.line(screen, WHITE, plane[0], plane[1])

                if relative_plane[1][2] > 0 and relative_plane[2][2] > 0:
                    pygame.draw.line(screen, WHITE, plane[1], plane[2])

                if relative_plane[2][2] > 0 and relative_plane[0][2] > 0:
                    pygame.draw.line(screen, WHITE, plane[2], plane[0])

            # Draw corners
            # for vertex in vertices:
            #     world_point = transform_point(vertex, rotation, scale, translation)

            #     relative_point = map_to_viewer(world_point, viewer_pos)

            #     relative_point = rotate_point(
            #         relative_point, rotation_matrix(ypivot_rotation, xpivot_rotation, 0)
            #     )

            #     projected_point = projected_pos(relative_point)
            #     screen_pos = viewer_to_screen(projected_point)

            #     if relative_point[2] <= 0:
            #         continue

            #     pygame.draw.circle(screen, RED, screen_pos, 4)

        pygame.display.flip()

    pygame.quit()
