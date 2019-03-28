"""
Raphael Holzer
16. 02. 2019

Displaying a window with the text 'Hello World'.
"""

import cocos
import pyglet
import os
from cocos.actions import *
from cocos.director import director


class Cat(cocos.layer.Layer):
    """Display a cat sprite which reacts to mouse and key input.
    Pressing the keys:
    - R rotations by 90 degrees
    - S scales by 1.5
    - N returns the scale back to 1
    A mouse click moves the sprite to a new position."""

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
        
        
class EventDisplay(cocos.layer.Layer):
    """This layer displays events (keyboard, mouse)."""
    
    is_event_handler = True     #: enable pyglet's events

    def __init__(self):
        super(EventDisplay, self).__init__()

        self.text = cocos.text.Label("", x=20, y=20)
        self.add(self.text)
        
        
        # To keep track of which keys are pressed:
        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)
        
        self.animals = ['cat', 'bird', 'cow']
        self.animal_index = 0
        self.animal = 'cat'
        self.animal_label = cocos.text.Label('bird', x=20, y=40)
        self.add(self.animal_label)
        
        self.animals_label = cocos.text.Label('cat bird cow', x=20, y=60)
        self.add(self.animals_label)
        
        self.mouse_action = 'None'
        self.mouse_modifiers = ''
        self.mouse_label = cocos.text.Label('No mouse events yet', x=20, y=100)
        self.add(self.mouse_label)

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        text = 'Keys: ' + ','.join(key_names)
        # Update self.text
        self.text.element.text = text
        #self.animal_label.element.text = 'other'

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.update_text()
        if key == pyglet.window.key.A:
            self.animal_index = (self.animal_index + 1) % len(self.animals)
            self.animal = self.animals[self.animal_index]
            print(self.animal)

    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)
        self.update_text()

    def update_mouse_label(self, x, y):
        template = 'Mouse @ ({}, {}), action = {}'
        if self.mouse_action == 'press':
            template += ', mod = {}'
        text = template.format(x, y, self.mouse_action, self.mouse_modifiers)
        self.mouse_label.element.text = text

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_action = 'motion'
        self.update_mouse_label(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse_action = 'drag'
        self.update_mouse_label(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.mouse_action = 'press'
        self.mouse_modifiers = modifiers
        self.posx, self.posy = director.get_virtual_coordinates(x, y)
        self.update_mouse_label(x, y)

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
        
        scale = ScaleBy(2, duration=1)
        
        cow = cocos.sprite.Sprite('animals/cow-icon.png')
        cow.do(Repeat(Reverse(scale) + scale))
        cow.position = 200, 200
        self.add(cow, z=1)


def on_key_press(self, key, modifiers):
    print('key', key, modifiers)


def main():
    # initialize the director
    cocos.director.director.init(resizable=True)
    
    animals = os.listdir('animals')
    sprites = []
    for animal in animals:
        path = 'animals/'+animal
        s = cocos.sprite.Sprite(path)
        sprites.append(s)

    print(sprites[1])
    
    # define a layer
    hello_layer = HelloWorld()
    event_layer = EventDisplay()
    
    scale = ScaleBy(5, duration=1)
    rot90 = RotateBy(90, duration=2)
    
    hello_layer.do(Repeat(rot90 + scale + Reverse(scale)))
    
    # place a layer into the scene
    main_scene = cocos.scene.Scene(hello_layer, event_layer, Cat())
    
    # run the scene
    cocos.director.director.run(main_scene)
    
if __name__ == "__main__":
    main()
