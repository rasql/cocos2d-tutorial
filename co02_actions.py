"""
Raphael Holzer
16. 02. 2019

Displaying a window with the text label 'Hello World'.
Make the label rotate and scale.
"""

import cocos
from cocos.actions import *

class HelloWorld(cocos.layer.ColorLayer):
    """Define a new layer class to display centered text"""
    def __init__(self):
        super(HelloWorld, self).__init__(64, 0, 255, 255)
        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a cocosnode
        label = cocos.text.Label('Hello, World!',
                                 font_name='Times New Roman',
                                 font_size=64,
                                 anchor_x='center', anchor_y='center')
        label.position = 320, 240
        self.add(label)
        
def main():
    # initialize the director
    cocos.director.director.init()
    
    # define a layer
    hello_layer = HelloWorld()
    
    scale = ScaleBy(5, duration=1)
    rot90 = RotateBy(90, duration=2)
    
    hello_layer.do(Repeat(rot90 + scale + Reverse(scale)))
    
    # place a layer into the scene
    main_scene = cocos.scene.Scene(hello_layer)
    
    # run the scene
    cocos.director.director.run(main_scene)    
    
if __name__ == "__main__":
    main()