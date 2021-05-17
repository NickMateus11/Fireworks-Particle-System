import pygame
from random import randint
import numpy as np


w, h = 800, 600
pygame.init()
screen = pygame.display.set_mode((w, h))

clock = pygame.time.Clock()

BLACK = pygame.Color("black")
WHITE = pygame.Color("white")


class Particle():
    def __init__(self, x=None, y=None, vx=0, vy=0, size=5, color=None, large_trail=False):
        self.x = x if x is not None else randint(0,w)
        self.y = y if y is not None else randint(0,h)
        self.vx = vx
        self.vy = vy
        self.size = size
        self.g = 1
        if color is not None:
            self.color = color
        else:
            self.color = pygame.Color(0,0,0)
            self.color.hsva = (randint(0,360), randint(80,100), 100)
        
        self.trail = []
        self.trail_max = 5 if not large_trail else 10

    def update(self):
        self.trail.append([self.x, self.y])
        if len(self.trail)>self.trail_max:
            self.trail.pop(0)
        self.x += self.vx
        self.y += self.vy

        self.vy += self.g
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        for i in range(len(self.trail)):
            factor = (len(self.trail)-i)/min(self.trail_max,len(self.trail))
            pygame.draw.circle(screen, self.color, (self.trail[i][0], self.trail[i][1]), self.size*(1-factor))


    def fade(self):
        rate = 8
        self.color = (
            max(self.color[0]-rate,0), 
            max(self.color[1]-rate,0), 
            max(self.color[2]-rate,0)
        )


class Firework(Particle):
    def __init__(self):
        self.x = randint(0,w)
        self.y = h
        self.vy = -randint(15,33)
        self.exploded = False
        self.particles = []
        Particle.__init__(self, self.x, self.y, 0, vy=self.vy)

    def update(self):
        Particle.update(self)
        if self.vy == 0:
            self.exploded = True
            theta = 0
            n = 50
            for _ in range(0,n):
                theta += 2*np.pi/n
                r = randint(1,8)
                vx = r*np.cos(theta)
                vy = r*np.sin(theta)
                p = Particle(self.x, self.y, vx, vy, 2, self.color, True)
                self.particles.append(p)
        for p in self.particles:
            p.update()
            p.fade()

    
    def draw(self):
        if not self.exploded:
            Particle.draw(self)
        for p in self.particles:
            p.draw()


def main():

    particles = []
    frame = 0
    framerate = 30

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        if (frame%(framerate/3) == 0):
            particles.append(Firework())
        frame += 1

        n = len(particles)
        for i in range(n-1,-1,-1):
            particles[i].update()
            particles[i].draw()
            if particles[i].y > h:
                particles.pop(i)

        pygame.display.flip()
        clock.tick(framerate)


if __name__ == "__main__":
    main()
