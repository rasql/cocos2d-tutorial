"""
Displaying different particle systems.
http://python.cocos2d.org/doc/api/cocos.particle_systems.html
"""

import cocos
from cocos.director import director
from cocos.particle_systems import *
from pyglet.window import key
from lib.listmenu import ListMenu


class ParticleSystem(ListMenu):
    """Display different particle systems.
    
    * Up/down : select a particle system
    * mouse click : select position for a new particle system
    * BACK : remove the last particle system from the list
    """
    is_event_handler = True

    particles = [
        Fireworks,
        Explosion,
        Fire,
        Flower,
        Smoke,
        Sun,
        Spiral,
        Meteor,
        Galaxy,
    ]

    items = [p.__name__ for p in particles]

    def __init__(self):
        super(ParticleSystem, self).__init__(self.items)
        self.add(cocos.layer.ColorLayer(0, 0, 0, 255), z=-1)
        self.p = self.particles[self.index]()
        self.p.position = (320,100)
        self.add(self.p)

    def on_mouse_press(self, x, y, buttons, mod):
        p = self.particles[self.index]()
        p.position = (x, y)
        self.add(p)

    def on_key_release(self, k, mod):
        if k == key.BACKSPACE:
            children = self.get_children()
            if len(children) > 2: 
                children[-1].kill()

if __name__ == '__main__':
    director.init(caption='Particle Systems', resizable=True)
    director.run(cocos.scene.Scene().add(ParticleSystem()))
