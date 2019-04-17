"""Flappy Bird impolements the game in different stages:
* without classes
* Bird class
* Wall class
"""

from random import randint

import cocos
import pyglet
from cocos.director import director
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.text import Label
import os

GAP = 130
GRAVITY = -0.3
FLAP_STRENGTH = 6.5
SPEED = 3

pyglet.resource.path = ['images']
pyglet.resource.reindex()

class Flappy(Layer):
    """Implements a flappy bird game."""
    is_event_handler = True
            
    def __init__(self):
        super(Flappy, self).__init__()
        w, h = director.get_window_size()

        self.bg = Sprite(pyglet.resource.image('background.png'))
        self.bg.position = w//2, h//2
        self.add(self.bg)
        self.score = 0

        self.top = Sprite(pyglet.resource.image('top.png'))
        self.top.image_anchor = 0, 0
        self.add(self.top)

        self.bottom = Sprite(pyglet.resource.image('bottom.png'))
        self.bottom.image_anchor = 0, self.bottom.height
        self.add(self.bottom)

        self.bird0 = pyglet.resource.image('bird0.png')
        self.bird1 = pyglet.resource.image('bird1.png')
        self.bird2 = pyglet.resource.image('bird2.png')
        self.birddead = pyglet.resource.image('birddead.png')
        
        self.bird = Sprite(self.bird0)
        self.bird.position = (200, 300)
        self.bird.vy = 0
        self.bird.dead = False
        self.add(self.bird)

        self.label = Label('0', color=(255, 255, 255, 255), 
            position=(120, h-100), font_size=72)
        self.add(self.label)

        self.reset_pipes()
        self.schedule(self.update)

    def reset_pipes(self):
        w, h = director.get_window_size()
        d = 20
        y = randint(d, h-d-GAP)
        x = 500
        self.bottom.position = x, y
        self.top.position = x, y+GAP

    def update_pipes(self):
        self.top.x -= SPEED
        self.bottom.x -= SPEED
        if self.top.x + self.top.width < 0:
            self.reset_pipes()
            self.score += 1
            self.label.element.text = str(self.score)

    def update_bird(self):
        uy = self.bird.vy
        self.bird.vy += GRAVITY
        self.bird.y += (uy + self.bird.vy) / 2

        if not self.bird.dead:
            if self.bird.vy < -3:
                self.bird.image = self.bird2
            else:
                self.bird.image = self.bird1

        if self.bird.x > self.top.x and \
            (self.bird.y < self.bottom.y or self.bird.y > self.top.y):
            self.dead = True
            self.bird.image = self.birddead
        
        if not 0 < self.bird.y < 720:
            self.bird.y = 300
            self.bird.dead = False
            self.score = 0
            self.label.element.text = str(self.score)
            self.bird.vy = 0
            self.reset_pipes()

        # self.label.element.text=str(self.score)

    def update(self, dt):
        self.update_pipes()
        self.update_bird()

    def on_key_press(self, k, mod):
        if not self.bird.dead:
            self.bird.vy = FLAP_STRENGTH

class BirdSprite(Sprite):
    """Implements the bird player.
    The questSion is : should Bird be a sprite or a layer?
    Let's start with a sprite.
    """
    is_event_handler = True

    def __init__(self):
        self.bird0 = pyglet.resource.image('bird0.png')
        self.bird1 = pyglet.resource.image('bird1.png')
        self.bird2 = pyglet.resource.image('bird2.png')
        self.birddead = pyglet.resource.image('birddead.png')
        super(BirdSprite, self).__init__(self.bird0)
        self.position = 200, 200

    def on_key_press(self, k, mod):
        print('key')
        if not self.bird.dead:
            self.bird.vy = FLAP_STRENGTH


class BirdLayer(Layer):
    """This layer implements the bird and handles its movement.
    any key - upwards push.
    """
    is_event_handler = True

    def __init__(self):
        self.bird0 = pyglet.resource.image('bird0.png')
        self.bird1 = pyglet.resource.image('bird1.png')
        self.bird2 = pyglet.resource.image('bird2.png')
        self.birddead = pyglet.resource.image('birddead.png')
        super(BirdLayer, self).__init__()
        self.bird = Sprite(self.bird0)
        self.bird.position = 200, 200
        self.bird.vy = 0
        self.add(self.bird)
        self.schedule(self.update)

    def on_key_press(self, k, mod):
        self.bird.vy = FLAP_STRENGTH

    def update(self, dt):
        g = -5
        self.bird.vy += g * dt
        self.bird.y += self.bird.vy
        if self.bird.y <= self.bird.height/2 :
            self.bird.y = self.bird.height/2


class WallLayer(Layer):
    """This layer implements the moving walls.
    """

    def __init__(self):
        super(WallLayer, self).__init__()
        self.top = Sprite(pyglet.resource.image('top.png'))
        self.top.image_anchor = (0, 0)
        self.top.vx = -200
        self.add(self.top)
    
        self.bottom = Sprite(pyglet.resource.image('bottom.png'))
        self.bottom.image_anchor = 0, self.bottom.height
        self.bottom.vx = -200
        self.add(self.bottom)

        self.reset()
        self.schedule(self.update)

    def reset(self):
        w, h = director.get_window_size()
        d = 20
        y = randint(d, h-d-GAP)
        x = 500
        self.bottom.position = x, y
        self.top.position = x, y+GAP

    def update(self, dt):
        w, h = director.get_window_size()
        self.top.x += self.top.vx *dt
        self.bottom.x += self.bottom.vx * dt
        if self.top.x < -self.top.width: 
            self.reset()
    

if __name__ == '__main__':
    director.init(resizable=True, caption='Flappy Bird')
    scene = Scene(Flappy())
    director.run(scene)