Creating documentation
======================

This document is created with sphinx.
In order to recreate it at your place, you have to clone

* clone the repository
* open a terminal
* change to the **docs** folder

Execute this commands::

    cd docs
    make html

This compiles the documentation and places the output into
the ``_build`` folder.

Doctest blocks
--------------

>>> print('hello')
hello

>>> 1 + 2
3

Footnotes
---------
This is a footnote reference [1]_.

Autonumbered footnotes are possible, like using [#]_ and [#]_.

.. [1] A numerical footnote.
.. [#] This is the first one.
.. [#] This is the second one.

External hyperlinks, like Cocos2D_.

.. _Cocos2D: http://python.cocos2d.org/doc/programming_guide/index.html



.. image:: ../screenshot-1554464788.png

