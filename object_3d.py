import pygame
import numpy as np
from typing import Tuple
from transforms import *
class Object_3D:
    def __init__(self, file_path: str, initial_pos: Tuple[int] = (0, 0, 0)):

        self.initial_pos = initial_pos
        file = open(file_path)
        self.vertices = []
        self.faces = []
        for line in file:
            if line.startswith("v"):
                try:
                    _, x,y,z = line.split()
                except:
                    pass

                # A parte comentada faz com que o centro do objeto não esteja na origem de seu espaço!

                x = float(x) #+ initial_pos[0]
                y = float(y) #+ initial_pos[1]  
                z = float(z) #+ initial_pos[2]   

                self.vertices.append([x,y,z,1])

            if line.startswith("f"):
                _, *indices = line.split()
                self.faces.append(indices)
        
        self._angle_x = 0
        self._angle_y = 0
        self._angle_z = 0

    def draw(self, screen: pygame.Surface, width: int, height: int, view_matrix: np.ndarray):
        relative_vertices = self.vertices @ view_matrix.transpose()
        for vertex in relative_vertices:
            if vertex[0,3] < 0:
                pygame.draw.circle(screen, "black", (vertex[0,0] / vertex[0,3] + width//2, vertex[0,1]/vertex[0,3] + height//2), 2)

    @property
    def angle_x(self):
        return self._angle_x
    
    @angle_x.setter
    def angle_x(self, new_angle_x):
        self.vertices = self.vertices @ rotation_x(new_angle_x - self._angle_x)
        self._angle_x = new_angle_x

    @property
    def angle_y(self):
        return self._angle_y
    
    @angle_y.setter
    def angle_y(self, new_angle_y):
        self.vertices = self.vertices @ rotation_y(new_angle_y - self._angle_y)
        self._angle_y = new_angle_y

    @property
    def angle_z(self):
        return self._angle_z
    
    @angle_z.setter
    def angle_z(self, new_angle_z):
        self.vertices = self.vertices @ rotation_z(new_angle_z - self._angle_z)
        self._angle_z = new_angle_z