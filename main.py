import math
import pygame

WIDTH = 600
HEIGHT = 600
G = 6.67*10**-11
DT = 14600*10
SCALE = 15.9e9

class Object:
    def __init__(self, x, y, vel, width, m, colour) -> None:
        self.x = x
        self.y = y
        self.vel = vel
        self.width = width
        self.colour = colour
        self.m = m
        self.prev = [(x - vel[0] * DT, y - vel[1] * DT)]

    def calcFg(self, sun):
        r = math.sqrt((self.x-sun.x)**2+(self.y-sun.y)**2)
        if r==0:
            return 0
        return G*self.m*sun.m/r**2

    def calc_acceleration(self, sun):
        r = math.sqrt((self.x-sun.x)**2+(self.y-sun.y)**2)
        if r == 0:
            return 0

        a = self.calcFg(sun)/self.m
        dx = sun.x - self.x
        dy = sun.y - self.y

        ax = a*dx/r
        ay = a*dy/r

        return (ax, ay)

    def update_position(self, sun):
        ax, ay = self.calc_acceleration(sun)
        newx = 2* self.x - self.prev[-1][0] + ax *DT**2
        newy = 2* self.y - self.prev[-1][1] + ay *DT**2
        self.prev.append((self.x, self.y))
        self.x, self.y = newx, newy

    def draw(self, screen):
        scaledx = int(self.x/SCALE+WIDTH/2)
        scaledy = int(self.y/SCALE+HEIGHT/2)
        pygame.draw.circle(screen, self.colour, (scaledx,scaledy), self.width)

    def drawLine(self, screen):
        for pos in self.prev:
            scaledx = int(pos[0]/SCALE+WIDTH/2)
            scaledy = int(pos[1]/SCALE+HEIGHT/2)
            screen.set_at((scaledx, scaledy), self.colour)


# Sun
sun = Object(WIDTH/2, HEIGHT/2, (0, 0), 1, 1.989e30, "YELLOW")

# Mercury
mercury = Object(
    WIDTH/2 + 57.91e9,  # Initial distance from the Sun (semi-major axis in meters)
    HEIGHT/2,
    (0, -47.87e3),  # Orbital velocity in m/s
    1,  # Display size
    3.301e23,  # Mass in kg
    "GRAY"
)

# Venus
venus = Object(
    WIDTH/2 + 108.2e9,
    HEIGHT/2,
    (0, -35.02e3),
    1,
    4.867e24,
    "ORANGE"
)

# Earth
earth = Object(
    WIDTH/2 + 149.6e9,
    HEIGHT/2,
    (0, -29.78e3),
    1,
    5.972e24,
    "BLUE"
)

# Mars
mars = Object(
    WIDTH/2 + 227.9e9,
    HEIGHT/2,
    (0, -24.077e3),
    1,
    6.417e23,
    "RED"
)

# Jupiter
jupiter = Object(
    WIDTH/2 + 778.5e9,
    HEIGHT/2,
    (0, -13.07e3),
    1,
    1.898e27,
    "BROWN"
)

# Saturn
saturn = Object(
    WIDTH/2 + 1.434e12,
    HEIGHT/2,
    (0, -9.69e3),
    1,
    5.683e26,
    "YELLOW"
)

# Uranus
uranus = Object(
    WIDTH/2 + 2.871e12,
    HEIGHT/2,
    (0, -6.81e3),
    1,
    8.681e25,
    "CYAN"
)

# Neptune
neptune = Object(
    WIDTH/2 + 4.495e12,
    HEIGHT/2,
    (0, -5.43e3),
    1,
    1.024e26,
    "BLUE"
)

planets = [earth, mercury, venus, mars, jupiter, neptune, uranus]


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planets")

screen.fill("BLACK")

running = True
clock = pygame.time.Clock()

while running: 
    clock.tick(60)
    screen.fill("BLACK")
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False

    sun.draw(screen)

    for planet in planets:
        planet.update_position(sun)
        planet.draw(screen)
        planet.drawLine(screen)

    pygame.display.flip()

pygame.quit()
