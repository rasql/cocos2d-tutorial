"""
Raphael Holzer
16. 02. 2019

Displaying different actions.
http://python.cocos2d.org/doc/programming_guide/actions.html
"""

import cocos
from cocos.actions import *
from cocos.director import director
from pyglet.window import key

actions = ['Rotate(360, 1)',
           'Rotate(-90, 1)',
           'MoveBy((50, 100), 1)',
           'MoveBy((0, 200), 1) + MoveBy((200, 0), 1) + MoveBy((0, -200), 1) + MoveBy((-200, 0), 1)',
           'MoveBy((200, 0), 2) | Rotate(360, 1)',
           'Rotate(360, 0.5) * 3',
           'Repeat(Rotate(360, 0.5))',
           'Repeat(ScaleBy(2, 1) + Reverse(ScaleBy(2, 0.5)))',
           'Reverse(MoveBy((50, 100), 1))',
           'MoveTo((0, 0), 2)',
           'Place((200, 200))',
           'ScaleBy(2, 1)',
           'Reverse(ScaleBy(2, 0.5))',
           'JumpBy((400, 0), height=100, jumps=4, duration=3)',
           'Repeat(JumpBy((400, 0), jumps=4, duration=3)+Reverse(JumpBy((400, 0), duration=1)))',
           'Blink(3, 2)',
           'Show()',
           'Hide()',
           'ToggleVisibility()',
           'FadeIn(2)',
           'FadeOut(1)',]

class Animal(cocos.layer.Layer):
    """Display an animal which does different actions.
    LEFT/RIGHT selections actions, ENTER does the action.
    A mouse-click repositions the animl."""
    
    is_event_handler = True     #: enable pyglet's events
    def __init__(self):
        super(Animal, self).__init__()
        
        self.cat = cocos.sprite.Sprite('animals/cat-icon.png')
        self.cat.position = 200, 200
        self.add(self.cat)
        self.index = 0
        self.action = eval(actions[0])
        self.text = cocos.text.Label(actions[0], x=20, y=20)
        self.add(self.text)
        msg = 'Left/right to select action, Enter to execute, mouse-click to position'
        self.add(cocos.text.Label(msg, x=20, y=460))
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        self.cat.position = director.get_virtual_coordinates(x, y) 
        
    def on_key_release(self, key_code, mod):
        n = len(actions)
        if key_code == key.LEFT:
            self.index = (self.index - 1) % n            
        elif key_code == key.RIGHT:
            self.index = (self.index + 1) % n
        elif key_code == key.RETURN:
            self.cat.do(self.action)
        
        self.action = eval(actions[self.index])
        self.text.element.text = actions[self.index]
    
if __name__ == "__main__":
    print(__file__)
    cocos.director.director.init()
    layer = Animal()
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)    