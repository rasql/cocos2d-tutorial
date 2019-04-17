import cocos
import pyglet
from cocos.director import director
from cocos.sprite import Sprite

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

class Game(cocos.layer.Layer):
    def __init__(self):
        w, h = director.get_window_size()
        super(Game, self).__init__()
        sprite = Sprite('asteroid.png', position=(100, 100))
        self.add(sprite)
        player = Sprite('player.png', position=(w//2, h//2))
        self.add(player)

if __name__ == '__main__':
    director.init(caption='Asteroids', resizable=True)
    director.run(cocos.scene.Scene().add(Game()))