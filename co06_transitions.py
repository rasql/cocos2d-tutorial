"""
Raphael Holzer
16. 02. 2019

Displaying different transitions.
http://python.cocos2d.org/doc/api/cocos.scenes.transitions.html
"""

import cocos
from cocos.actions import *
from cocos.scenes.transitions import *
from cocos.director import director
from pyglet.window import key

transitions = [
    RotoZoomTransition,
    JumpZoomTransition,
    SplitColsTransition,
    SplitRowsTransition,
    MoveInLTransition,
    MoveInRTransition,
    MoveInBTransition,
    MoveInTTransition,
    SlideInLTransition,
    SlideInRTransition,
    SlideInBTransition,
    SlideInTTransition,
    FlipX3DTransition,
    FlipY3DTransition,
    FlipAngular3DTransition,
    ShuffleTransition,
    ShrinkGrowTransition,
    CornerMoveTransition,
    EnvelopeTransition,
    FadeTRTransition,
    FadeBLTransition,
    FadeUpTransition,
    FadeDownTransition,
    TurnOffTilesTransition,
    FadeTransition,
    ZoomTransition,
]
print(len(transitions))

scenes = []

class Layer1(cocos.layer.ColorLayer):
    def __init__(self):
        super(Layer1, self).__init__(250, 0, 0, 0)

        sprite = cocos.sprite.Sprite('animals/cow-icon.png')
        sprite.position = (320, 240)

        rot = RotateBy(360, 2)
        sprite.do(Repeat(rot + Reverse(rot)))
        self.add(sprite)


class Layer2(cocos.layer.ColorLayer):
    def __init__(self):
        super(Layer2, self).__init__(250, 0, 0, 0)

        sprite = cocos.sprite.Sprite('animals/cat-icon.png')
        sprite.position = (320, 240)

        scale = ScaleBy(4, 1)
        sprite.do(Repeat(scale + Reverse(scale)))
        self.add(sprite)


class Control(cocos.layer.Layer):
    """Display an animal which does different actions.
    LEFT/RIGHT selects transitions, ENTER does execute it."""
    
    is_event_handler = True     #: enable pyglet's events
    def __init__(self):
        super(Control, self).__init__()
        
        self.index = 0
        self.transition = transitions[0]
        self.text = cocos.text.Label(transitions[0].__name__, x=20, y=20)
        self.add(self.text)
        msg = 'Left/Right to select transition, Enter to execute'
        self.add(cocos.text.Label(msg, x=20, y=460))
        self.scene = 0

        
    def on_key_release(self, key_code, mod):
        n = len(transitions)
        if key_code == key.LEFT:
            self.index = (self.index - 1) % n            
        elif key_code == key.RIGHT:
            self.index = (self.index + 1) % n
        elif key_code == key.RETURN:
            self.scene = (self.scene + 1) % 2
            director.replace(transitions[self.index](scenes[self.scene], 1.25))

        self.transition = transitions[self.index]
        self.text.element.text = transitions[self.index].__name__

def main():
    # initialize the director
    cocos.director.director.init(caption='Transition demo', resizable=True)
    
    # define a layer
    control_layer = Control()
    c1 = cocos.layer.ColorLayer(128, 16, 16, 255)
    c2 = cocos.layer.ColorLayer(0, 127, 127, 255)
        
    global scenes
    scenes = [
        cocos.scene.Scene(c1, Layer1(), control_layer),
        cocos.scene.Scene(c2, Layer2(), control_layer),
    ]
            
    # run the scene
    cocos.director.director.run(scenes[0])    
    
if __name__ == "__main__":
    main()