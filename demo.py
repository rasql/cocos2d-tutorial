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
from cocos.sprite import Sprite
from cocos.actions import *

from mylib import Title, SwitchScene, SwitchLayer
from mylib import ActionMenu, EffectMenu, TransitionMenu, actions, effects, transitions
from menus import OptionsMenu
from pong import Pong
        
class DriveCar(cocos.actions.Driver):
    def step(self, dt):
        # handle input and move the car
        self.target.rotation += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 150 * dt
        self.target.acceleration = (keyboard[key.UP] - keyboard[key.DOWN]) * 400
        if keyboard[key.SPACE]: self.target.speed = 0
        super(DriveCar, self).step(dt)
        scroller.set_focus(self.target.x, self.target.y)


class HelloWorld(Layer):
    """Display the text 'hello world' in the center."""
    def __init__(self):
        super(HelloWorld, self).__init__()
        w, h = director.get_window_size()
        self.label = Label('Hello World', position=(w//2, h//2), 
            font_size=36, anchor_x='center', anchor_y='center')
        self.add(self.label)

class AddActor(Layer):
    """Display an actor in the center of the window."""
    def __init__(self):
        super(AddActor, self).__init__()
        w, h = director.get_window_size()
        self.sprite = Sprite('animals/dog-icon.png', position=(w//2, h//2))
        self.add(self.sprite)

class AddAction(Layer):
    """Display an actor and add a simple action."""
    def __init__(self):
        super(AddAction, self).__init__()
        w, h = director.get_window_size()
        self.sprite = Sprite('animals/dog-icon.png', position=(w//2, h//2))
        self.sprite.do(Repeat(Rotate(360, 2))|Repeat(ScaleBy(2, 1)+Reverse(ScaleBy(2, 1))))
        self.add(self.sprite)

class Mouse(Layer):
    """This class displays the mouse coordinates in the status line,
    * mouse press: the image jumps to the new position
    * mouse drag: the image moves with the mouse
    * mouse move: the mouse coordinates are displayed in the status line."""
    is_event_handler = True     #: enable pyglet's events
    
    def __init__(self):
        super(Mouse, self).__init__()
        self.img = Sprite('animals/mouse-icon.png')
        w, h = director.get_window_size()
        self.img.position = w//2, h//2
        self.add(self.img)

        self.status = Label('status', position=(10, 30))
        self.add(self.status)

    def on_mouse_motion(self, x, y, dx, dy):
        self.status.element.text = 'mouse motion pos=({}, {}), vec=({}, {})'.format(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.status.element.text = 'mouse drag pos=({}, {}), vec=({}, {}), but={}'.format(x, y, dx, dy, buttons)
        self.img.position = (x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.img.position = (x, y)


class Cat(cocos.layer.Layer):
    """Display a sprite sprite which reacts to mouse and key input.
    - R : rotate by 90 degrees
    - S : scale by 1.5
    - N : return back to normal (scale=1)
    - mouse press : move the sprite to the new position."""

    is_event_handler = True
    
    def __init__(self):
        super(Cat, self).__init__()
        
        self.cat = cocos.sprite.Sprite('animals/cat-icon.png')
        self.cat.position = 200, 200
        self.add(self.cat, z=1)
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        self.cat.position = director.get_virtual_coordinates(x, y)
        
    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.R:
            self.cat.do(Rotate(90, 1))
        elif key == pyglet.window.key.S:
            self.cat.do(ScaleBy(1.5, 1))
        elif key == pyglet.window.key.N:
            self.cat.scale = 1


def main():
    # initialize the director
    director.init(800, 600, resizable=True)
    # create the scene switch layer
    switch_layer = SwitchScene()    

    # define the scene switch layer


    red = ColorLayer(255, 0, 0, 255)
    green = ColorLayer(0, 255, 0, 255)
    blue = ColorLayer(0, 0, 255, 255)

    # Goal: adding class name and docstring
    # 1 using on_enter:
    # get parent().__name__
    # get parent().__doc__


    # place all scenes in a scene list
    scenes = [
        Scene(Title('Cocos2D tutorial'), switch_layer),
        Scene(HelloWorld(), switch_layer),
        Scene(AddActor(), switch_layer),
        Scene(AddAction(), switch_layer),
        Scene(Mouse(), switch_layer),
        Scene(Cat(), switch_layer),     
        Scene(Pong(), switch_layer),     
        Scene(SwitchLayer(red, green, blue), switch_layer),
        Scene(PythonInterpreterLayer(), switch_layer),
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