=====
Usage
=====

Import the ``takes`` decorator::

    from takes import takes


Example data class
------------------

For the following examples, we will assume that our functions
are accepting a simple dict, representing a point with X and Y coordinates::

    {"x": 1, "y": 1}

We will replace that dict with the following class::

    from dataclasses import dataclass

    @dataclass
    class Point:
        x: int
        y: int

Note that our replacement class does not have to be a ``dataclass``,
any class which accepts the keys from our example dict as keyword arguments
to its ``__init__`` method will do.

Convert the first positional argument
-------------------------------------

The simplest use case only requires us to specify the replacement type::

    @takes(Point)
    def my_function(point):
        x, y = point.x, point.y


Specfiying an argument to convert, by name
------------------------------------------

In case the argument to convert is not the first positional argument,
specify the argument to convert by name::

    @takes(Point, name="point")
    def transform(delta: int, point: Point) -> Point:
        return Point(x=point.x + delta, y=point.y + delta)

Convert multiple arguments
--------------------------

To convert multiple arguments, simply stack decorators::

    @takes(Point, name="p1")
    @takes(Point, name="p2")
    def calculate_distance(p1, p2):
        ...


Stacking with other decorators
------------------------------

Most of the time, ``takes`` should be applied first (closest to the decorated function)::

    @cache
    @takes(Point)
    def my_function(point):
        ...


Takes requires the tuple returned by ``inspect.getfullargspec`` to be
correct. Most decorators don't correctly preserve the signature of the
decorated function - ``functools.wraps`` preserves the signature description
returned by ``help()``, but not ``getfullargspec``.


Handling additional data values
-------------------------------

When converting a dictionary, ``takes`` passes the entire dict
to the target class's constructor. Vanilla python classes will
throw an error when given unexpected keyword arguments.

Takes provides no mechanism for stripping out extra values, it is up
to the target class to ignore them. One option is to use Pydantic_, which
will ignore extra arguments by default.

.. _Pydantic: https://pydantic-docs.helpmanual.io/usage/model_config/
