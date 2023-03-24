import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.offsetbox as offsetbox
from itertools import product
import time

_empty_set = set()
radius = 0.01


class Grid:
    def __init__(self, volume, num):
        self.grid = {}
        self.bucket_map = {}
        self.separation = np.array([(i[1]-i[0]) / num for i in volume])
        self.volume = volume
        self.dim = len(volume)
        if self.dim < 2:
            self.start = [int(volume[0][0] // self.separation), 0]
            self.end = [int((volume[0][1] + 1) // self.separation), 1]
            self.dim = 2
        else:
            self.start = [int(boundary[0] // self.separation[i]) for i, boundary in enumerate(volume)]
            self.end = [int((boundary[1] + 1) // self.separation[i]) for i, boundary in enumerate(volume)]

    def key(self, particle):
        return tuple(particle.position // self.separation)

    def add_particle(self, particle):
        k = self.key(particle)
        if k in self.grid:
            cell = self.grid[k]
        else:
            cell = set()
            self.grid[k] = cell

        cell.add(particle)
        self.bucket_map[particle] = cell
        particle.key = k

    def remove_particle(self, particle):
        self.bucket_map[particle].remove(particle)

    def update_particle(self, particle):
        if self.key(particle) != particle.key:
            self.remove_particle(particle)
            self.add_particle(particle)

    def update_grid(self):
        self.grid = {k: v for k, v in self.grid.items() if v != _empty_set}
        self.bucket_map = {k: v for k, v in self.bucket_map.items() if k != _empty_set}

    def update(self, dt):

        for index in product(*[range(start, end) for start, end in zip(self.start, self.end)]):
            for particle in self.grid.get(index, _empty_set):

                for i in product(*[range(-1, 2) for i in range(self.dim)]):
                    for particle2 in self.grid.get(tuple(np.array(index) + np.array(i)), _empty_set):
                        if particle2 != particle:
                            particle.collide(particle2)


        momentum = 0
        for particle in self.bucket_map:
            particle.update(dt)
            momentum += particle.walls() * particle.mass * np.linalg.norm(particle.velocity)

        for particle, _ in self.bucket_map.items():
            self.update_particle(particle)

        self.update_grid()

        return momentum

    def get_particles(self):
        for i in self.bucket_map:
            yield i


def hypot(*array):
    if len(array) == 1:
        return abs(array[0])
    else:
        return np.hypot(*array)


class Particle:
    def __init__(self, ini_volume, ini_temp, mass=1.0):
        self.position = np.array([random.uniform(float(i[0] + radius), float(i[1] - radius)) for i in ini_volume])
        self.mass = mass

        v = math.sqrt(3 * 8.317162 * ini_temp / self.mass)
        theta = random.uniform(-np.pi, np.pi)
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        self.velocity = np.dot(rot, np.array([random.randrange(int(v*0.7), int(v*1.3)) for i in ini_volume]))

        if self.position.size < 2:
            self.position = np.array([self.position[0], 0])
            self.velocity = np.array([self.velocity[0], 0])

        self.radius = radius * self.mass
        self.space = ini_volume.copy()
        self.previous_velocity = self.velocity.copy()
        self.key = 0

    def update(self, dt):
        self.position += self.velocity * dt
        self.previous_velocity = self.velocity.copy()

    def walls(self):
        condition_table = [self.space[i][0] > self.position[i] - radius or
                           self.space[i][1] < self.position[i] + radius for i in range(len(self.space))]

        if any(condition_table):
            for i, value in enumerate(condition_table):
                if value:
                    self.velocity[i] *= -1

        collision_total = sum(condition_table)
        return collision_total

    def collide(self, particle):
        if hypot(*(self.position - particle.position)) > self.radius + particle.radius:
            return

        M = self.mass + particle.mass
        v1 = self.previous_velocity
        v2 = particle.previous_velocity

        self.velocity = ((self.mass - particle.mass) * v1 + (2 * particle.mass) * v2) / M


temp = 200
volume = [(-10.0, 10.0), (-10.0, 10.0)]
grid = Grid(volume, 10 / 0.1)

for i in range(100):
    particle = Particle(volume, temp, 1)
    grid.add_particle(particle)

for i in range(500):
    particle = Particle([(-1, 1), (-1, 1)], temp * 3, 0.4)
    particle.space = volume
    grid.add_particle(particle)

fig, ax = plt.subplots()
ax.set(xlim=[volume[0][0], volume[0][1]], ylim=[-10, 10])

text = offsetbox.AnchoredText("0", loc=1)
ax.add_artist(text)

cmap = plt.colormaps['jet']

circles = {particle: plt.Circle(tuple(particle.position), particle.radius * 3,
                                color=cmap(random.random()))
           for particle in grid.get_particles()}
for circle in circles.values():
    ax.add_patch(circle)

dt = 0.001
total = 0
totals = []

def animate(frame):
    global total, totals

    if frame == 9:
        totals.append(total)
        totals = totals[-10:]
        total = 0

    total += grid.update(dt)

    for particle in grid.get_particles():
        circles[particle].set_center(tuple(particle.position))

    if len(totals) > 0:
        text.txt.set_text(f"{np.mean(totals) /(40.0 * dt)}")

    return circles, text


ani = animation.FuncAnimation(fig, animate, 10, interval=0)
plt.grid("minor")
plt.show()