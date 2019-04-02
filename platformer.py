import cocos
import pyglet
import math
from pyglet.window import key

from cocos import layer, tiles, mapcolliders
from cocos.director import director
from cocos.layer import Layer, ColorLayer, ScrollableLayer, ScrollingManager, PythonInterpreterLayer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.actions import * # Driver, ScaleTo, Move, WrappedMove, BoundedMove
from cocos.actions import RandomDelay
from mylib import Title, SwitchScene, SwitchLayer


class DriveCar(Driver):
    """Action class to drive a car-type vehicle."""
    def step(self, dt):
        # handle input and move the car
        self.target.rotation += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 150 * dt
        self.target.acceleration = (keyboard[key.UP] - keyboard[key.DOWN]) * 400
        if keyboard[key.SPACE]: self.target.speed = 0
        super(DriveCar, self).step(dt)
        scroller.set_focus(self.target.x, self.target.y)

class ScrollablePlayer(ScrollableLayer):
    """Define a player for a scrollable Layer."""
    def __init__(self, img, *args, **kwargs):
        super(ScrollablePlayer, self).__init__(*args, **kwargs)
        self.sprite = Sprite(img, position=(200, 100), scale=0.5)
        self.add(self.sprite)
        self.sprite.max_reverse_speed = -100
        self.sprite.max_forward_speed = 200
        self.sprite.do(DriveCar())

class Ball(Layer):
    """Define a moving ball layer."""
    def __init__(self, img, *args, **kwargs):
        super(Ball, self).__init__(*args, **kwargs)
        self.sprite = Sprite(img, position=(200, 100), scale=0.2)
        self.sprite.velocity = (50, 50)
        self.sprite.speed = 20
        self.sprite.rotation = -45
        #self.sprite.do(Move())
        self.sprite.do(WrappedMove(600, 300))
        #self.sprite.do(BoundedMove(600, 300))
        #self.sprite.do(Driver())
        self.sprite.do(RandomWalk(10))
        self.add(self.sprite)

class MyMap(ScrollingManager):
    """Display a map: 'MyMap(map_layer)'.
    Z - zoom
    U - unzoom
    N - back to normal
    mouse press - center map
    """
    is_event_handler = True

    def __init__(self, map_layer, *args, **kwargs):
        super(MyMap, self).__init__(*args, **kwargs)
        self.map = map_layer
        self.add(self.map)
        self.debug = False

    def on_mouse_press(self, x, y, buttons, mod):
        x, y = self.screen_to_world(x, y)
        print(x, y)
        self.set_focus(x, y)

    def on_key_press(self, k, mod):
        if k == key.D:
            self.debug = not self.debug
            self.map.set_debug(self.debug)
            print('debug =', self.debug)
            self.map.set_dirty() # to force a redisplay

        scale = cocos.actions.ScaleBy(0.75, 1)
        if k == key.Z:
            self.do(scale)
        elif k == key.U:
            self.do(Reverse(scale))
        elif k == key.N:
            self.scale = 1

class DriveCar(Driver):
    """Controller for car type of vehicle."""
    def step(self, dt):
        # handle input and move the car
        self.target.rotation += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 150 * dt
        self.target.acceleration = (keyboard[key.UP] - keyboard[key.DOWN]) * 400
        if keyboard[key.SPACE]: self.target.speed = 0
        super(DriveCar, self).step(dt)
        if isinstance(self.target.parent.parent, ScrollingManager):
            self.target.parent.parent.set_focus(*self.target.position)

class MoveShip(cocos.actions.Move):
    """Controller for spaceship type of vehicle."""
    global keyboard

    def step(self, dt):
        super(MoveShip, self).step(dt)
        self.target.dr = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 360
        angle = math.radians(self.target.rotation)
        ax = math.cos(angle) * 200
        ay = math.sin(angle) * 200
        if keyboard[key.UP]:
            self.target.acceleration = ax, ay
        print('step', self.target.dr, ax, ay, keyboard)

