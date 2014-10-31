
ABOUT
=====

This "Next Generation" library is not intended to replace all the various configuration libraries out there, only mine. I had a very old module that I created way back in the 1.5 or 2.0 days, when the place to go for Python libraries was the old Vaults of Parnassus. There are many good choices now, but none of them seemed like the right fit for me, and certainly wouldn't work with my existing configurations. The old library had many deficiencies, and cried out for a thorough refactoring. I have finally answered this call.

There may be some remarks that are not, as yet, well translated for a wider audience, being originally intended for my own reference. I am working through the package to remedy this. Sorry about the mess!


SUMMARY
=======

Containers are all lists until they are out of scope. then a new container of
the intended type is constructed from the list. this is necessary to support
immutable containers, but it means no complaining about unhashable set elements
or other incompatible elements until the end.

Concepts
--------

immutable
(configuration) container/tree
item
type
declared
defined
command
(un)ordered
validate/convert


children are defined by a command, %dict or %odict. they maybe inline or
external. an inline child begins with an open brace at the end of the line
started by the dict or odict, and ends with a close brace on a line by itself.
an externally defined child has a filename to load, as though included.


Tips and Tricks
---------------
Containers can't contain containers, but items may be anything your custom validator can parse.

Containers with mixed type elements are possible, but a custom type is needed
that can validate them all. obviously, one needs to conform to the rules of the
underlying container. for instance, all elements of a set must be hashable.

replacing types is allowed, but existing references to the previous type will persist,
unless it's refetched at every call, or some explicit updating mechanism is included.

Enforced limitations
--------------------

not a class interface. all customizations are global.

requires Python 2.7

three-space indents!

no containers in containers

TODO
====

external dependencies!
- do_string
- make_grid

unit tests
- test lists of dictionaries
- test multiline items
- use parser on a stream
- added untyped items

perhaps the parser could be generated automagically from some syntax definition
