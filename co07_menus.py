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
        super(OptionsMenu, self).__init__('Options')
        
        items = []
        self.volumes = ['Mute','10','20','30','40','50','60','70','80','90','100']

        items.append(MultipleMenuItem(
                        'SFX volume: ', 
                        self.on_volume,
                        self.volumes,
                        5)
                    )
        items.append(MultipleMenuItem(
                        'Music volume: ', 
                        self.on_volume,
                        self.volumes,
                        5)
                    )
        items.append(ToggleMenuItem('Show FPS:', self.on_show_fps, director.show_FPS) )
        items.append(MenuItem('Fullscreen', self.on_fullscreen) )
        items.append(MenuItem('Back', self.on_quit) )
        self.create_menu( items, shake(), shake_back() )

    def on_fullscreen(self):
        director.window.set_fullscreen(not director.window.fullscreen)

    def on_quit(self):
        self.parent.switch_to(0)

    def on_show_fps(self, value):
        director.show_FPS = value

    def on_volume(self, idx):
        # called with the index (0 .. 10)
        pass


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