# Problem : the image files are not found if the module is executed from another working directory
# Solution : search in pyglet.resources

import pyglet
import os
from cocos.director import director
from cocos.scene import Scene
from flappybird.flappybird import Flappy

# script_dir = os.path.dirname(__file__)
# print('script dir =', script_dir)
# path = os.path.join(script_dir, '/images/background.png')
# print('path =', path)

pyglet.resource.path = ['flappybird/images']
pyglet.resource.reindex()

director.init(resizable=True, caption='Flappy Bird')
scene = Scene(Flappy())
director.run(scene)