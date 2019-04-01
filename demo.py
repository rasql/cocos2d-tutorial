"""
Raphael Holzer
16. 02. 2019
Cocos2D Tutorial
"""

import cocos
import pyglet
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer, MultiplexLayer, PythonInterpreterLayer
from cocos.text import Label
from mylib import Title, SwitchScene, SwitchLayer
from mylib import Mouse, ActionMenu, EffectMenu, TransitionMenu, actions, effects, transitions
from menus import OptionsMenu
        
class DriveCar(cocos.actions.Driver):
    def step(self, dt):
        # handle input and move the car
        self.target.rotation += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 150 * dt
        self.target.acceleration = (keyboard[key.UP] - keyboard[key.DOWN]) * 400
        if keyboard[key.SPACE]: self.target.speed = 0
        super(DriveCar, self).step(dt)
        scroller.set_focus(self.target.x, self.target.y)



def main():
    # initialize the director
    director.init(800, 600, resizable=True)
    # create the scene switch layer
    switch_layer = SwitchScene()    

    # define the scene switch layer


    red = ColorLayer(255, 0, 0, 255)
    green = ColorLayer(0, 255, 0, 255)
    blue = ColorLayer(0, 0, 255, 255)

    # place all scenes in a scene list
    scenes = [
        Scene(Title('Cocos2D tutorial'), switch_layer),
        Scene(SwitchLayer(red, green, blue), switch_layer),
        Scene(PythonInterpreterLayer(), switch_layer),
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