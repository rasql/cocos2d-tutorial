import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import ColorLayer
from cocos.text import Label
from cocos.sprite import Sprite
from cocos.actions import *
from cocos.scenes.transitions import *
from pyglet.window import key

class TitleStatus(cocos.layer.Layer):
    """Define a new layer class to display a title and status line"""
    def __init__(self):
        super(TitleStatus, self).__init__()
        self.title = cocos.text.Label('Title', font_size=24, x=10, y=400)
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

    def __init__(self, items, *args, **kwargs):
        super(ListMenu, self).__init__(*args, **kwargs)
        self.items = items
        self.labels = []
        self.index = 0

        # Create labels for each item in the list
        x, y, dy = 10, 50, 20
        for item in items:
            label = Label(item, position=(x, y))
            y += dy
            self.add(label)
            self.labels.append(label)

        # Make the selected item bold
        self.labels[self.index].element.bold = True
    
    def on_key_press(self, k, mod):
        d = {key.UP:1, key.DOWN:-1}
        if k in d:
            self.labels[self.index].element.bold = False
            self.index += d[k]
            self.index %= len(self.items)
            self.labels[self.index].element.bold = True
        if k== key.ENTER:
            self.cb(self.items[self.index])

    def cb(self, val):
        print(val)


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
        super(ActionMenu, self).__init__(list, *args, *kwargs)
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
        super(EffectMenu, self).__init__(list, *args, *kwargs)
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
        super(TransitionMenu, self).__init__(list, *args, *kwargs)

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
    

def main():
    director.init(800, 600, resizable=True)
    bg = cocos.layer.ColorLayer(0, 127, 127, 255)
    
    #main_scene = cocos.scene.Scene(ActionMenu(actions))
    main_scene = cocos.scene.Scene(bg, TransitionMenu(transitions))
    director.run(main_scene)

if __name__ == '__main__':
    main()