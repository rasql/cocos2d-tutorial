"""
Demonstration of transitions between scenes.
"""

import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.layer import ColorLayer, Layer
from cocos.scenes.transitions import *

import pyglet
from pyglet.window import key
from lib.listmenu import ListMenu

pyglet.resource.path = ['../animals']
pyglet.resource.reindex()

transitions = [
    'RotoZoomTransition',
    'JumpZoomTransition',
    'SplitColsTransition',
    'SplitRowsTransition',
    'MoveInLTransition',
    'MoveInRTransition',
    'MoveInBTransition',
    'MoveInTTransition',
    'SlideInLTransition',
    'SlideInRTransition',
    'SlideInBTransition',
    'SlideInTTransition',
    'FlipX3DTransition',
    'FlipY3DTransition',
    'FlipAngular3DTransition',
    'ShuffleTransition',
    'ShrinkGrowTransition',
    'CornerMoveTransition',
    'EnvelopeTransition',
    'FadeTRTransition',
    'FadeBLTransition',
    'FadeUpTransition',
    'FadeDownTransition',
    'TurnOffTilesTransition',
    'FadeTransition',
    'ZoomTransition',
]

class Transitions(ListMenu):
    def __init__(self, *args, **kwargs):
        super(Transitions, self).__init__(transitions, wrap=True, *args, *kwargs)
        w, h = director.get_window_size()

        # Define three different sprites
        s0 = Sprite('cow-icon.png', position=(w//2, h//2), scale=2)
        s1 = Sprite('bird-icon.png', position=(w//2, h//2), scale=2)
        s2 = Sprite('parrot-icon.png', position=(w//2, h//2), scale=2)

        # Define three different scenes
        scene0 = Scene(ColorLayer(100, 0, 0, 255), s0, self)
        scene1 = Scene(ColorLayer(0, 100, 0, 255), s1, self)
        scene2 = Scene(ColorLayer(0, 0, 100, 255), s2, self)
        
        self.scenes = [scene0, scene1, scene2]
        self.scene_index = 0
    
    def cb(self):
        if self.k == key.ENTER:
            self.scene_index += 1
            self.scene_index %= len(self.scenes)
            scene = self.scenes[self.scene_index]
            transition = eval(self.item)
            director.replace(transition(scene, 1))

if __name__ == '__main__':
    director.init(caption='Transitions', resizable=True)
    director.run(Transitions().scenes[0])
