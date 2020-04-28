from pyglet.gl import *
from force import *
import random
import math

class Flock:
    def __init__(self, size, bounds):
        self.boids = [Boid(random.randint(0, bounds), random.randint(0, bounds), bounds) for _ in range(size)]

    def draw(self):
        for boid in self.boids:
            boid.vertexList.draw(GL_TRIANGLES)

    def update(self, force):
        for boid in self.boids:
            boid.update(force)

    def addBoid(self, x, y, bounds):
        self.boids.append(Boid(x, y, bounds))

class Boid:
    def __init__(self, x, y, bounds):
        self.pos = [x, y]
        self.theta = 0
        self.vel = [5 * random.random(), 5 * random.random()]
        self.acc = [0, 0]
        self.bounds = bounds

        # TODO: FIX ME
        self.vertex = [self.pos[0],self.pos[1]+10,
            self.pos[0]-5,self.pos[1]-10, self.pos[0]+5,self.pos[1]-10]

        self.vertexList = pyglet.graphics.vertex_list(3, ('v2f', list(map(int, self.vertex))))

    def update(self, force):
        # Update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Update velocity
        delX = force.x - self.pos[0]
        delY = force.y - self.pos[1]
        mul = force.magnitude / math.pow(delX * delX + delY * delY, 3/2)
        self.vel[0] += mul * delX
        self.vel[1] += mul * delY

        # Limit position and velocity
        if self.pos[0] < 0:
            self.pos[0] = self.bounds
        elif self.pos[0] > self.bounds:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = self.bounds
        elif self.pos[1] > self.bounds:
            self.pos[1] = 0

        if self.vel[0] > 5:
            self.vel[0] = 5
        elif self.vel[0] < -5:
            self.vel[0] = -5
        if self.vel[1] > 5:
            self.vel[1] = 5
        elif self.vel[1] < -5:
            self.vel[1] = -5

        # Calculate vertex positions
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
