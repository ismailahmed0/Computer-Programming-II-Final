'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Ismail A Ahmed
Advanced Computer Programming Final
Version 1.0

'''

import pygame
import sys
import random
import time
window_width = 640
window_height = 480
screen = pygame.display.set_mode((window_width, window_height))

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
global color
color = GREEN
global sped
sped = 5

def doRectsOverlap(rect1, rect2): #checks to see if the first rect collides coordinates with the second
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if ((isPointInsideRect(a.left, a.top, b)) or
            (isPointInsideRect(a.left, a.bottom, b)) or
            (isPointInsideRect(a.right, a.top, b)) or
            (isPointInsideRect(a.right, a.bottom, b))):
            return True

    return False

def isPointInsideRect(x, y, rect): #checks to see if the point is inside the rect
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False


class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Line(Entity):
    """
    The Line! Moves around the screen!
    """

    def __init__(self, x, y, width, height):
        super(Line, self).__init__(x, y, width, height)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.x_direction = -1
        self.speed = 5
    def update(self):
        # Moves the line
        self.rect.move_ip(self.speed * self.x_direction, 0)
        directions = [1, -1]
        if self.rect.x <= 0:
            self.x_direction *= -1
        elif self.rect.x >= 450:
            self.x_direction *= -1

class Rrect(Entity):
    """
    The red rectangle! Stays still!
    """

    def __init__(self, x, y, width, height):
        super(Rrect, self).__init__(x, y, width, height)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

class Circ(pygame.sprite.Sprite): #player will be a circle

    def __init__(self,x,y):
        super().__init__()

        self.image = pygame.Surface((100,100))
        self.image.fill(BLUE)

        pygame.draw.circle(self.image, color, (50, 50), 50, 0)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #self.barrier = None
        directions = [1,-1] #makes it go other ways
        self.x_direction = random.choice(directions)
        # Positive = down, negative = up
        self.y_direction = random.choice(directions)
        self.speed = 5

    def update(self):
        global color
        self.rect.move_ip(self.speed * self.x_direction,
                          self.speed * self.y_direction)
        # Keep the ball in bounds, and make it bounce off the sides.
        directions = [1, -1]

        if self.rect.y < 0:
            self.y_direction *= -1
            if self.speed >= 15:
                self.speed = 5
            elif self.speed >= 5 and self.speed <= 14:
                self.speed += 1
            color = PURPLE

        elif self.rect.y > window_height - 100:
            self.y_direction *= -1
            if self.speed >= 15:
                self.speed = 5
            elif self.speed >= 5 and self.speed <= 14:
                self.speed += 1

            color = YELLOW

        if self.rect.x < 0:
            self.x_direction *= -1 #makes go opposite direction
            if self.speed >= 15:
                self.speed = 5
            elif self.speed >= 5 and self.speed <= 14:
                self.speed += 1

            color = GRAY

        elif self.rect.x > window_width - 100:
            self.x_direction *= -1
            if self.speed >= 15:
                self.speed = 5
            elif self.speed >= 5 and self.speed <= 14:
                self.speed += 1

            color = ORANGE



pygame.init()

# screen info
pygame.display.set_caption("Advanced Computer Programming Final")
clock = pygame.time.Clock()

player = Line(220, 20, 200, 4)
redy = Rrect(590, 435, 100, 100)
circle = Circ(50,50)

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)
all_sprites_list.add(circle)
all_sprites_list.add(redy)

end_it = False
while (end_it == False):
    screen.fill(WHITE)
    myfont = pygame.font.SysFont(None, 40)
    nlabel = myfont.render("Press space to start!", 1, (BLACK))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # so game doesnt get all glitchy when you try to exit without this code
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                end_it = True  # stops the while true
    screen.blit(nlabel, (200, 230))

    pygame.display.flip()

while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    for ent in all_sprites_list:
        ent.update()

    if doRectsOverlap(player.rect, circle.rect):
        color = WHITE
        if circle.speed >= 15:
            circle.speed = 5
        elif circle.speed >= 5 and circle.speed <= 14:
            circle.speed +=1
        circle.x_direction *= -1
        circle.y_direction *= -1
    if doRectsOverlap(player.rect, redy.rect):
        color = RED
        if circle.speed >= 15:
            circle.speed = 5
        elif circle.speed >= 5 and circle.speed <= 14:
            circle.speed +=1
        circle.x_direction *= -1
        circle.y_direction *= -1

    screen.fill(BLUE)
    all_sprites_list.draw(screen)

    pygame.display.flip()
    clock.tick(60)


