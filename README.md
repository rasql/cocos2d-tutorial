# Cocos2d Tutorial

Developing games with cocos2d

Cocos2D is a game development platform.

It uses a hierachy of classes

* __Director__ - there is only one director. The director is running scenes
* __Scene__ - there can be multiple scenes, but at any one time only one scene is running
* __Layers__ - a scene can be composed of multiple layers
* __Sprites__ - sprites are animated images which can be part of a layer

## Hello world

To create a simple application we have to:

* import the cocos framework
* initialize the **director**
* create an object (layer, label, sprite, etc.)
* add the object to a **scene**
* let the director run the scene

This is the code to make this basic application which displays 'Hello World' inside a window.

    import cocos

    cocos.director.director.init()
    label = cocos.text.Label('Hello World', font_size=72)
    scene = cocos.scene.Scene(label)
    cocos.director.director.run(scene)

## Built-in commands

* cmd+I opens the interpreter shell
* cmd+S takes a screen capture
* cmd+P pauses the screen
* cmd+F toggle to full screen
* cmd+X toggle FPS display
* cmd+W toggle wire-frame

## The built-in interpreter

![interpreter]('screenshot-1554228960.png')

## Installing Python modules within the Anaconda environment

* Install the Anaconda Distribution (https://www.anaconda.com/distribution/)
* Install VS Code from within Anconda (this installs automatically the Python extensions)
* Launch VS Code
* Select the /anaconda/bin/python3 environment ('base': conda)

Install Cocos2D for the user only

    pip install --user cocos2d

Run platformer.py

## To do

* Object attribute editor (Sprite, Layer, etc.)
* Particle systems demo
* Breaking Flappy Bird into parts (bird, walls, score)
* Add OpenGL primitives (Lines, Recangle)
* Save screenshots
* Add screenshots to the documentation
* Place the documentation on ReadTheDocs
* Add board games (memory, nurikabe, snake)