from pyglet.gl import *
from force import *
import random
import math

class Flock:
    def __init__(self, size, bounds):
        #self.boids = [Boid(random.randint(0, bounds), random.randint(0, bounds), bounds) for _ in range(size)]
        self.boids = [Boid(random.randint(225, 275), random.randint(225, 275), bounds) for _ in range(size)]

    def draw(self):
        for boid in self.boids:
            boid.vertexList.draw(GL_TRIANGLES)

    def update(self, force):
        for boid in self.boids:
            boid.update(force, self)

    def addBoid(self, x, y, bounds):
        self.boids.append(Boid(x, y, bounds))

class Boid:
    vision = 100
    repulse = -10
    attract = 50

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

    def update(self, force, flock):
        # Update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Update velocity
        delX = force.x - self.pos[0]
        delY = force.y - self.pos[1]
        mul = force.magnitude / (math.pow(delX * delX + delY * delY, 1.5) + 0.0001)
        self.vel[0] += mul * delX
        self.vel[1] += mul * delY

        # Avoid birds and go to center
        dV = [0, 0]
        sum = [0, 0]
        dCenter = [0, 0]
        count = 0
        for boid in flock.boids:
            # Determine r
            dX = boid.pos[0] - self.pos[0]
            dY = boid.pos[1] - self.pos[1]
            r = math.pow(dX * dX + dY * dY, 0.5) + 0.0001
            # If in vision
            if r < Boid.vision:
                # Repulsion
                dV[0] += Boid.repulse / math.pow(r, 3) * dX
                dV[1] += Boid.repulse / math.pow(r, 3) * dY

                # Attraction to center
                sum[0] += boid.pos[0]
                sum[1] += boid.pos[1]
                count += 1
        # Attraction to center
        if count > 0:
            dCenter[0] = sum[0] / count - self.pos[0]
            dCenter[1] = sum[1] / count - self.pos[1]
            mCenter = Boid.attract / (math.pow(dCenter[0] * dCenter[0] + dCenter[1] * dCenter[1], 1.5) + 0.0001)
            dV[0] += mCenter * dCenter[0]
            dV[1] += mCenter * dCenter[1]

        # Avoid wall    # TODO: MAYBE SHOULD MAKE BOID TURN PARALLEL TO WALL
        f = 0.5
        if self.bounds - self.pos[0] < 25:
            dV[0] -= f
            dV[1] -= f  # Try avoiding ccw?
        elif self.pos[0] < 25:
            dV[0] += f
            dV[1] += f
        if self.bounds - self.pos[1] < 25:
            dV[1] -= f
            dV[0] += f
        elif self.pos[1] < 25:
            dV[1] += f
            dV[0] -= f

        # Update velocity for avoidance and center attraction
        self.vel[0] += dV[0]
        self.vel[1] += dV[1]

        # Limit position and velocity
        #if self.pos[0] < 0:
        #    self.pos[0] = self.bounds
        #elif self.pos[0] > self.bounds:
        #    self.pos[0] = 0
        #if self.pos[1] < 0:
        #    self.pos[1] = self.bounds
        #elif self.pos[1] > self.bounds:
        #    self.pos[1] = 0

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
