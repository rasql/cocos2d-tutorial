import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer, ScrollingManager, ScrollableLayer, MultiplexLayer
from cocos.text import Label
from cocos.sprite import Sprite
from cocos.actions import *
from cocos.scenes.transitions import *
from pyglet.window import key

keyboard = key.KeyStateHandler()

class Title(cocos.layer.Layer):
    """This layer displays title in the center."""
    def __init__(self, title):
        super(Title, self).__init__()
        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a cocosnode
        label = cocos.text.Label(title, font_size=64,
                                 anchor_x='center', anchor_y='center')
        w, h = director.get_window_size()
        label.position = (w//2, h//2)
        self.add(label)

class SwitchScene(Layer):
    """This layer allows to switch between different scenes by using the LEFT/RIGHT arrow."""
    is_event_handler = True

    def __init__(self):
        super(SwitchScene, self).__init__()
        self.label = cocos.text.Label('Switch scenes with cmd+LEFT/RIGHT')
        self.label.position = (10, 10)
        self.add(self.label)
        self.scenes = []
        self.index = 0

    def on_key_press(self, k, mod):
        """Switch between scenes."""
        d = {key.LEFT:-1, key.RIGHT:+1}
        if k in d and mod & key.MOD_COMMAND:
            self.index += d[k]
            self.index %= len(self.scenes)
            scene = self.scenes[self.index]
            cocos.director.director.replace(scene)

class TitleStatus(cocos.layer.Layer):
    """Define a new layer class to display a title and status line"""
    def __init__(self, *args, **kwargs):
        super(TitleStatus, self).__init__(*args, **kwargs)
        w, h = director.get_window_size()
        self.title = cocos.text.Label('Title', font_size=24)
        self.title.position = (10, h-30)
        self.add(self.title)
        self.status = cocos.text.Label('Status message', position=(10, 10))
        self.add(self.status)
        self.body = cocos.text.Label('Body\ntext', x=10, y=300, multiline=True, width=600)
        self.add(self.body)


class ListMenu(cocos.layer.Layer):
    """Define a scrollable menu based on an items list. 
    Use UP/DOWN arrows to select and ENTER to execute a callback (cb) function.
    """
    is_event_handler = True

    def __init__(self, items, title=None, *args, **kwargs):
        super(ListMenu, self).__init__(*args, **kwargs)
        self.items = items
        self.labels = []
        self.index = 0
        w, h = director.get_window_size()
        if title == None:
            title = 'List Menu' 
        self.title = Label(title, font_size=24, bold=True, position=(10, h-30))
        self.add(self.title)

        # Create labels for each item in the list
        x, y, dy = 10, h-60, -20
        for item in items:
            label = Label(item, position=(x, y))
            y += dy
            self.add(label)
            self.labels.append(label)

        # Make the selected item bold
        self.labels[self.index].element.bold = True
    
    def on_key_press(self, k, mod):
        d = {key.UP:-1, key.DOWN:1}
        if k in d:
            self.labels[self.index].element.bold = False
            self.index += d[k]
            self.index %= len(self.items)
            self.labels[self.index].element.bold = True
        if k== key.ENTER:
            self.cb(self.items[self.index])

    def cb(self, val):
        print(val)


class SwitchLayer(MultiplexLayer):
    """Returns a MultiplexLayer and permits switching with LEFT/RIGHT arrows."""
    is_event_handler = True

    def __init__(self, *layers):
        super(SwitchLayer, self).__init__(*layers)
        self.index = 0
        self.label = Label('Switch layers with LEFT/RIGHT')
        self.label.position = (10, 30)
        self.add(self.label, z=1)

    def on_key_press(self, k, mod):
        d = {key.LEFT:-1, key.RIGHT:1}
        if k in d:
            self.index += d[k]
            self.index %= len(self.layers)
            self.switch_to(self.index)
            layer = self.layers[self.index] 
            # print(layer.__class__)
            # print(layer.__doc__)


actions = [
    'Rotate(360, 1)',
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
    'FadeOut(1)',
]

class ActionMenu(ListMenu):
    def __init__(self, list, *args, **kwargs):
        super(ActionMenu, self).__init__(list, title='Actions', *args, *kwargs)
        self.sprite = cocos.sprite.Sprite('animals/cat-icon.png')
        self.sprite.position = 320, 240
        self.add(self.sprite)
    
    def cb(self, val):
        self.sprite.do(eval(val))

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.sprite.position = director.get_virtual_coordinates(x, y)


effects = [
    'Twirl(grid=(16, 12), duration=4)',
    'Lens3D(grid=(32, 24), duration=5)',
    'Waves(grid=(16, 12), duration=4)',
    'Liquid(grid=(16, 24), duration=5)',
    'Waves3D(waves=5, amplitude=40, grid=(16,16), duration=4)',
    'FlipX3D(duration=3)',
    'FlipY3D(duration=3)',
    'Shaky3D(randrange=6, grid=(4,4), duration=5)',
    'Ripple3D(center=(320,240), radius=240, waves=15, amplitude=60, duration=5, grid=(32,24))',   
]

class EffectMenu(ListMenu):
    def __init__(self, list, *args, **kwargs):
        super(EffectMenu, self).__init__(list, title='Effects', *args, *kwargs)
        self.sprite = cocos.sprite.Sprite('animals/cat-icon.png')
        self.sprite.position = 400, 300
        self.sprite.scale = 2
        self.add(self.sprite)
    
    def cb(self, val):
        print(val)
        self.do(eval(val))


transitions = [
    'RotoZoomTransition',
    'JumpZoomTransition',
    'SplitColsTransition',
    'SplitRowsTransition',
    'MoveInLTransition',
    'MoveInRTransition',
    'MoveInBTransition',
    'MoveInTTransition',
    'SlideInLTransition',
    'SlideInRTransition',
    'SlideInBTransition',
    'SlideInTTransition',
    'FlipX3DTransition',
    'FlipY3DTransition',
    'FlipAngular3DTransition',
    'ShuffleTransition',
    'ShrinkGrowTransition',
    'CornerMoveTransition',
    'EnvelopeTransition',
    'FadeTRTransition',
    'FadeBLTransition',
    'FadeUpTransition',
    'FadeDownTransition',
    'TurnOffTilesTransition',
    'FadeTransition',
    'ZoomTransition',
]

class TransitionMenu(ListMenu):
    def __init__(self, list, *args, **kwargs):
        super(TransitionMenu, self).__init__(list, title='Transitions', *args, *kwargs)

        # Define three different sprites
        s0 = Sprite('animals/cow-icon.png', position=(400, 300), scale=2)
        s1 = Sprite('animals/bird-icon.png', position=(400, 300), scale=2)
        s2 = Sprite('animals/parrot-icon.png', position=(400, 300), scale=2)

        # Define three different scenes
        scene0 = Scene(ColorLayer(100, 0, 0, 255), s0, self)
        scene1 = Scene(ColorLayer(0, 100, 0, 255), s1, self)
        scene2 = Scene(ColorLayer(0, 0, 100, 255), s2, self)
        
        self.scenes = [scene0, scene1, scene2]
        self.scene_index = 0
    
    def cb(self, val):
        self.scene_index += 1
        self.scene_index %= len(self.scenes)
        scene = self.scenes[self.scene_index]
        transition = eval(val)
        director.replace(transition(scene, 1.25))


class Mouse(TitleStatus):
    """This class displays the mouse coordinates in the status line,
on mouse press, the image position is reset to the mouse position."""
    is_event_handler = True     #: enable pyglet's events
    
    def __init__(self):
        super(Mouse, self).__init__()
        self.title.element.text = 'Mouse'
        self.body.element.text = self.__doc__
        self.img = cocos.sprite.Sprite('animals/cat-icon.png')
        self.img.position = 200, 100
        self.add(self.img)

    def on_mouse_motion(self, x, y, dx, dy):
        self.status.element.text = 'mouse motion pos=({}, {}), vec=({}, {})'.format(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.status.element.text = 'mouse drag pos=({}, {}), vec=({}, {}), but={}'.format(x, y, dx, dy, buttons)
        self.img.position = (x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.img.position = (x, y)
    
# Imports as usual
from cocos.tiles import load
from cocos.layer import ScrollingManager
from cocos.director import director
from cocos.scene import Scene

class MyMap(ScrollingManager):
    def __init__(self, *args, **kwargs):
        super(ScrollingManager, self).__init__(*args, **kwargs)
        self.map_layer = load("maps/world.tmx")["tiles"]
        self.add(self.map_layer)


class CarDriver(Driver):
    def step(self, dt):
        self.target.rotation += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 100 * dt
        self.target.acceleration = (keyboard[key.UP] - keyboard[key.DOWN]) * 350
        if keyboard[key.SPACE]:
            self.target.speed = 0
        super(CarDriver, self).step(dt)



class CarLayer(ScrollableLayer):
    def __init__(self, *args, **kwargs):
        super(CarLayer, self).__init__(*args, **kwargs)
        self.car = Sprite('img/cars/car.png', position=(200, 100), scale=0.5)
        self.add(self.car)
        self.car.do(CarDriver())


def main():
    director.init(800, 600, resizable=True)
    bg = cocos.layer.ColorLayer(0, 127, 127, 255)
    
    map_layer = load("maps/world.tmx")["tiles"] # cocos.tiles.RectMapLayer
    car_layer = CarLayer()
    scroller = ScrollingManager() # cocos.layer.scrolling.ScrollingManager
    scroller.add(map_layer)
    scroller.add(car_layer)
    print(scroller)

    # main_scene = Scene(ActionMenu(actions))
    main_scene = Scene(TransitionMenu(transitions)) 
    director.run(Scene(scroller))
    # director.run(Scene(MyMap()))

if __name__ == '__main__':
    main()