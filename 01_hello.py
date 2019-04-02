import cocos
from cocos.actions import *

cocos.director.director.init()
label = cocos.text.Label('Hello world.', font_size=36, position=(320, 240))
label.do(Rotate(360, 10))

dog = cocos.sprite.Sprite('animals/dog-icon.png', position=(100, 100))
cat = cocos.sprite.Sprite('animals/cat-icon.png', position=(300, 200))

layer = cocos.layer.ColorLayer(0, 255, 0, 255)

label.add(dog)

scene = cocos.scene.Scene(cat, layer, cat, label.add(dog))

cocos.director.director.run(scene)