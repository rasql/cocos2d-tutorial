import cocos
from cocos.director import director

import pyglet
from pyglet.window import key

def center():
    w, h = director.get_window_size()
    return (w//2, h//2)

class GameOver(cocos.layer.Layer):
    def __init__(self):
        super(GameOver, self).__init__()
        self.add(cocos.text.Label('Game Over', font_size=72, position=center(),
            anchor_x='center', anchor_y='center'))
   

class Ball(cocos.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__('img/baseball.png', scale=0.2)

    def update(self, dt):
        pass


class Pong(cocos.layer.Layer):
    """Implements a pong arcade game."""

    is_event_handler = True

    def __init__(self):
        super(Pong, self).__init__()
        w, h = director.get_window_size()
        self.add(cocos.layer.ColorLayer(20, 20, 20, 255))
        
        self.score = 0
        self.label = cocos.text.Label('0', font_size=36, position=(100, h-100))
        self.add(self.label)

        self.sound = pyglet.resource.media('bullet.wav', streaming=False)

        w, h = director.get_window_size()
        ball = cocos.sprite.Sprite('img/baseball.png', scale=0.2)
        ball.position = w//2, h//2
        ball.dx = 100
        ball.dy = 100

        r = ball.get_rect()
        self.add(ball)
        self.ball = ball
    
        pad = cocos.layer.ColorLayer(255, 0, 0, 127)
        pad.width = 20
        pad.height = 100
        self.pad = pad
        self.add(pad)
        self.schedule(self.update)

    def on_key_press(self, k, mod):
        w, h = director.get_window_size()
        d = {key.UP:+1, key.DOWN:-1}
        if k in d:
            self.pad.y += d[k]*10
        self.pad.y = max(0, min(self.pad.y, h-100))    

    def update(self, dt):
        d = self.ball.width // 2
        w, h = director.get_window_size()
        self.ball.x += self.ball.dx * dt
        self.ball.y += self.ball.dy * dt
        if not (d < self.ball.y < h-d):
            self.ball.dy *= -1
            self.sound.play()
            self.score += 1
            self.label.element.text = str(self.score)
        if self.ball.x > w-d:
            self.ball.dx *= -1
            self.score += 1
            self.label.element.text = str(self.score)
        if self.ball.x < d + 20:
            if self.pad.y < self.ball.y < self.ball.y + 100: 
                self.ball.dx *= -1
                self.sound.play()
            else:
                gameover = cocos.scene.Scene(GameOver())
                director.replace(gameover)

if __name__ == '__main__':
    cocos.director.director.init(resizable=True, caption='Pong')
    scene = cocos.scene.Scene(Pong())
    cocos.director.director.run(scene)