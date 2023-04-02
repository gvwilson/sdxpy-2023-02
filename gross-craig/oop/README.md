# Building Objects and Classes

Please use the code in start.py as a starting point.

## Changing Objects' Properties

Modify the code so that when we search for a method, we look in the
object before looking in its class (and parent classes) so that if
someone wants to override a method for a particular object (rather than
for an entire class) they can do so.

### Solution

This is implemented in `object_override.py` by passing the object to `find`
rather than the class of the object. Then `find` first searches the methods
in the object. If the desired method is not found, `find` calls
`find_in_class` to search the object's class (followed by the parent classes)
for the method.

## Multiple Inheritance

Modify the code so that a class can have any number of parents.  Create
a simple example to show that this works, either by modifying the code
in start.py or by creating something new.

### Solution

This is implemented in `multiple.py`. The main change is that parent classes are stored in lists and those lists are iterated over in `find_internal` to find a method. This produces a "depth first" method resolution order, exhausting the first specified parent class's parents then moving to the next. Otherwise, everything is the same.

There are some limitations due to an overall lack of scoping by parent class.
Here, overrides are overrides and there's no accessing the parent-defined
values of overridden methods or variables. Thus, if parent class B (called
second in the constructor) overrides a variable needed by one of parent class
A (called first in the constructor)'s methods, that method would stop working
properly. This leaves it up to the programmer to ensure that multiple
inheritance is "compatible."

We test this by mixing `Square` objects and `Colorable` objects to produce `ColorableSquare`s. We check the method resolution order via an `equals` method implemented by `Shape`, `Square`, and `Colorable`. Since `Colorable` is specified first in `ColorableSquare`'s `_parent` property, it is the only way that equality is checked.


## Prototypes

Some languages don't distinguish between objects and classes. Instead,
we clone an existing object to create a new one, and then modify the new
one's properties. Every object remembers what it was cloned from, so
when we look up a method, we look at the chain of clones instead of the
chain of classes. Create a new file prototype.py and write functions
clone(), find(), and call() that do this. Do you find prototypes easier
or harder to understand than classes?

### Solution

This is implemented in `prototype.py`. I think that prototypes are generally
easier to understand and work with on the back-end than classes. There's less
going on in the inner workings and no need to track common class data, but
I do feel like this leads to more book-keeping on the front-end. 

For example, creating the `sq` and `ci` prototypes is kind of messy, and in
practice, my first instinct was to write a constructor for them. I'm sure
that there's a more effective, prototype-y way to do this, but I feel like
I would just end up re-implementing a class-based design by hand. 

I learned OOP using Java, so the free-flowing nature of prototyping here goes
against my very safety-oriented, statically-typed nature. I imagine that the
more templated nature of classes would help me better organize my thoughts as
well, but again, this is probably because I'm more used to class-based
design.
