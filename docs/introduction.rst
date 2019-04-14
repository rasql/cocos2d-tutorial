Introduction
============

Cocos2D is a platform for creating games.

Hello world
-----------

We begin this tutorial with the traditional *Hello World* program. This program

* imports the module Cocos2D
* initializes the module,
* creates a label,
* adds this lable to a layer,
* adds this layer to a scene, and finally
* runs the scene.

Create a layer
--------------

Type this code in a new file::

    import cocos

    cocos.director.director.init(600, 200)
    layer = cocos.layer.ColorLayer(0, 255, 0, 255)
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)

.. image:: img/hello1.png

Create a label
--------------

Create a ``Label`` object and add it to the color layer::

    import cocos

    cocos.director.director.init(600, 200)

    label = cocos.text.Label('Hello World', font_size=72)
    layer = cocos.layer.ColorLayer(255, 0, 0, 255)
    layer.add(label)
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)

This is the result:

.. image:: img/hello2.png

Create a class
--------------

In Cocos2D we normally subclass a ``Layer`` to create
a new custom layer::

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

This is the result:

.. image:: img/hello3.png
