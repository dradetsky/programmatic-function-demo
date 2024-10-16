Python Programmatic Function Definition Example
===============================================

Many people are familiar with programmatic definition of types in Python using
`type(name, bases, attrs)`. But programmatic defition of functions is somewhat
more obscure. No doubt this is because it's not officially supported.

It's probably a dumb idea to use this on critical code, but you may have a
special use-case for this sort of fancy tricks.

Usage
-----

`python demo.py`

Only stdlib is used, so this should work out of the box.

As of now, I have only tested this with Python 3.12.6.

Why Tho?
--------

I originally learned this stuff in the context of compiling my own programming
languages into Python (for reasons of simplicity, not efficiency or practical
utility). I then made some examples for anyone who wanted to copy/adapt them
(rather than having to experiment yourself).
