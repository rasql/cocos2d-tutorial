"""
This is a template for new examples.
"""

import cocos
from cocos.director import director

class Game(cocos.layer.Layer):
    def __init__(self):
        super(Game, self).__init__()
        label = cocos.text.Label('Hello', font_size=140)
        self.add(label)

if __name__ == '__main__':
    director.init(caption='Template', resizable=True)
    scene = cocos.scene.Scene(Game())
    director.run(scene)