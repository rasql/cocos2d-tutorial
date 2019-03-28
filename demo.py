"""
Raphael Holzer
16. 02. 2019

Displaying a window with the text 'Hello World'.
"""

import cocos
import pyglet
import actions

scene = None
scendes = []

class HelloWorld(cocos.layer.Layer):
    """Define a new layer class to display centered text"""
    def __init__(self):
        super(HelloWorld, self).__init__()
        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a cocosnode
        label = cocos.text.Label('Hello, World!',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')
        label.position = 320, 240
        self.add(label)
        
class SwitchScenes(cocos.layer.Layer):
    is_event_handler = True
    global scene, scenes

    def __init__(self):
        super(SwitchScenes, self).__init__()
        self.scenes = []
        self.index = 0

    def on_key_press(self, key, modifiers):
        """Switch between scenes."""
        if key == pyglet.window.key.RIGHT:
            self.index = (self.index + 1) % len(self.scenes)
            scene = self.scenes[self.index]
            cocos.director.director.replace(scene)


def main():
    # initialize the director
    cocos.director.director.init()
    
    # define a layer
    hello_layer = HelloWorld()
    action_layer = actions.Animal()
    switch_layer = SwitchScenes()

    # place a layer into the scene
    main_scene = cocos.scene.Scene(hello_layer, switch_layer)
    action_scene = cocos.scene.Scene(action_layer, switch_layer)
    switch_layer.scenes = [main_scene, action_scene]
    
    # run the scene
    cocos.director.director.run(main_scene) 
    
if __name__ == "__main__":
    main()