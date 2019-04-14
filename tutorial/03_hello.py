import cocos

# sub-class a layer
class HelloWorld(cocos.layer.ColorLayer):
    """Create a new layer by sub-classing Layer."""
    
    # define the constructor function
    def __init__(self):
        # call the parent constructor
        super(HelloWorld, self).__init__(127, 127, 0, 255)
        # create a Label object
        label = cocos.text.Label('Hello World', font_size=72)
        # add the label to the layer
        self.add(label)

cocos.director.director.init(600, 200)
scene = cocos.scene.Scene(HelloWorld())
cocos.director.director.run(scene)