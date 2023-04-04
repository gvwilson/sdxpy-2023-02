# Building Objects and Classes

Please use the code in start.py as a starting point.

## Changing Objects' Properties

Modify the code so that when we search for a method, we look in the
object before looking in its class (and parent classes) so that if
someone wants to override a method for a particular object (rather than
for an entire class) they can do so.

> Done ✔

## Multiple Inheritance

Modify the code so that a class can have any number of parents.  Create
a simple example to show that this works, either by modifying the code
in start.py or by creating something new.

> Done ✔

## Prototypes

Some languages don't distinguish between objects and classes. Instead,
we clone an existing object to create a new one, and then modify the new
one's properties. Every object remembers what it was cloned from, so
when we look up a method, we look at the chain of clones instead of the
chain of classes. Create a new file prototype.py and write functions
clone(), find(), and call() that do this. Do you find prototypes easier
or harder to understand than classes?

> Not enough time, bowwing out for now. 🙇‍♂️

> Obviously new clones would need to carry a historical record of where they came from. I don't know whether this should be a list that keeps getting bigger or something else. But I'm probably close to it with the idea of parents being a list of objects in itself. I guess we'd just make the list get bigger referencing each object that came before it.
