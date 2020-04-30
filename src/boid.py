from pyglet.gl import *
import random
import math

class Flock:
    def __init__(self, size, boundX, boundY):
        self.boids = [Boid(random.randint(0, boundX), random.randint(0, boundY), boundX, boundY) for _ in range(size)]
        #self.boids = [Boid(random.randint(bounds / 2 - 25, bounds / 2 + 25),
        #    random.randint(bounds / 2 - 25, bounds / 2 + 25), bounds) for _ in range(size)]

    def draw(self):
        for boid in self.boids:
            glColor3f(boid.color[0], boid.color[1], boid.color[2])
            boid.vertexList.draw(GL_TRIANGLES)

    def update(self):
        for boid in self.boids:
            boid.update(self)

    def addBoid(self, x, y, bounds):
        self.boids.append(Boid(x, y, bounds))

class Boid:
    vision = 75
    avoidVision = 20
    home = 50
    attract = 2.5
    align = 0.5
    avoid = 5
    maxVel = 10
    maxAcc = 0.25

    def __init__(self, x, y, boundX, boundY):
        self.pos = [x, y]
        self.theta = 0
        self.vel = [Boid.maxVel * 2 * (random.random() - 0.5), Boid.maxVel * 2 * (random.random() - 0.5)]
        self.acc = [0, 0]
        self.targetV = [self.vel[0], self.vel[1]]
        self.bounds = [boundX, boundY]
        self.color = [random.random(), random.random(), random.random()]

        # TODO: FIX ME (Initialize based on theta)
        self.vertex = [self.pos[0],self.pos[1]+10,
            self.pos[0]-5,self.pos[1]-10, self.pos[0]+5,self.pos[1]-10]

        self.vertexList = pyglet.graphics.vertex_list(3, ('v2f', list(map(int, self.vertex))))

    def update(self, flock):
        # Update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Update velocity
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]

        # Reset target velocity
        self.targetV[0] = 0
        self.targetV[1] = 0

        # Avoid boids and go to center
        sum = [0, 0]
        count = 0
        dCenter = [0, 0]
        sumSep = [0, 0]
        countSep = 0
        sumVel = [0, 0]
        avgVel = [0, 0]
        for boid in flock.boids:
            # Skip itself
            if boid == self:
                continue

            # Determine r
            dX = boid.pos[0] - self.pos[0]
            dY = boid.pos[1] - self.pos[1]
            r_sq = dX * dX + dY * dY + 0.0001        # Avoid taking sqrt...
            # If in vision
            if r_sq < Boid.vision * Boid.vision:
                # Position sum
                count += 1
                sum[0] += boid.pos[0]
                sum[1] += boid.pos[1]

                # Velocity sum
                sumVel[0] += boid.vel[0]
                sumVel[1] += boid.vel[1]

                if r_sq < Boid.avoidVision * Boid.avoidVision:
                    # Avoid sum
                    countSep += 1
                    sumSep[0] -= dX / r_sq     # r^2 force...
                    sumSep[1] -= dY / r_sq

        # Attraction to center and align vectors
        if count > 0:
            # Attraction
            dCenter[0] = sum[0] / count - self.pos[0]
            dCenter[1] = sum[1] / count - self.pos[1]
            rCenter = math.pow(dCenter[0] * dCenter[0] + dCenter[1] * dCenter[1], 0.5) + 0.0001
            self.targetV[0] += dCenter[0] / rCenter * Boid.attract
            self.targetV[1] += dCenter[1] / rCenter * Boid.attract

            # Alignment
            avgVel[0] = sumVel[0] / count
            avgVel[1] = sumVel[1] / count
            speed = math.pow(avgVel[0] * avgVel[0] + avgVel[1] * avgVel[1], 0.5) + 0.0001
            velP = abs(math.atan2(self.vel[1], self.vel[0]) - math.atan2(avgVel[1], avgVel[0]))
            self.targetV[0] += sumVel[0] / speed * Boid.align * velP
            self.targetV[1] += sumVel[1] / speed * Boid.align * velP

        # Avoid boids
        if countSep > 0:
            rCenter = math.pow(sumSep[0] * sumSep[0] + sumSep[1] * sumSep[1], 0.5) + 0.0001
            self.targetV[0] += sumSep[0] / rCenter * Boid.avoid
            self.targetV[1] += sumSep[1] / rCenter * Boid.avoid

        # Attraction to center of screen
        homeX = self.bounds[0] / 2 - self.pos[0]
        homeY = self.bounds[1] / 2 - self.pos[1]
        homeR = homeX * homeX + homeY * homeY
        self.targetV[0] += homeX / homeR * Boid.home * math.pow(count, 0.5)
        self.targetV[1] += homeY / homeR * Boid.home * math.pow(count, 0.5)
        
        # Avoid wall
        if self.pos[0] < 50:
            self.targetV[0] += 5
        elif self.pos[0] > self.bounds[0] - 50:
            self.targetV[0] -= 5
        if self.pos[1] < 50:
            self.targetV[1] += 5
        elif self.pos[1] > self.bounds[1] - 50:
            self.targetV[1] -= 5

        # Update acceleration
        self.acc[0] = self.targetV[0] - self.vel[0]
        self.acc[1] = self.targetV[1] - self.vel[1]
        rAcc = math.pow(self.acc[0] * self.acc[0] + self.acc[1] * self.acc[1], 0.5) + 0.0001
        if rAcc > Boid.maxAcc:
            self.acc[0] = self.acc[0] / rAcc * Boid.maxAcc
            self.acc[1] = self.acc[1] / rAcc * Boid.maxAcc

        # Limit position and velocity
        if self.pos[0] < -50:
            self.pos[0] = self.bounds[0] + 50
        elif self.pos[0] > self.bounds[0] + 50:
            self.pos[0] = -50
        if self.pos[1] < -50:
            self.pos[1] = self.bounds[1] + 50
        elif self.pos[1] > self.bounds[1] + 50:
            self.pos[1] = -50

        if self.vel[0] > Boid.maxVel:
            self.vel[0] = Boid.maxVel
        elif self.vel[0] < -Boid.maxVel:
            self.vel[0] = -Boid.maxVel
        if self.vel[1] > Boid.maxVel:
            self.vel[1] = Boid.maxVel
        elif self.vel[1] < -Boid.maxVel:
            self.vel[1] = -Boid.maxVel

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
