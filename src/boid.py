from pyglet.gl import *
import random
import math

class Flock:
    def __init__(self, size):
        self.boids = [Boid(random.randint(0, 500), random.randint(0, 500)) for _ in range(size)]

    def draw(self):
        for boid in self.boids:
            boid.vertexList.draw(GL_TRIANGLES)

    def update(self):
        for boid in self.boids:
            boid.update()

class Boid:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.theta = 0
        self.vel = [5 * random.random(), 5 * random.random()]
        self.acc = [0, 0]

        # TODO: FIX ME
        self.vertex = [self.pos[0],self.pos[1]+10,
            self.pos[0]-5,self.pos[1]-10, self.pos[0]+5,self.pos[1]-10]

        self.vertexList = pyglet.graphics.vertex_list(3, ('v2f', list(map(int, self.vertex))))

    def update(self):
        # This runs at 30 Hz, so the velocities and accelerations should be scaled...
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]

        if self.pos[0] < 0:
            self.pos[0] = 500
        elif self.pos[0] > 500:
            self.pos[0] = 0

        if self.pos[1] < 0:
            self.pos[1] = 500
        elif self.pos[1] > 500:
            self.pos[1] = 0

        # CCW from x
        self.theta = math.atan2(self.vel[1], self.vel[0])

        x, y = self.pos
        cos = math.cos(self.theta)
        sin = math.sin(self.theta)
        self.vertex = [
            x + 10 * cos, y + 10 * sin,
            x - 10 * cos - 5 * sin, y - 10 * sin + 5 * cos,
            x - 10 * cos + 5 * sin, y - 10 * sin - 5 * cos
            ]
        self.vertexList = pyglet.graphics.vertex_list(3, ('v2f', list(map(int, self.vertex))))
