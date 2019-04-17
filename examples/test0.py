# display a sprite
import cocos
import pyglet

img = pyglet.resource.image('../animals/cow-icon.png')
sprite = cocos.sprite.Sprite(img)
scene = cocos.scene.Scene()
scene.add(sprite)

cocos.director.director.init()
cocos.director.run(scene)