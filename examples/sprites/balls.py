"""
This module shows how to animate sprites
"""

import cocos
import pyglet
from cocos.director import director
from cocos.sprite import Sprite

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

class Game(cocos.layer.Layer):
    def __init__(self):
        super(Game, self).__init__()
        sprite = Sprite('asteroid.png')
        self.add(sprite)

if __name__ == '__main__':
    director.init(caption='Asteroids', resizable=True)
    director.run(cocos.scene.Scene().add(Game()))
