import cocos

cocos.director.director.init()
label = cocos.text.Label('Hello World', font_size=72)
scene = cocos.scene.Scene(label)
cocos.director.director.run(scene)