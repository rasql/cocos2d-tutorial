"""
Raphael Holzer
16. 02. 2019

Displaying a window with the text 'Hello World'.
"""

import cocos
import pyglet
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import ColorLayer
from actions import Animal
from mylib import Mouse, ActionMenu, EffectMenu, TransitionMenu, actions, effects, transitions
from menus import OptionsMenu


class HelloWorld(cocos.layer.Layer):
    """This layer displays the words 'Hello world' in the center."""
    def __init__(self):
        super(HelloWorld, self).__init__()
        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a cocosnode
        label = cocos.text.Label('Cocos2D Tutorial',
                                 font_name='Times New Roman',
                                 font_size=64,
                                 anchor_x='center', anchor_y='center',
                                 position=(400, 300))
        self.add(label)
        
class SwitchScenes(cocos.layer.Layer):
    """This layer allows to switch between different scenes by using the LEFT/RIGHT arrow."""
    is_event_handler = True

    def __init__(self):
        super(SwitchScenes, self).__init__()
        self.label = cocos.text.Label('Switch scenes : cmd+LEFT/RIGHT', x=5, y=5)
        self.add(self.label)
        self.scenes = []
        self.index = 0

    def on_key_press(self, key, modifiers):
        """Switch between scenes."""
        if key == pyglet.window.key.LEFT and modifiers & pyglet.window.key.MOD_COMMAND:
            self.index -= 1
            self.index %= len(self.scenes)
            scene = self.scenes[self.index]
            cocos.director.director.replace(scene)
        if key == pyglet.window.key.RIGHT and modifiers & pyglet.window.key.MOD_COMMAND:
            self.index += 1
            self.index %= len(self.scenes)
            scene = self.scenes[self.index]
            cocos.director.director.replace(scene)


def main():
    # initialize the director
    director.init(800, 600, resizable=True)
    
    # define the scene switch layer
    switch_layer = SwitchScenes()

    # place all scenes in a scene list
    scenes = [
        Scene(HelloWorld(), switch_layer),
        Scene(Animal(), switch_layer),
        Scene(Mouse(), switch_layer),
        Scene(ColorLayer(150, 0, 0, 255), switch_layer),
        Scene(OptionsMenu(), switch_layer),
        Scene(ColorLayer(0, 150, 0, 255), switch_layer),
        Scene(ActionMenu(actions), switch_layer),
        Scene(EffectMenu(effects), switch_layer),
        Scene(TransitionMenu(transitions), switch_layer)
        ]

    # give the scene list to the switch layer
    switch_layer.scenes = scenes
    
    # run the first scene
    cocos.director.director.run(scenes[0]) 
    
if __name__ == "__main__":
    main()