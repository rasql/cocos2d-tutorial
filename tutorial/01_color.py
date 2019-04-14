import cocos

cocos.director.director.init(600, 200)
layer = cocos.layer.ColorLayer(0, 255, 0, 255)
scene = cocos.scene.Scene(layer)
cocos.director.director.run(scene)