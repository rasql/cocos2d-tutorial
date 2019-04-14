import cocos

cocos.director.director.init(600, 200)

label = cocos.text.Label('Hello World', font_size=72)
layer = cocos.layer.ColorLayer(255, 0, 255, 255)
layer.add(label)
scene = cocos.scene.Scene(layer)
cocos.director.director.run(scene)