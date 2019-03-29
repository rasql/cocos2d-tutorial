"""
Raphael Holzer
16. 02. 2019

Displaying a main menu and an options menu.
"""

import cocos
import sys
from cocos.layer import *
from cocos.menu import *
from cocos.scene import *

class OptionsMenu(Menu):
    def __init__(self):
        super(OptionsMenu, self).__init__('Menus')
        
        items = []
        self.values = ['Mute','10','20','30','40','50','60','70','80','90','100']
        self.colors = [(255, 255, 255), (255, 0, 50), (0, 255, 50), (0, 50, 255)]

        items.append(MenuItem('Menu', self.cb0))    
        items.append(MultipleMenuItem('Multiple:', self.cb, self.values, 5))
        items.append(ToggleMenuItem('Toggle:', self.cb))
        items.append(EntryMenuItem('Entry:', self.cb, 'abc', 10))
        items.append(ColorMenuItem('Color:', self.cb, self.colors))
        items.append(ImageMenuItem('animals/bird-icon.png', self.cb0))
        
        self.create_menu( items, zoom_in(), zoom_out() )

    def cb0(self):
        """Callback function without callback value."""
        print('cb')

    def cb(self, val):
        """Callback function with callback value."""
        print('cb value =', val)


class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Main')
        
        items = []
        items.append(MenuItem('New', self.on_new_game))
        items.append(MenuItem('Options', self.on_options))
        items.append(MenuItem('Scores', self.on_scores))
        items.append(MenuItem('Quit', self.on_quit))
        
        self.create_menu(items, shake(), shake_back())
        
    def on_new_game(self):
        print('new game')
        
    def on_options(self):
        self.parent.switch_to(1)
        
    def on_scores(self):
        print('scores')
        
    def on_quit(self):
        print('quit')
        cocos.director.pyglet.app.exit()
        sys.exit()
        
def main():   
    director.init(resizable=True)
    bg = cocos.layer.ColorLayer(0, 127, 127, 255)
    
    scene = Scene()
    scene.add(MultiplexLayer(MainMenu(), OptionsMenu()), z=1)
    scene.add(bg, z=0 )
    director.run(scene)    
    
if __name__ == "__main__":
    main()