class Player(Layer):
    """
    Define a player for a normal Layer. 
    Use the arrow keys to change velocity
    - N : position = (0, 0), velocity = (0, 0)
    - up/down : modify y velocity
    - left/right : modify x velocity
    """
    is_event_handler = True

    def __init__(self, img, driver=None, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        w, h = director.get_window_size()

        self.status = cocos.text.Label('Status')
        self.status.position = (10, 50)
        self.add(self.status)

        self.sprite = Sprite(img, position=(w//2, h//2), scale=0.5)
        self.sprite.velocity = [10, 10]
        self.sprite.max_reverse_speed = -100
        self.sprite.max_forward_speed = 200
        if driver == None:
            driver = cocos.actions.Move()
        self.sprite.do(driver)
        self.add(self.sprite)

    def on_key_press(self, k, mod):
        w, h = director.get_window_size()
        vx, vy = self.sprite.velocity

        if k == key.N:
            self.sprite.position = w // 2, h // 2
            vx, vy = 0, 0
        elif k == key.RIGHT:
            vx += 10
        elif k == key.LEFT:
            vx -= 10
        elif k == key.UP:
            vy += 10
        elif k == key.DOWN:
            vy -= 10     
        self.sprite.velocity = vx, vy

    def on_draw(self):
        self.status.element.text = 'pos=({:.0f}, {:.0f})'.format(self.sprite.x, self.sprite.y)

class MyWitchController(cocos.actions.Action):
    """Control the player movement (left/right and jump)."""
    on_ground = True
    MOVE_SPEED = 300
    JUMP_SPEED = 800
    GRAVITY = -1200

    def start(self):
        self.target.velocity = (0, 0)

    def step(self, dt):
        global keyboard

        vx, vy = self.target.velocity
        vx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.MOVE_SPEED
        vy += self.GRAVITY * dt
        if self.on_ground and keyboard[key.SPACE]:
            vy = self.JUMP_SPEED

        dx = vx * dt
        dy = vy * dt

        last = self.target.get_rect()
        new = last.copy()
        new.x += dx
        new.y += dy

        self.target.velocity = self.target.collision_handler(last, new, vx, vy)

        self.on_ground = (new.y == last.y)
        self.target.position = new.center
        self.target.parent.parent.set_focus(*new.center)

class MyWitch(Layer):
    """Simple platformer example with walls, decoration and a player.
    - Left/right : move the player
    - Space : jump
    """
    def __init__(self, *args, **kwargs):
        super(MyWitch, self).__init__(*args, **kwargs)

        # add a background layer
        self.add(ColorLayer(100, 100, 100, 255))

        scroller = ScrollingManager()
        
        self.fullmap = cocos.tiles.load('maps/platformer-map.xml')

        # add the walls (labyrinth)
        self.walls = self.fullmap['walls']
        scroller.add(self.walls, z=0)

        # add the items (bushes cauldron)
        self.decoration = self.fullmap['decoration']
        scroller.add(self.decoration, z=1)

        # add the player
        player_layer = layer.ScrollableLayer()
        self.player = cocos.sprite.Sprite('img/witch-standing.png')
        self.player.do(MyWitchController())
        player_layer.add(self.player)
        scroller.add(player_layer, z=2)
        self.add(scroller)

        # set the player start position using the player_start token from the map
        start = self.decoration.find_cells(player_start=True)[0]
        r = self.player.get_rect()
        r.midbottom = start.midbottom
        self.player.position = r.center

        # give a collision handler to the player
        mapcollider = cocos.mapcolliders.RectMapCollider(velocity_on_bump='slide')
        self.player.collision_handler = mapcolliders.make_collision_handler(
            mapcollider, self.walls)

class MyRoad(MyMap):
    """Car driving on a tiled map.
    - Left/right : steering
    - Up/down : accelerate/decelerate
    - Space : brake
    - Z/U : zoom
    - N : normal
    - D : Display debug info
    """
    def __init__(self):
        super(MyRoad, self).__init__(cocos.tiles.load('maps/road-map.xml')['map0'])
        self.add(ScrollablePlayer('img/cars/taxi.png'))

if __name__ == '__main__':
    director.init(800, 600, resizable=True)
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    # create the scene switch layer
    switch_layer = SwitchScene()    

    # place all scenes in a scene list
    scenes = [
        Scene(Title('Platformer demo'), switch_layer),
        Scene(MyWitch(), switch_layer),
        Scene(MyRoad(), switch_layer),
        Scene(Player('img/rocket.png'), switch_layer),
        Scene(MyMap(cocos.tiles.load('maps/world.tmx')['tiles']), switch_layer),
        Scene(ScrollablePlayer('img/rocket.png'), switch_layer),
        Scene(ScrollablePlayer('img/cars/truck.png'), switch_layer),        
        ]

    # give the scene list to the switch layer
    switch_layer.scenes = scenes
    director.run(scenes[0]) 
