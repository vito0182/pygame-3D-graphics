import pygame
from pygame.locals import *
import numpy as np
from math import tan, radians, degrees, cos, sin, sqrt
from transforms import *
import time
from input_handler import mouse_handler, keyboard_handler
from camera import Camera
from object_3d import Object_3D

width = 800
height = 600

obj = Object_3D("cessna.obj")

fov = radians(90)

scaling_factor = 1/(tan(fov/2))

pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

t = 0

fov = 100

zfar = 1000
znear = 0.01

pygame.mouse.set_visible(0)

camera = Camera()

while True:

    t += 10

    rot_world = rotation_z(0) @ rotation_y(0) @ rotation_x(0)
    world_matrix = translation(0,0,0) @ rot_world

    camera.update()

    final_matrix = perspective(fov,height/width,znear,zfar) @ viewport(width,height) @ camera.matrix @ world_matrix

    for event in pygame.event.get():
        if event.type in [pygame.QUIT]:
            quit()
        if event.type == pygame.MOUSEWHEEL:
            camera.pos_z += 10 * event.y

    # Getting mouse position and rotation angles
    camera.angle_x, camera.angle_y = mouse_handler(width, height, camera.angle_x, camera.angle_y)

    # Handling keyboard inputs
    keyboard_handler(camera)
    
    screen.fill("#ff5555")

    cube_p = obj.vertices @ final_matrix.transpose()

    for vertex in cube_p:
        if vertex[0,3] < 0:
            pygame.draw.circle(screen, "black", (vertex[0,0] / vertex[0,3] + width//2, vertex[0,1]/vertex[0,3] + height//2), 2)
        
    pygame.draw.circle(screen, "white", (width//2, height//2), 5, 2)

    pygame.display.update()
    clock.tick()