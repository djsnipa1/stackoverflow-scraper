# StackOverflow Top Python Questions


## [What does the yield keyword do?](https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do)

**9996 Votes**, Alex. S.

To understand what `yield` does, you must understand what generators are. And before you can understand generators, you must understand iterables.

### Iterables

When you create a list, you can read its items one by one. Reading its items one by one is called iteration:

```python
>>> mylist = [1, 2, 3]
>>> for i in mylist:
...    print(i)
1
2
3
```

`mylist` is an iterable. When you use a list comprehension, you create a list, and so an iterable:

```python
>>> mylist = [x*x for x in range(3)]
>>> for i in mylist:
...    print(i)
0
1
4
```

Everything you can use "`for... in...`" on is an iterable; `lists`, `strings`, files...
These iterables are handy because you can read them as much as you wish, but you store all the values in memory and this is not always what you want when you have a lot of values.

### Generators

Generators are iterators, a kind of iterable you can only iterate over once. Generators do not store all the values in memory, they generate the values on the fly:

```python
>>> mygenerator = (x*x for x in range(3))
>>> for i in mygenerator:
...    print(i)
0
1
4
```

It is just the same except you used `()` instead of `[]`. BUT, you cannot perform `for i in mygenerator` a second time since generators can only be used once: they calculate 0, then forget about it and calculate 1, and end calculating 4, one by one.

### Yield

`yield` is a keyword that is used like `return`, except the function will return a generator.

```python
>>> def createGenerator():
...    mylist = range(3)
...    for i in mylist:
...        yield i*i
...
>>> mygenerator = createGenerator() # create a generator
>>> print(mygenerator) # mygenerator is an object!
<generator object createGenerator at 0xb7555c34>
>>> for i in mygenerator:
...     print(i)
0
1
4
```

Here it's a useless example, but it's handy when you know your function will return a huge set of values that you will only need to read once.
To master `yield`, you must understand that when you call the function, the code you have written in the function body does not run. The function only returns the generator object, this is a bit tricky :-)
Then, your code will continue from where it left off each time `for` uses the generator.
Now the hard part:
The first time the `for` calls the generator object created from your function, it will run the code in your function from the beginning until it hits `yield`, then it'll return the first value of the loop. Then, each subsequent call will run another iteration of the loop you have written in the function and return the next value. This will continue until the generator is considered empty, which happens when the function runs without hitting `yield`. That can be because the loop has come to an end, or because you no longer satisfy an `"if/else"`.


### Your code explained

Generator:

```python
# Here you create the method of the node object that will return the generator
def _get_child_candidates(self, distance, min_dist, max_dist):

    # Here is the code that will be called each time you use the generator object:

    # If there is still a child of the node object on its left
    # AND if the distance is ok, return the next child
    if self._leftchild and distance - max_dist < self._median:
        yield self._leftchild

    # If there is still a child of the node object on its right
    # AND if the distance is ok, return the next child
    if self._rightchild and distance + max_dist >= self._median:
        yield self._rightchild

    # If the function arrives here, the generator will be considered empty
    # there is no more than two values: the left and the right children
```

Caller:

```python
# Create an empty list and a list with the current object reference
result, candidates = list(), [self]

# Loop on candidates (they contain only one element at the beginning)
while candidates:

    # Get the last candidate and remove it from the list
    node = candidates.pop()

    # Get the distance between obj and the candidate
    distance = node._get_dist(obj)

    # If distance is ok, then you can fill the result
    if distance <= max_dist and distance >= min_dist:
        result.extend(node._values)

    # Add the children of the candidate in the candidate's list
    # so the loop will keep running until it will have looked
    # at all the children of the children of the children, etc. of the candidate
    candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))

return result
```

This code contains several smart parts:

The loop iterates on a list, but the list expands while the loop is being iterated :-) It's a concise way to go through all these nested data even if it's a bit dangerous since you can end up with an infinite loop. In this case, `candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))` exhaust all the values of the generator, but `while` keeps creating new generator objects which will produce different values from the previous ones since it's not applied on the same node.
The `extend()` method is a list object method that expects an iterable and adds its values to the list.

Usually we pass a list to it:

```python
>>> a = [1, 2]
>>> b = [3, 4]
>>> a.extend(b)
>>> print(a)
[1, 2, 3, 4]
```

But in your code, it gets a generator, which is good because:

You don't need to read the values twice.
You may have a lot of children and you don't want them all stored in memory.

And it works because Python does not care if the argument of a method is a list or not. Python expects iterables so it will work with strings, lists, tuples, and generators! This is called duck typing and is one of the reasons why Python is so cool. But this is another story, for another question...
You can stop here, or read a little bit to see an advanced use of a generator:

### Controlling a generator exhaustion


```python
>>> class Bank(): # Let's create a bank, building ATMs
...    crisis = False
...    def create_atm(self):
...        while not self.crisis:
...            yield "$100"
>>> hsbc = Bank() # When everything's ok the ATM gives you as much as you want
>>> corner_street_atm = hsbc.create_atm()
>>> print(corner_street_atm.next())
$100
>>> print(corner_street_atm.next())
$100
>>> print([corner_street_atm.next() for cash in range(5)])
['$100', '$100', '$100', '$100', '$100']
>>> hsbc.crisis = True # Crisis is coming, no more money!
>>> print(corner_street_atm.next())
<type 'exceptions.StopIteration'>
>>> wall_street_atm = hsbc.create_atm() # It's even true for new ATMs
>>> print(wall_street_atm.next())
<type 'exceptions.StopIteration'>
>>> hsbc.crisis = False # The trouble is, even post-crisis the ATM remains empty
>>> print(corner_street_atm.next())
<type 'exceptions.StopIteration'>
>>> brand_new_atm = hsbc.create_atm() # Build a new one to get back in business
>>> for cash in brand_new_atm:
...    print cash
$100
$100
$100
$100
$100
$100
$100
$100
$100
...
```

Note: For Python 3, use`print(corner_street_atm.__next__())` or `print(next(corner_street_atm))`
It can be useful for various things like controlling access to a resource.

### Itertools, your best friend

The itertools module contains special functions to manipulate iterables. Ever wish to duplicate a generator?
Chain two generators? Group values in a nested list with a one-liner? `Map / Zip` without creating another list?
Then just `import itertools`.
An example? Let's see the possible orders of arrival for a four-horse race:

```python
>>> horses = [1, 2, 3, 4]
>>> races = itertools.permutations(horses)
>>> print(races)
<itertools.permutations object at 0xb754f1dc>
>>> print(list(itertools.permutations(horses)))
[(1, 2, 3, 4),
 (1, 2, 4, 3),
 (1, 3, 2, 4),
 (1, 3, 4, 2),
 (1, 4, 2, 3),
 (1, 4, 3, 2),
 (2, 1, 3, 4),
 (2, 1, 4, 3),
 (2, 3, 1, 4),
 (2, 3, 4, 1),
 (2, 4, 1, 3),
 (2, 4, 3, 1),
 (3, 1, 2, 4),
 (3, 1, 4, 2),
 (3, 2, 1, 4),
 (3, 2, 4, 1),
 (3, 4, 1, 2),
 (3, 4, 2, 1),
 (4, 1, 2, 3),
 (4, 1, 3, 2),
 (4, 2, 1, 3),
 (4, 2, 3, 1),
 (4, 3, 1, 2),
 (4, 3, 2, 1)]
```


### Understanding the inner mechanisms of iteration

Iteration is a process implying iterables (implementing the `__iter__()` method) and iterators (implementing the `__next__()` method).
Iterables are any objects you can get an iterator from. Iterators are objects that let you iterate on iterables.
There is more about it in this article about how `for` loops work.

## [Does Python have a ternary conditional operator?](https://stackoverflow.com/questions/394809/does-python-have-a-ternary-conditional-operator)

**5901 Votes**, community-wiki

Yes, it was added in version 2.5. The expression syntax is:

```python
a if condition else b
```

First `condition` is evaluated, then exactly one of either ``a or ``b is evaluated and returned based on the Boolean value of `condition`. If `condition` evaluates to `True`, then ``a is evaluated and returned but ``b is ignored, or else when ``b is evaluated and returned but ``a is ignored.
This allows short-circuiting because when `condition` is true only ``a is evaluated and ``b is not evaluated at all, but when `condition` is false only ``b is evaluated and ``a is not evaluated at all.
For example:

```python
>>> 'true' if True else 'false'
'true'
>>> 'true' if False else 'false'
'false'
```

Note that conditionals are an expression, not a statement. This means you can't use assignment statements or `pass` or other statements within a conditional expression:

```python
>>> pass if False else x = 3
  File "<stdin>", line 1
    pass if False else x = 3
          ^
SyntaxError: invalid syntax
```

You can, however, use conditional expressions to assign a variable like so:

```python
x = a if True else b
```

Think of the conditional expression as switching between two values. It is very useful when you're in a 'one value or another' situation, it but doesn't do much else.
If you need to use statements, you have to use a normal `if` statement instead of a conditional expression.

Keep in mind that it's frowned upon by some Pythonistas for several reasons:

The order of the arguments is different from those of the classic `condition ? a : b` ternary operator from many other languages (such as C, C++, Go, Perl, Ruby, Java, Javascript, etc.), which may lead to bugs when people unfamiliar with Python's "surprising" behaviour use it (they may reverse the argument order).
Some find it "unwieldy", since it goes contrary to the normal flow of thought (thinking of the condition first and then the effects).
Stylistic reasons. (Although the 'inline `if`' can be really useful, and make your script more concise, it really does complicate your code)

If you're having trouble remembering the order, then remember that when read aloud, you (almost) say what you mean. For example, `x = 4 if b > 8 else 9` is read aloud as `x will be 4 if b is greater than 8 otherwise 9`.
Official documentation:     

Conditional expressions
Is there an equivalent of Cs ?: ternary operator?

## [What does if __name__ == __main__: do?](https://stackoverflow.com/questions/419163/what-does-if-name-main-do)

**5891 Votes**, Devoted

Whenever the Python interpreter reads a source file, it does two things:

it sets a few special variables like `__name__`, and then
it executes all of the code found in the file.

Let's see how this works and how it relates to your question about the `__name__` checks we always see in Python scripts.
Code Sample
Let's use a slightly different code sample to explore how imports and scripts work.  Suppose the following is in a file called `foo.py`.

```python
# Suppose this is foo.py.

print("before import")
import math

print("before functionA")
def functionA():
    print("Function A")

print("before functionB")
def functionB():
    print("Function B {}".format(math.sqrt(100)))

print("before __name__ guard")
if __name__ == '__main__':
    functionA()
    functionB()
print("after __name__ guard")
```

Special Variables
When the Python interpeter reads a source file, it first defines a few special variables. In this case, we care about the `__name__` variable.
When Your Module Is the Main Program
If you are running your module (the source file) as the main program, e.g.

```python
python foo.py
```

the interpreter will assign the hard-coded string `"__main__"` to the `__name__` variable, i.e.

```python
# It's as if the interpreter inserts this at the top
# of your module when run as the main program.
__name__ = "__main__" 
```

When Your Module Is Imported By Another
On the other hand, suppose some other module is the main program and it imports your module. This means there's a statement like this in the main program, or in some other module the main program imports:

```python
# Suppose this is in some other main program.
import foo
```

The interpreter will search for your `foo.py` file (along with searching for a few other variants), and prior to executing that module, it will assign the name `"foo"` from the import statement to the `__name__` variable, i.e.

```python
# It's as if the interpreter inserts this at the top
# of your module when it's imported from another module.
__name__ = "foo"
```

Executing the Module's Code
After the special variables are set up, the interpreter executes all the code in the module, one statement at a time. You may want to open another window on the side with the code sample so you can follow along with this explanation.
Always

It prints the string `"before import"` (without quotes).
It loads the `math` module and assigns it to a variable called `math`. This is equivalent to replacing `import math` with the following (note that `__import__` is a low-level function in Python that takes a string and triggers the actual import):


```python
# Find and load a module given its string name, "math",
# then assign it to a local variable called math.
math = __import__("math")
```


It prints the string `"before functionA"`.
It executes the `def` block, creating a function object, then assigning that function object to a variable called `functionA`.
It prints the string `"before functionB"`.
It executes the second `def` block, creating another function object, then assigning it to a variable called `functionB`.
It prints the string `"before __name__ guard"`.

Only When Your Module Is the Main Program

If your module is the main program, then it will see that `__name__` was indeed set to `"__main__"` and it calls the two functions, printing the strings `"Function A"` and `"Function B 10.0"`.

Only When Your Module Is Imported by Another

(instead) If your module is not the main program but was imported by another one, then `__name__` will be `"foo"`, not `"__main__"`, and it'll skip the body of the `if` statement.

Always

It will print the string `"after __name__ guard"` in both situations.

Summary
In summary, here's what'd be printed in the two cases:

```python
# What gets printed if foo is the main program
before import
before functionA
before functionB
before __name__ guard
Function A
Function B 10.0
after __name__ guard
```


```python
# What gets printed if foo is imported as a regular module
before import
before functionA
before functionB
before __name__ guard
after __name__ guard
```

Why Does It Work This Way?
You might naturally wonder why anybody would want this.  Well, sometimes you want to write a `.py` file that can be both used by other programs and/or modules as a module, and can also be run as the main program itself.  Examples:

Your module is a library, but you want to have a script mode where it runs some unit tests or a demo.
Your module is only used as a main program, but it has some unit tests, and the testing framework works by importing `.py` files like your script and running special test functions. You don't want it to try running the script just because it's importing the module.
Your module is mostly used as a main program, but it also provides a programmer-friendly API for advanced users.

Beyond those examples, it's elegant that running a script in Python is just setting up a few magic variables and importing the script. "Running" the script is a side effect of importing the script's module.
Food for Thought

Question: Can I have multiple `__name__` checking blocks?  Answer: it's strange to do so, but the language won't stop you.
Suppose the following is in `foo2.py`.  What happens if you say `python foo2.py` on the command-line? Why?


```python
# Suppose this is foo2.py.

def functionA():
    print("a1")
    from foo2 import functionB
    print("a2")
    functionB()
    print("a3")

def functionB():
    print("b")

print("t1")
if __name__ == "__main__":
    print("m1")
    functionA()
    print("m2")
print("t2")
```


Now, figure out what will happen if you remove the `__name__` check in `foo3.py`:


```python
# Suppose this is foo3.py.

def functionA():
    print("a1")
    from foo3 import functionB
    print("a2")
    functionB()
    print("a3")

def functionB():
    print("b")

print("t1")
print("m1")
functionA()
print("m2")
print("t2")
```


What will this do when used as a script?  When imported as a module?


```python
# Suppose this is in foo4.py
__name__ = "__main__"

def bar():
    print("bar")

print("before __name__ guard")
if __name__ == "__main__":
    bar()
print("after __name__ guard")
```

## [What are metaclasses in Python?](https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python)

**5620 Votes**, e-satis

A metaclass is the class of a class. A class defines how an instance of the class (i.e. an object) behaves while a metaclass defines how a class behaves. A class is an instance of a metaclass.
While in Python you can use arbitrary callables for metaclasses (like Jerub shows), the better approach is to make it an actual class itself. `type` is the usual metaclass in Python. `type` is itself a class, and it is its own type. You won't be able to recreate something like `type` purely in Python, but Python cheats a little. To create your own metaclass in Python you really just want to subclass `type`.
A metaclass is most commonly used as a class-factory. When you create an object by calling the class, Python creates a new class (when it executes the 'class' statement) by calling the metaclass. Combined with the normal `__init__` and `__new__` methods, metaclasses therefore allow you to do 'extra things' when creating a class, like registering the new class with some registry or replace the class with something else entirely.
When the `class` statement is executed, Python first executes the body of the `class` statement as a normal block of code. The resulting namespace (a dict) holds the attributes of the class-to-be. The metaclass is determined by looking at the baseclasses of the class-to-be (metaclasses are inherited), at the `__metaclass__` attribute of the class-to-be (if any) or the `__metaclass__` global variable. The metaclass is then called with the name, bases and attributes of the class to instantiate it.
However, metaclasses actually define the type of a class, not just a factory for it, so you can do much more with them. You can, for instance, define normal methods on the metaclass. These metaclass-methods are like classmethods in that they can be called on the class without an instance, but they are also not like classmethods in that they cannot be called on an instance of the class. `type.__subclasses__()` is an example of a method on the `type` metaclass. You can also define the normal 'magic' methods, like `__add__`, `__iter__` and `__getattr__`, to implement or change how the class behaves.
Here's an aggregated example of the bits and pieces:

```python
def make_hook(f):
    """Decorator to turn 'foo' method into '__foo__'"""
    f.is_hook = 1
    return f

class MyType(type):
    def __new__(mcls, name, bases, attrs):

        if name.startswith('None'):
            return None

        # Go over attributes and see if they should be renamed.
        newattrs = {}
        for attrname, attrvalue in attrs.iteritems():
            if getattr(attrvalue, 'is_hook', 0):
                newattrs['__%s__' % attrname] = attrvalue
            else:
                newattrs[attrname] = attrvalue

        return super(MyType, mcls).__new__(mcls, name, bases, newattrs)

    def __init__(self, name, bases, attrs):
        super(MyType, self).__init__(name, bases, attrs)

        # classregistry.register(self, self.interfaces)
        print "Would register class %s now." % self

    def __add__(self, other):
        class AutoClass(self, other):
            pass
        return AutoClass
        # Alternatively, to autogenerate the classname as well as the class:
        # return type(self.__name__ + other.__name__, (self, other), {})

    def unregister(self):
        # classregistry.unregister(self)
        print "Would unregister class %s now." % self

class MyObject:
    __metaclass__ = MyType


class NoneSample(MyObject):
    pass

# Will print "NoneType None"
print type(NoneSample), repr(NoneSample)

class Example(MyObject):
    def __init__(self, value):
        self.value = value
    @make_hook
    def add(self, other):
        return self.__class__(self.value + other.value)

# Will unregister the class
Example.unregister()

inst = Example(10)
# Will fail with an AttributeError
#inst.unregister()

print inst + inst
class Sibling(MyObject):
    pass

ExampleSibling = Example + Sibling
# ExampleSibling is now a subclass of both Example and Sibling (with no
# content of its own) although it will believe it's called 'AutoClass'
print ExampleSibling
print ExampleSibling.__mro__
```

## [How do I check whether a file exists without exceptions?](https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions)

**5482 Votes**, spence91

If the reason you're checking is so you can do something like `if file_exists: open_it()`, it's safer to use a `try` around the attempt to open it. Checking and then opening risks the file being deleted or moved or something between when you check and when you try to open it.
If you're not planning to open the file immediately, you can use `os.path.isfile`

Return `True` if path is an existing regular file. This follows symbolic links, so both islink() and isfile() can be true for the same path.


```python
import os.path
os.path.isfile(fname) 
```

if you need to be sure it's a file.
Starting with Python 3.4, the `pathlib` module offers an object-oriented approach (backported to `pathlib2` in Python 2.7):

```python
from pathlib import Path

my_file = Path("/path/to/file")
if my_file.is_file():
    # file exists
```

To check a directory, do:

```python
if my_file.is_dir():
    # directory exists
```

To check whether a `Path` object exists independently of whether is it a file or directory, use `exists()`:

```python
if my_file.exists():
    # path exists
```

You can also use `resolve(strict=True)` in a `try` block:

```python
try:
    my_abs_path = my_file.resolve(strict=True)
except FileNotFoundError:
    # doesn't exist
else:
    # exists
```

## [Calling an external command from Python](https://stackoverflow.com/questions/89228/calling-an-external-command-from-python)

**4791 Votes**, freshWoWer

Look at the subprocess module in the standard library:

```python
import subprocess
subprocess.run(["ls", "-l"])
```

The advantage of `subprocess` vs. `system` is that it is more flexible (you can get the `stdout`, `stderr`, the "real" status code, better error handling, etc...).
The official documentation recommends the `subprocess` module over the alternative `os.system()`:

The `subprocess` module provides more powerful facilities for spawning new processes and retrieving their results; using that module is preferable to using this function [`os.system()`].

The Replacing Older Functions with the subprocess Module section in the `subprocess` documentation may have some helpful recipes.
For versions of Python before 3.5, use `call`:

```python
import subprocess
subprocess.call(["ls", "-l"])
```

## [How do I merge two dictionaries in a single expression?](https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression)

**4642 Votes**, Carl Meyer

### How can I merge two Python dictionaries in a single expression?


For dictionaries ``x and ``y, ``z becomes a shallowly merged dictionary with values from ``y replacing those from ``x.

In Python 3.5 or greater:

```python
z = {**x, **y}
```

In Python 2, (or 3.4 or lower) write a function:

```python
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
```

and now:

```python
z = merge_two_dicts(x, y)
```

In Python 3.9.0a4 or greater (final release date approx October 2020): PEP-584, discussed here, was implemented to further simplify this:

```python
z = x | y          # NOTE: 3.9+ ONLY
```


Explanation
Say you have two dicts and you want to merge them into a new dict without altering the original dicts:

```python
x = {'a': 1, 'b': 2}
y = {'b': 3, 'c': 4}
```

The desired result is to get a new dictionary (``z) with the values merged, and the second dict's values overwriting those from the first.

```python
>>> z
{'a': 1, 'b': 3, 'c': 4}
```

A new syntax for this, proposed in PEP 448 and available as of Python 3.5, is 

```python
z = {**x, **y}
```

And it is indeed a single expression. 
Note that we can merge in with literal notation as well:

```python
z = {**x, 'foo': 1, 'bar': 2, **y}
```

and now: 

```python
>>> z
{'a': 1, 'b': 3, 'foo': 1, 'bar': 2, 'c': 4}
```

It is now showing as implemented in the release schedule for 3.5, PEP 478, and it has now made its way into What's New in Python 3.5 document.
However, since many organizations are still on Python 2, you may wish to do this in a backwards compatible way. The classically Pythonic way, available in Python 2 and Python 3.0-3.4, is to do this as a two-step process:

```python
z = x.copy()
z.update(y) # which returns None since it mutates z
```

In both approaches, ``y will come second and its values will replace ``x's values, thus `'b'` will point to ``3 in our final result.

### Not yet on Python 3.5, but want a single expression

If you are not yet on Python 3.5, or need to write backward-compatible code, and you want this in a single expression, the most performant while correct approach is to put it in a function:

```python
def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z
```

and then you have a single expression:

```python
z = merge_two_dicts(x, y)
```

You can also make a function to merge an undefined number of dicts, from zero to a very large number:

```python
def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result
```

This function will work in Python 2 and 3 for all dicts. e.g. given dicts ``a to ``g:

```python
z = merge_dicts(a, b, c, d, e, f, g) 
```

and key value pairs in ``g will take precedence over dicts ``a to ``f, and so on.

### Critiques of Other Answers

Don't use what you see in the formerly accepted answer:

```python
z = dict(x.items() + y.items())
```

In Python 2, you create two lists in memory for each dict, create a third list in memory with length equal to the length of the first two put together, and then discard all three lists to create the dict. In Python 3, this will fail because you're adding two `dict_items` objects together, not two lists - 

```python
>>> c = dict(a.items() + b.items())
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'dict_items' and 'dict_items'
```

and you would have to explicitly create them as lists, e.g. `z = dict(list(x.items()) + list(y.items()))`. This is a waste of resources and computation power. 
Similarly, taking the union of `items()` in Python 3 (`viewitems()` in Python 2.7) will also fail when values are unhashable objects (like lists, for example). Even if your values are hashable, since sets are semantically unordered, the behavior is undefined in regards to precedence. So don't do this:

```python
>>> c = dict(a.items() | b.items())
```

This example demonstrates what happens when values are unhashable:

```python
>>> x = {'a': []}
>>> y = {'b': []}
>>> dict(x.items() | y.items())
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

Here's an example where y should have precedence, but instead the value from x is retained due to the arbitrary order of sets:

```python
>>> x = {'a': 2}
>>> y = {'a': 1}
>>> dict(x.items() | y.items())
{'a': 2}
```

Another hack you should not use:

```python
z = dict(x, **y)
```

This uses the `dict` constructor, and is very fast and memory efficient (even slightly more-so than our two-step process) but unless you know precisely what is happening here (that is, the second dict is being passed as keyword arguments to the dict constructor), it's difficult to read, it's not the intended usage, and so it is not Pythonic. 
Here's an example of the usage being remediated in django.
Dicts are intended to take hashable keys (e.g. frozensets or tuples), but this method fails in Python 3 when keys are not strings.

```python
>>> c = dict(a, **b)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: keyword arguments must be strings
```

From the mailing list, Guido van Rossum, the creator of the language, wrote:

I am fine with
  declaring dict({}, **{1:3}) illegal, since after all it is abuse of
  the ** mechanism.

and 

Apparently dict(x, **y) is going around as "cool hack" for "call
  x.update(y) and return x". Personally I find it more despicable than
  cool.

It is my understanding (as well as the understanding of the creator of the language) that the intended usage for `dict(**y)` is for creating dicts for readability purposes, e.g.:

```python
dict(a=1, b=10, c=11)
```

instead of 

```python
{'a': 1, 'b': 10, 'c': 11}
```


### Response to comments


Despite what Guido says, `dict(x, **y)` is in line with the dict specification, which btw. works for both Python 2 and 3. The fact that this only works for string keys is a direct consequence of how keyword parameters work and not a short-comming of dict. Nor is using the ** operator in this place an abuse of the mechanism, in fact ** was designed precisely to pass dicts as keywords. 

Again, it doesn't work for 3 when keys are non-strings. The implicit calling contract is that namespaces take ordinary dicts, while users must only pass keyword arguments that are strings. All other callables enforced it. `dict` broke this consistency in Python 2:

```python
>>> foo(**{('a', 'b'): None})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: foo() keywords must be strings
>>> dict(**{('a', 'b'): None})
{('a', 'b'): None}
```

This inconsistency was bad given other implementations of Python (Pypy, Jython, IronPython). Thus it was fixed in Python 3, as this usage could be a breaking change.
I submit to you that it is malicious incompetence to intentionally write code that only works in one version of a language or that only works given certain arbitrary constraints.
More comments:

`dict(x.items() + y.items())` is still the most readable solution for Python 2. Readability counts. 

My response: `merge_two_dicts(x, y)` actually seems much clearer to me, if we're actually concerned about readability. And it is not forward compatible, as Python 2 is increasingly deprecated.

`{**x, **y}` does not seem to handle nested dictionaries. the contents of nested keys are simply overwritten, not merged [...] I ended up being burnt by these answers that do not merge recursively and I was surprised no one mentioned it. In my interpretation of the word "merging" these answers describe "updating one dict with another", and not merging.

Yes. I must refer you back to the question, which is asking for a shallow merge of two dictionaries, with the first's values being overwritten by the second's - in a single expression.
Assuming two dictionary of dictionaries, one might recursively merge them in a single function, but you should be careful not to modify the dicts from either source, and the surest way to avoid that is to make a copy when assigning values. As keys must be hashable and are usually therefore immutable, it is pointless to copy them:

```python
from copy import deepcopy

def dict_of_dicts_merge(x, y):
    z = {}
    overlapping_keys = x.keys() & y.keys()
    for key in overlapping_keys:
        z[key] = dict_of_dicts_merge(x[key], y[key])
    for key in x.keys() - overlapping_keys:
        z[key] = deepcopy(x[key])
    for key in y.keys() - overlapping_keys:
        z[key] = deepcopy(y[key])
    return z
```

Usage:

```python
>>> x = {'a':{1:{}}, 'b': {2:{}}}
>>> y = {'b':{10:{}}, 'c': {11:{}}}
>>> dict_of_dicts_merge(x, y)
{'b': {2: {}, 10: {}}, 'a': {1: {}}, 'c': {11: {}}}
```

Coming up with contingencies for other value types is far beyond the scope of this question, so I will point you at my answer to the canonical question on a "Dictionaries of dictionaries merge".

### Less Performant But Correct Ad-hocs

These approaches are less performant, but they will provide correct behavior.
They will be much less performant than `copy` and `update` or the new unpacking because they iterate through each key-value pair at a higher level of abstraction, but they do respect the order of precedence (latter dicts have precedence)
You can also chain the dicts manually inside a dict comprehension:

```python
{k: v for d in dicts for k, v in d.items()} # iteritems in Python 2.7
```

or in python 2.6 (and perhaps as early as 2.4 when generator expressions were introduced):

```python
dict((k, v) for d in dicts for k, v in d.items())
```

`itertools.chain` will chain the iterators over the key-value pairs in the correct order:

```python
import itertools
z = dict(itertools.chain(x.iteritems(), y.iteritems()))
```


### Performance Analysis

I'm only going to do the performance analysis of the usages known to behave correctly. 

```python
import timeit
```

The following is done on Ubuntu 14.04
In Python 2.7 (system Python):

```python
>>> min(timeit.repeat(lambda: merge_two_dicts(x, y)))
0.5726828575134277
>>> min(timeit.repeat(lambda: {k: v for d in (x, y) for k, v in d.items()} ))
1.163769006729126
>>> min(timeit.repeat(lambda: dict(itertools.chain(x.iteritems(), y.iteritems()))))
1.1614501476287842
>>> min(timeit.repeat(lambda: dict((k, v) for d in (x, y) for k, v in d.items())))
2.2345519065856934
```

In Python 3.5 (deadsnakes PPA):

```python
>>> min(timeit.repeat(lambda: {**x, **y}))
0.4094954460160807
>>> min(timeit.repeat(lambda: merge_two_dicts(x, y)))
0.7881555100320838
>>> min(timeit.repeat(lambda: {k: v for d in (x, y) for k, v in d.items()} ))
1.4525277839857154
>>> min(timeit.repeat(lambda: dict(itertools.chain(x.items(), y.items()))))
2.3143140770262107
>>> min(timeit.repeat(lambda: dict((k, v) for d in (x, y) for k, v in d.items())))
3.2069112799945287
```


### Resources on Dictionaries


My explanation of Python's dictionary implementation, updated for 3.6.
Answer on how to add new keys to a dictionary
Mapping two lists into a dictionary
The official Python docs on dictionaries 
The Dictionary Even Mightier - talk by Brandon Rhodes at Pycon 2017
Modern Python Dictionaries, A Confluence of Great Ideas - talk by Raymond Hettinger at Pycon 2017

## [How can I safely create a nested directory?](https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory)

**4139 Votes**, Parand

On Python  3.5, use `pathlib.Path.mkdir`:

```python
from pathlib import Path
Path("/my/directory").mkdir(parents=True, exist_ok=True)
```

For older versions of Python, I see two answers with good qualities, each with a small flaw, so I will give my take on it:
Try `os.path.exists`, and consider `os.makedirs` for the creation.

```python
import os
if not os.path.exists(directory):
    os.makedirs(directory)
```

As noted in comments and elsewhere, there's a race condition  if the directory is created between the `os.path.exists` and the `os.makedirs` calls, the `os.makedirs` will fail with an `OSError`. Unfortunately, blanket-catching `OSError` and continuing is not foolproof, as it will ignore a failure to create the directory due to other factors, such as insufficient permissions, full disk, etc.
One option would be to trap the `OSError` and examine the embedded error code (see Is there a cross-platform way of getting information from Pythons OSError):

```python
import os, errno

try:
    os.makedirs(directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
```

Alternatively, there could be a second `os.path.exists`, but suppose another created the directory after the first check, then removed it before the second one  we could still be fooled. 
Depending on the application, the danger of concurrent operations may be more or less than the danger posed by other factors such as file permissions. The developer would have to know more about the particular application being developed and its expected environment before choosing an implementation.
Modern versions of Python improve this code quite a bit, both by exposing `FileExistsError` (in 3.3+)...

```python
try:
    os.makedirs("path/to/directory")
except FileExistsError:
    # directory already exists
    pass
```

...and by allowing a keyword argument to `os.makedirs` called `exist_ok` (in 3.2+).

```python
os.makedirs("path/to/directory", exist_ok=True)  # succeeds even if directory exists.
```

## [Does Python have a string 'contains' substring method?](https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method)

**3599 Votes**, Blankman

You can use the `in` operator:

```python
if "blah" not in somestring: 
    continue
```

## [Accessing the index in 'for' loops?](https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops)

**3509 Votes**, Joan Venge

Using an additional state variable, such as an index variable (which you would normally use in languages such as C or PHP), is considered non-pythonic.
The better option is to use the built-in function `enumerate()`, available in both Python 2 and 3:

```python
for idx, val in enumerate(ints):
    print(idx, val)
```

Check out PEP 279 for more.

## [Difference between staticmethod and classmethod](https://stackoverflow.com/questions/136097/difference-between-staticmethod-and-classmethod)

**3506 Votes**, Daryl Spitzer

Maybe a bit of example code will help: Notice the difference in the call signatures of `foo`, `class_foo` and `static_foo`:

```python
class A(object):
    def foo(self, x):
        print "executing foo(%s, %s)" % (self, x)

    @classmethod
    def class_foo(cls, x):
        print "executing class_foo(%s, %s)" % (cls, x)

    @staticmethod
    def static_foo(x):
        print "executing static_foo(%s)" % x    

a = A()
```

Below is the usual way an object instance calls a method. The object instance, ``a, is implicitly passed as the first argument.

```python
a.foo(1)
# executing foo(<__main__.A object at 0xb7dbef0c>,1)
```


With classmethods, the class of the object instance is implicitly passed as the first argument instead of `self`.

```python
a.class_foo(1)
# executing class_foo(<class '__main__.A'>,1)
```

You can also call `class_foo` using the class. In fact, if you define something to be
a classmethod, it is probably because you intend to call it from the class rather than from a class instance. `A.foo(1)` would have raised a TypeError, but `A.class_foo(1)` works just fine:

```python
A.class_foo(1)
# executing class_foo(<class '__main__.A'>,1)
```

One use people have found for class methods is to create inheritable alternative constructors.

With staticmethods, neither `self` (the object instance) nor  `cls` (the class) is implicitly passed as the first argument. They behave like plain functions except that you can call them from an instance or the class:

```python
a.static_foo(1)
# executing static_foo(1)

A.static_foo('hi')
# executing static_foo(hi)
```

Staticmethods are used to group functions which have some logical connection with a class to the class.

`foo` is just a function, but when you call `a.foo` you don't just get the function,
you get a "partially applied" version of the function with the object instance ``a bound as the first argument to the function. `foo` expects 2 arguments, while `a.foo` only expects 1 argument.
``a is bound to `foo`. That is what is meant by the term "bound" below:

```python
print(a.foo)
# <bound method A.foo of <__main__.A object at 0xb7d52f0c>>
```

With `a.class_foo`, ``a is not bound to `class_foo`, rather the class ``A is bound to `class_foo`.

```python
print(a.class_foo)
# <bound method type.class_foo of <class '__main__.A'>>
```

Here, with a staticmethod, even though it is a method, `a.static_foo` just returns
a good 'ole function with no arguments bound. `static_foo` expects 1 argument, and
`a.static_foo` expects 1 argument too.

```python
print(a.static_foo)
# <function static_foo at 0xb7d479cc>
```

And of course the same thing happens when you call `static_foo` with the class ``A instead.

```python
print(A.static_foo)
# <function static_foo at 0xb7d479cc>
```

## [How do I list all files of a directory?](https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory)

**3473 Votes**, duhhunjonn

`os.listdir()` will get you everything that's in a directory - files and directories.
If you want just files, you could either filter this down using `os.path`:

```python
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
```

or you could use `os.walk()` which will yield two lists for each directory it visits - splitting into files and dirs for you. If you only want the top directory you can just break the first time it yields

```python
from os import walk

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break
```

## [How do I sort a dictionary by value?](https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value)

**3422 Votes**, Gern Blanston

Python 3.6+

```python
x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
{k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
{0: 0, 2: 1, 1: 2, 4: 3, 3: 4}
```

Older Python
It is not possible to sort a dictionary, only to get a representation of a dictionary that is sorted. Dictionaries are inherently orderless, but other types, such as lists and tuples, are not. So you need an ordered data type to represent sorted values, which will be a listprobably a list of tuples.
For instance,

```python
import operator
x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
sorted_x = sorted(x.items(), key=operator.itemgetter(1))
```

`sorted_x` will be a list of tuples sorted by the second element in each tuple. `dict(sorted_x) == x`.
And for those wishing to sort on keys instead of values:

```python
import operator
x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
sorted_x = sorted(x.items(), key=operator.itemgetter(0))
```

In Python3 since unpacking is not allowed [1] we can use 

```python
x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
sorted_x = sorted(x.items(), key=lambda kv: kv[1])
```

If you want the output as a dict, you can use `collections.OrderedDict`:

```python
import collections

sorted_dict = collections.OrderedDict(sorted_x)
```

## [How to make a flat list out of list of lists?](https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists)

**3247 Votes**, Emma

Given a list of lists ``l,
`flat_list = [item for sublist in l for item in sublist]`
which means:

```python
flat_list = []
for sublist in l:
    for item in sublist:
        flat_list.append(item)
```

is faster than the shortcuts posted so far. (``l is the list to flatten.)
Here is the corresponding function:

```python
flatten = lambda l: [item for sublist in l for item in sublist]
```

As evidence, you can use the `timeit` module in the standard library:

```python
$ python -mtimeit -s'l=[[1,2,3],[4,5,6], [7], [8,9]]*99' '[item for sublist in l for item in sublist]'
10000 loops, best of 3: 143 usec per loop
$ python -mtimeit -s'l=[[1,2,3],[4,5,6], [7], [8,9]]*99' 'sum(l, [])'
1000 loops, best of 3: 969 usec per loop
$ python -mtimeit -s'l=[[1,2,3],[4,5,6], [7], [8,9]]*99' 'reduce(lambda x,y: x+y,l)'
1000 loops, best of 3: 1.1 msec per loop
```

Explanation: the shortcuts based on ``+ (including the implied use in `sum`) are, of necessity, `O(L**2)` when there are L sublists -- as the intermediate result list keeps getting longer, at each step a new intermediate result list object gets allocated, and all the items in the previous intermediate result must be copied over (as well as a few new ones added at the end). So, for simplicity and without actual loss of generality, say you have L sublists of I items each: the first I items are copied back and forth L-1 times, the second I items L-2 times, and so on; total number of copies is I times the sum of x for x from 1 to L excluded, i.e., `I * (L**2)/2`.
The list comprehension just generates one list, once, and copies each item over (from its original place of residence to the result list) also exactly once.

## [How do I check if a list is empty?](https://stackoverflow.com/questions/53513/how-do-i-check-if-a-list-is-empty)

**3234 Votes**, Ray

```python
if not a:
  print("List is empty")
```

Using the implicit booleanness of the empty `list` is quite pythonic.

## [Understanding slice notation](https://stackoverflow.com/questions/509211/understanding-slice-notation)

**3199 Votes**, Simon

It's pretty simple really:

```python
a[start:stop]  # items start through stop-1
a[start:]      # items start through the rest of the array
a[:stop]       # items from the beginning through stop-1
a[:]           # a copy of the whole array
```

There is also the `step` value, which can be used with any of the above:

```python
a[start:stop:step] # start through not past stop, by step
```

The key point to remember is that the `:stop` value represents the first value that is not in the selected slice. So, the difference between `stop` and `start` is the number of elements selected (if `step` is 1, the default).
The other feature is that `start` or `stop` may be a negative number, which means it counts from the end of the array instead of the beginning. So:

```python
a[-1]    # last item in the array
a[-2:]   # last two items in the array
a[:-2]   # everything except the last two items
```

Similarly, `step` may be a negative number:

```python
a[::-1]    # all items in the array, reversed
a[1::-1]   # the first two items, reversed
a[:-3:-1]  # the last two items, reversed
a[-3::-1]  # everything except the last two items, reversed
```

Python is kind to the programmer if there are fewer items than you ask for. For example, if you ask for `a[:-2]` and ``a only contains one element, you get an empty list instead of an error. Sometimes you would prefer the error, so you have to be aware that this may happen.
Relation to `slice()` object
The slicing operator `[]` is actually being used in the above code with a `slice()` object using the ``: notation (which is only valid within `[]`), i.e.:

```python
a[start:stop:step]
```

is equivalent to:

```python
a[slice(start, stop, step)]
```

Slice objects also behave slightly differently depending on the number of arguments, similarly to `range()`, i.e. both `slice(stop)` and `slice(start, stop[, step])` are supported.
To skip specifying a given argument, one might use `None`, so that e.g. `a[start:]` is equivalent to `a[slice(start, None)]` or `a[::-1]` is equivalent to `a[slice(None, None, -1)]`.
While the ``:-based notation is very helpful for simple slicing, the explicit use of `slice()` objects simplifies the programmatic generation of slicing.

## [What is the difference between Python's list methods append and extend?](https://stackoverflow.com/questions/252703/what-is-the-difference-between-pythons-list-methods-append-and-extend)

**3116 Votes**, Claudiu

`append`: Appends object at the end.

```python
x = [1, 2, 3]
x.append([4, 5])
print (x)
```

gives you: `[1, 2, 3, [4, 5]]`

`extend`: Extends list by appending elements from the iterable.

```python
x = [1, 2, 3]
x.extend([4, 5])
print (x)
```

gives you: `[1, 2, 3, 4, 5]`

## [Finding the index of an item in a list](https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list)

**3073 Votes**, Eugene M

```python
>>> ["foo", "bar", "baz"].index("bar")
1
```

Reference: Data Structures > More on Lists
Caveats follow
Note that while this is perhaps the cleanest way to answer the question as asked, `index` is a rather weak component of the `list` API, and I can't remember the last time I used it in anger. It's been pointed out to me in the comments that because this answer is heavily referenced, it should be made more complete. Some caveats about `list.index` follow. It is probably worth initially taking a look at the documentation for it:


```python
list.index(x[, start[, end]])
```

Return zero-based index in the list of the first item whose value is equal to x. Raises a `ValueError` if there is no such item.
The optional arguments start and end are interpreted as in the slice notation and are used to limit the search to a particular subsequence of the list. The returned index is computed relative to the beginning of the full sequence rather than the start argument.


### Linear time-complexity in list length

An `index` call checks every element of the list in order, until it finds a match. If your list is long, and you don't know roughly where in the list it occurs, this search could become a bottleneck. In that case, you should consider a different data structure. Note that if you know roughly where to find the match, you can give `index` a hint. For instance, in this snippet, `l.index(999_999, 999_990, 1_000_000)` is roughly five orders of magnitude faster than straight `l.index(999_999)`, because the former only has to search 10 entries, while the latter searches a million:

```python
>>> import timeit
>>> timeit.timeit('l.index(999_999)', setup='l = list(range(0, 1_000_000))', number=1000)
9.356267921015387
>>> timeit.timeit('l.index(999_999, 999_990, 1_000_000)', setup='l = list(range(0, 1_000_000))', number=1000)
0.0004404920036904514
```


### Only returns the index of the first match to its argument

A call to `index` searches through the list in order until it finds a match, and stops there. If you expect to need indices of more matches, you should use a list comprehension, or generator expression.

```python
>>> [1, 1].index(1)
0
>>> [i for i, e in enumerate([1, 2, 1]) if e == 1]
[0, 2]
>>> g = (i for i, e in enumerate([1, 2, 1]) if e == 1)
>>> next(g)
0
>>> next(g)
2
```

Most places where I once would have used `index`, I now use a list comprehension or generator expression because they're more generalizable. So if you're considering reaching for `index`, take a look at these excellent Python features.

### Throws if element not present in list

A call to `index` results in a `ValueError` if the item's not present.

```python
>>> [1, 1].index(2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: 2 is not in list
```

If the item might not be present in the list, you should either 

Check for it first with `item in my_list` (clean, readable approach), or
Wrap the `index` call in a `try/except` block which catches `ValueError` (probably faster, at least when the list to search is long, and the item is usually present.)

## [Using global variables in a function](https://stackoverflow.com/questions/423379/using-global-variables-in-a-function)

**3059 Votes**, user46646

You can use a global variable in other functions by declaring it as `global` in each function that assigns to it:

```python
globvar = 0

def set_globvar_to_one():
    global globvar    # Needed to modify global copy of globvar
    globvar = 1

def print_globvar():
    print(globvar)     # No need for global declaration to read value of globvar

set_globvar_to_one()
print_globvar()       # Prints 1
```

I imagine the reason for it is that, since global variables are so dangerous, Python wants to make sure that you really know that's what you're playing with by explicitly requiring the `global` keyword.
See other answers if you want to share a global variable across modules.

## [Iterating over dictionaries using 'for' loops](https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops)

**3055 Votes**, TopChef

`key` is just a variable name.  

```python
for key in d:
```

will simply loop over the keys in the dictionary, rather than the keys and values.  To loop over both key and value you can use the following:
For Python 3.x:

```python
for key, value in d.items():
```

For Python 2.x:

```python
for key, value in d.iteritems():
```

To test for yourself, change the word `key` to `poop`.
In Python 3.x, `iteritems()` was replaced with simply `items()`, which returns a set-like view backed by the dict, like `iteritems()` but even better. 
This is also available in 2.7 as `viewitems()`. 
The operation `items()` will work for both 2 and 3, but in 2 it will return a list of the dictionary's `(key, value)` pairs, which will not reflect changes to the dict that happen after the `items()` call. If you want the 2.x behavior in 3.x, you can call `list(d.items())`.

## [How to get the current time in Python](https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python)

**2795 Votes**, user46646

Use:

```python
>>> import datetime
>>> datetime.datetime.now()
datetime.datetime(2009, 1, 6, 15, 8, 24, 78915)

>>> print(datetime.datetime.now())
2009-01-06 15:08:24.789150
```

And just the time:

```python
>>> datetime.datetime.now().time()
datetime.time(15, 8, 24, 78915)

>>> print(datetime.datetime.now().time())
15:08:24.789150
```

See the documentation for more information.
To save typing, you can import the `datetime` object from the `datetime` module:

```python
>>> from datetime import datetime
```

Then remove the leading `datetime.` from all of the above.

## [How to make a chain of function decorators?](https://stackoverflow.com/questions/739654/how-to-make-a-chain-of-function-decorators)

**2716 Votes**, Imran

Check out the documentation to see how decorators work. Here is what you asked for:

```python
from functools import wraps

def makebold(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        return "<b>" + fn(*args, **kwargs) + "</b>"
    return wrapped

def makeitalic(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        return "<i>" + fn(*args, **kwargs) + "</i>"
    return wrapped

@makebold
@makeitalic
def hello():
    return "hello world"

@makebold
@makeitalic
def log(s):
    return s

print hello()        # returns "<b><i>hello world</i></b>"
print hello.__name__ # with functools.wraps() this returns "hello"
print log('hello')   # returns "<b><i>hello</i></b>"
```

## [How can I make a time delay in Python? [duplicate]](https://stackoverflow.com/questions/510348/how-can-i-make-a-time-delay-in-python)

**2710 Votes**, user46646

```python
import time
time.sleep(5)   # Delays for 5 seconds. You can also use a float value.
```

Here is another example where something is run approximately once a minute:

```python
import time
while True:
    print("This prints once a minute.")
    time.sleep(60) # Delay for 1 minute (60 seconds).
```

## [Check if a given key already exists in a dictionary](https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary)

**2683 Votes**, Mohan Gulati

`in` is the intended way to test for the existence of a key in a `dict`.

```python
d = {"key1": 10, "key2": 23}

if "key1" in d:
    print("this will execute")

if "nonexistent key" in d:
    print("this will not")
```

If you wanted a default, you can always use `dict.get()`:

```python
d = dict()

for i in range(100):
    key = i % 10
    d[key] = d.get(key, 0) + 1
```

and if you wanted to always ensure a default value for any key you can either use `dict.setdefault()` repeatedly or `defaultdict` from the `collections` module, like so:

```python
from collections import defaultdict

d = defaultdict(int)

for i in range(100):
    d[i % 10] += 1
```

but in general, the `in` keyword is the best way to do it.

## [Difference between __str__ and __repr__?](https://stackoverflow.com/questions/1436703/difference-between-str-and-repr)

**2674 Votes**, Casebash

Alex summarized well but, surprisingly, was too succinct.
First, let me reiterate the main points in Alexs post:

The default implementation is useless (its hard to think of one which wouldnt be, but yeah)
`__repr__` goal is to be unambiguous
`__str__` goal is to be readable
Containers `__str__` uses contained objects `__repr__`

Default implementation is useless
This is mostly a surprise because Pythons defaults tend to be fairly useful. However, in this case, having a default for `__repr__` which would act like:

```python
return "%s(%r)" % (self.__class__, self.__dict__)
```

would have been too dangerous (for example, too easy to get into infinite recursion if objects reference each other). So Python cops out. Note that there is one default which is true: if `__repr__` is defined, and `__str__` is not, the object will behave as though `__str__=__repr__`.
This means, in simple terms: almost every object you implement should have a functional `__repr__` thats usable for understanding the object. Implementing `__str__` is optional: do that if you need a pretty print functionality (for example, used by a report generator).
The goal of `__repr__` is to be unambiguous
Let me come right out and say it  I do not believe in debuggers. I dont really know how to use any debugger, and have never used one seriously. Furthermore, I believe that the big fault in debuggers is their basic nature  most failures I debug happened a long long time ago, in a galaxy far far away. This means that I do believe, with religious fervor, in logging. Logging is the lifeblood of any decent fire-and-forget server system. Python makes it easy to log: with maybe some project specific wrappers, all you need is a

```python
log(INFO, "I am in the weird function and a is", a, "and b is", b, "but I got a null C  using default", default_c)
```

But you have to do the last step  make sure every object you implement has a useful repr, so code like that can just work. This is why the eval thing comes up: if you have enough information so `eval(repr(c))==c`, that means you know everything there is to know about ``c. If thats easy enough, at least in a fuzzy way, do it. If not, make sure you have enough information about ``c anyway. I usually use an eval-like format: `"MyClass(this=%r,that=%r)" % (self.this,self.that)`. It does not mean that you can actually construct MyClass, or that those are the right constructor arguments  but it is a useful form to express this is everything you need to know about this instance.
Note: I used `%r` above, not `%s`. You always want to use `repr()` [or `%r` formatting character, equivalently] inside `__repr__` implementation, or youre defeating the goal of repr. You want to be able to differentiate `MyClass(3)` and `MyClass("3")`.
The goal of `__str__` is to be readable
Specifically, it is not intended to be unambiguous  notice that `str(3)==str("3")`. Likewise, if you implement an IP abstraction, having the str of it look like 192.168.1.1 is just fine. When implementing a date/time abstraction, the str can be "2010/4/12 15:35:22", etc. The goal is to represent it in a way that a user, not a programmer, would want to read it. Chop off useless digits, pretend to be some other class  as long is it supports readability, it is an improvement.
Containers `__str__` uses contained objects `__repr__`
This seems surprising, doesnt it? It is a little, but how readable would it be if it used their `__str__`?

```python
[moshe is, 3, hello
world, this is a list, oh I don't know, containing just 4 elements]
```

Not very. Specifically, the strings in a container would find it way too easy to disturb its string representation. In the face of ambiguity, remember, Python resists the temptation to guess. If you want the above behavior when youre printing a list, just

```python
print "[" + ", ".join(l) + "]"
```

(you can probably also figure out what to do about dictionaries.
Summary
Implement `__repr__` for any class you implement. This should be second nature. Implement `__str__` if you think it would be useful to have a string version which errs on the side of readability.

## [Catch multiple exceptions in one line (except block)](https://stackoverflow.com/questions/6470428/catch-multiple-exceptions-in-one-line-except-block)

**2672 Votes**, inspectorG4dget

From Python Documentation:

An except clause may name multiple exceptions as a parenthesized tuple, for example


```python
except (IDontLikeYouException, YouAreBeingMeanException) as e:
    pass
```

Or, for Python 2 only:

```python
except (IDontLikeYouException, YouAreBeingMeanException), e:
    pass
```

Separating the exception from the variable with a comma will still work in Python 2.6 and 2.7, but is now deprecated and does not work in Python 3; now you should be using `as`.

## [How do I pass a variable by reference?](https://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference)

**2579 Votes**, David Sykes

Arguments are passed by assignment. The rationale behind this is twofold:

the parameter passed in is actually a reference to an object (but the reference is passed by value)
some data types are mutable, but others aren't

So:

If you pass a mutable object into a method, the method gets a reference to that same object and you can mutate it to your heart's delight, but if you rebind the reference in the method, the outer scope will know nothing about it, and after you're done, the outer reference will still point at the original object. 
If you pass an immutable object to a method, you still can't rebind the outer reference, and you can't even mutate the object.

To make it even more clear, let's have some examples. 

### List - a mutable type

Let's try to modify the list that was passed to a method:

```python
def try_to_change_list_contents(the_list):
    print('got', the_list)
    the_list.append('four')
    print('changed to', the_list)

outer_list = ['one', 'two', 'three']

print('before, outer_list =', outer_list)
try_to_change_list_contents(outer_list)
print('after, outer_list =', outer_list)
```

Output:

```python
before, outer_list = ['one', 'two', 'three']
got ['one', 'two', 'three']
changed to ['one', 'two', 'three', 'four']
after, outer_list = ['one', 'two', 'three', 'four']
```

Since the parameter passed in is a reference to `outer_list`, not a copy of it, we can use the mutating list methods to change it and have the changes reflected in the outer scope.
Now let's see what happens when we try to change the reference that was passed in as a parameter:

```python
def try_to_change_list_reference(the_list):
    print('got', the_list)
    the_list = ['and', 'we', 'can', 'not', 'lie']
    print('set to', the_list)

outer_list = ['we', 'like', 'proper', 'English']

print('before, outer_list =', outer_list)
try_to_change_list_reference(outer_list)
print('after, outer_list =', outer_list)
```

Output:

```python
before, outer_list = ['we', 'like', 'proper', 'English']
got ['we', 'like', 'proper', 'English']
set to ['and', 'we', 'can', 'not', 'lie']
after, outer_list = ['we', 'like', 'proper', 'English']
```

Since the `the_list` parameter was passed by value, assigning a new list to it had no effect that the code outside the method could see. The `the_list` was a copy of the `outer_list` reference, and we had `the_list` point to a new list, but there was no way to change where `outer_list` pointed.

### String - an immutable type

It's immutable, so there's nothing we can do to change the contents of the string
Now, let's try to change the reference

```python
def try_to_change_string_reference(the_string):
    print('got', the_string)
    the_string = 'In a kingdom by the sea'
    print('set to', the_string)

outer_string = 'It was many and many a year ago'

print('before, outer_string =', outer_string)
try_to_change_string_reference(outer_string)
print('after, outer_string =', outer_string)
```

Output:

```python
before, outer_string = It was many and many a year ago
got It was many and many a year ago
set to In a kingdom by the sea
after, outer_string = It was many and many a year ago
```

Again, since the `the_string` parameter was passed by value, assigning a new string to it had no effect that the code outside the method could see. The `the_string` was a copy of the `outer_string` reference, and we had `the_string` point to a new string, but there was no way to change where `outer_string` pointed.
I hope this clears things up a little.
EDIT: It's been noted that this doesn't answer the question that @David originally asked, "Is there something I can do to pass the variable by actual reference?". Let's work on that.

### How do we get around this?

As @Andrea's answer shows, you could return the new value. This doesn't change the way things are passed in, but does let you get the information you want back out:

```python
def return_a_whole_new_string(the_string):
    new_string = something_to_do_with_the_old_string(the_string)
    return new_string

# then you could call it like
my_string = return_a_whole_new_string(my_string)
```

If you really wanted to avoid using a return value, you could create a class to hold your value and pass it into the function or use an existing class, like a list:

```python
def use_a_wrapper_to_simulate_pass_by_reference(stuff_to_change):
    new_string = something_to_do_with_the_old_string(stuff_to_change[0])
    stuff_to_change[0] = new_string

# then you could call it like
wrapper = [my_string]
use_a_wrapper_to_simulate_pass_by_reference(wrapper)

do_something_with(wrapper[0])
```

Although this seems a little cumbersome.

## [Least Astonishment and the Mutable Default Argument](https://stackoverflow.com/questions/1132941/least-astonishment-and-the-mutable-default-argument)

**2557 Votes**, Stefano Borini

Actually, this is not a design flaw, and it is not because of internals, or performance.
It comes simply from the fact that functions in Python are first-class objects, and not only a piece of code.
As soon as you get to think into this way, then it completely makes sense: a function is an object being evaluated on its definition; default parameters are kind of "member data" and therefore their state may change from one call to the other - exactly as in any other object.
In any case, Effbot has a very nice explanation of the reasons for this behavior in Default Parameter Values in Python.
I found it very clear, and I really suggest reading it for a better knowledge of how function objects work.

## [How can I add new keys to a dictionary?](https://stackoverflow.com/questions/1024847/how-can-i-add-new-keys-to-a-dictionary)

**2552 Votes**, lfaraone

```python
d = {'key': 'value'}
print(d)
# {'key': 'value'}
d['mynewkey'] = 'mynewvalue'
print(d)
# {'key': 'value', 'mynewkey': 'mynewvalue'}
```

## [How to install pip on Windows?](https://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows)

**2520 Votes**, community-wiki

### Python 2.7.9+ and 3.4+

Good news! Python 3.4 (released March 2014) and Python 2.7.9 (released December 2014) ship with Pip. This is the best feature of any Python release. It makes the community's wealth of libraries accessible to everyone. Newbies are no longer excluded from using community libraries by the prohibitive difficulty of setup. In shipping with a package manager, Python joins Ruby, Node.js, Haskell, Perl, Goalmost every other contemporary language with a majority open-source community. Thank you, Python.
If you do find that pip is not available when using Python 3.4+ or Python 2.7.9+, simply execute e.g.:

```python
py -3 -m ensurepip
```

Of course, that doesn't mean Python packaging is problem solved. The experience remains frustrating. I discuss this in the Stack Overflow question Does Python have a package/module management system?.
And, alas for everyone using Python 2.7.8 or earlier (a sizable portion of the community). There's no plan to ship Pip to you. Manual instructions follow.

### Python 2  2.7.8 and Python 3  3.3

Flying in the face of its 'batteries included' motto, Python ships without a package manager. To make matters worse, Pip wasuntil recentlyironically difficult to install.
Official instructions
Per https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip:
Download `get-pip.py`, being careful to save it as a `.py` file rather than `.txt`. Then, run it from the command prompt:

```python
python get-pip.py
```

You possibly need an administrator command prompt to do this. Follow Start a Command Prompt as an Administrator (Microsoft TechNet).
This installs the pip package, which (in Windows) contains ...\Scripts\pip.exe that path must be in PATH environment variable to use pip from the command line (see the second part of 'Alternative Instructions' for adding it to your PATH,
Alternative instructions
The official documentation tells users to install Pip and each of its dependencies from source. That's tedious for the experienced and prohibitively difficult for newbies.
For our sake, Christoph Gohlke prepares Windows installers (`.msi`) for popular Python packages. He builds installers for all Python versions, both 32 and 64 bit. You need to:

Install setuptools
Install pip

For me, this installed Pip at `C:\Python27\Scripts\pip.exe`. Find `pip.exe` on your computer, then add its folder (for example, `C:\Python27\Scripts`) to your path (Start / Edit environment variables). Now you should be able to run `pip` from the command line. Try installing a package:

```python
pip install httpie
```

There you go (hopefully)! Solutions for common problems are given below:
Proxy problems
If you work in an office, you might be behind an HTTP proxy. If so, set the environment variables `http_proxy` and `https_proxy`. Most Python applications (and other free software) respect these. Example syntax:

```python
http://proxy_url:port
http://username:password@proxy_url:port
```

If you're really unlucky, your proxy might be a Microsoft NTLM proxy. Free software can't cope. The only solution is to install a free software friendly proxy that forwards to the nasty proxy. http://cntlm.sourceforge.net/
Unable to find vcvarsall.bat
Python modules can be partly written in C or C++. Pip tries to compile from source. If you don't have a C/C++ compiler installed and configured, you'll see this cryptic error message.

Error: Unable to find vcvarsall.bat

You can fix that by installing a C++ compiler such as MinGW or Visual C++. Microsoft actually ships one specifically for use with Python. Or try Microsoft Visual C++ Compiler for Python 2.7.
Often though it's easier to check Christoph's site for your package.

## [Understanding Python super() with __init__() methods [duplicate]](https://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods)

**2489 Votes**, Mizipzor

`super()` lets you avoid referring to the base class explicitly, which can be nice. But the main advantage comes with multiple inheritance, where all sorts of fun stuff can happen. See the standard docs on super if you haven't already.
Note that the syntax changed in Python 3.0: you can just say `super().__init__()` instead of `super(ChildB, self).__init__()` which IMO is quite a bit nicer. The standard docs also refer to a guide to using `super()` which is quite explanatory.

## [How to clone or copy a list?](https://stackoverflow.com/questions/2612802/how-to-clone-or-copy-a-list)

**2468 Votes**, aF.

With `new_list = my_list`, you don't actually have two lists. The assignment just copies the reference to the list, not the actual list, so both `new_list` and `my_list` refer to the same list after the assignment.
To actually copy the list, you have various possibilities:

You can use the builtin `list.copy()` method (available since Python 3.3):

```python
new_list = old_list.copy()
```

You can slice it: 

```python
new_list = old_list[:]
```

Alex Martelli's opinion (at least back in 2007) about this is, that it is a weird syntax and it does not make sense to use it ever. ;) (In his opinion, the next one is more readable).
You can use the built in `list()` function:

```python
new_list = list(old_list)
```

You can use generic `copy.copy()`:

```python
import copy
new_list = copy.copy(old_list)
```

This is a little slower than `list()` because it has to find out the datatype of `old_list` first.
If the list contains objects and you want to copy them as well, use generic `copy.deepcopy()`:

```python
import copy
new_list = copy.deepcopy(old_list)
```

Obviously the slowest and most memory-needing method, but sometimes unavoidable.

Example:

```python
import copy

class Foo(object):
    def __init__(self, val):
         self.val = val

    def __repr__(self):
        return 'Foo({!r})'.format(self.val)

foo = Foo(1)

a = ['foo', foo]
b = a.copy()
c = a[:]
d = list(a)
e = copy.copy(a)
f = copy.deepcopy(a)

# edit orignal list and instance 
a.append('baz')
foo.val = 5

print('original: %r\nlist.copy(): %r\nslice: %r\nlist(): %r\ncopy: %r\ndeepcopy: %r'
      % (a, b, c, d, e, f))
```

Result:

```python
original: ['foo', Foo(5), 'baz']
list.copy(): ['foo', Foo(5)]
slice: ['foo', Foo(5)]
list(): ['foo', Foo(5)]
copy: ['foo', Foo(5)]
deepcopy: ['foo', Foo(1)]
```

## [How do I concatenate two lists in Python?](https://stackoverflow.com/questions/1720421/how-do-i-concatenate-two-lists-in-python)

**2448 Votes**, y2k

You can use the ``+ operator to combine them:

```python
listone = [1,2,3]
listtwo = [4,5,6]

joinedlist = listone + listtwo
```

Output:

```python
>>> joinedlist
[1,2,3,4,5,6]
```

## [How do I copy a file in Python?](https://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python)

**2399 Votes**, Matt

`shutil` has many methods you can use. One of which is:

```python
from shutil import copyfile
copyfile(src, dst)
```


Copy the contents of the file named src to a file named dst.
The destination location must be writable; otherwise, an IOError exception will be raised.
If dst already exists, it will be replaced.
Special files such as character or block devices and pipes cannot be copied with this function. 
With copy, src and dst are path names given as strings. 

If you use `os.path` operations, use `copy` rather than `copyfile.copyfile` will only accept strings.

## [What does ** (double star/asterisk) and * (star/asterisk) do for parameters?](https://stackoverflow.com/questions/36901/what-does-double-star-asterisk-and-star-asterisk-do-for-parameters)

**2280 Votes**, Todd

The `*args` and `**kwargs` is a common idiom to allow arbitrary number of arguments to functions as described in the section more on defining functions in the Python documentation.
The `*args` will give you all function parameters as a tuple:

```python
def foo(*args):
    for a in args:
        print(a)        

foo(1)
# 1

foo(1,2,3)
# 1
# 2
# 3
```

The `**kwargs` will give you all 
keyword arguments except for those corresponding to a formal parameter as a dictionary.

```python
def bar(**kwargs):
    for a in kwargs:
        print(a, kwargs[a])  

bar(name='one', age=27)
# age 27
# name one
```

Both idioms can be mixed with normal arguments to allow a set of fixed and some variable arguments:

```python
def foo(kind, *args, **kwargs):
   pass
```

It is also possible to use this the other way around:

```python
def foo(a, b, c):
    print(a, b, c)

obj = {'b':10, 'c':'lee'}

foo(100,**obj)
# 100 10 lee
```

Another usage of the `*l` idiom is to unpack argument lists when calling a function.

```python
def foo(bar, lee):
    print(bar, lee)

l = [1,2]

foo(*l)
# 1 2
```

In Python 3 it is possible to use `*l` on the left side of an assignment (Extended Iterable Unpacking), though it gives a list instead of a tuple in this context:

```python
first, *rest = [1,2,3,4]
first, *l, last = [1,2,3,4]
```

Also Python 3 adds new semantic (refer PEP 3102):

```python
def func(arg1, arg2, arg3, *, kwarg1, kwarg2):
    pass
```

Such function accepts only 3 positional arguments, and everything after ``* can only be passed as keyword arguments.

## [What is __init__.py for?](https://stackoverflow.com/questions/448271/what-is-init-py-for)

**2254 Votes**, Mat

It used to be a required part of a package (old, pre-3.3 "regular package", not newer 3.3+ "namespace package").
Here's the documentation.

Python defines two types of packages, regular packages and namespace packages. Regular packages are traditional packages as they existed in Python 3.2 and earlier. A regular package is typically implemented as a directory containing an `__init__.py` file. When a regular package is imported, this `__init__.py` file is implicitly executed, and the objects it defines are bound to names in the packages namespace. The `__init__.py` file can contain the same Python code that any other module can contain, and Python will add some additional attributes to the module when it is imported.

But just click the link, it contains an example, more information, and an explanation of namespace packages, the kind of packages without `__init__.py`.

## [Manually raising (throwing) an exception in Python](https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python)

**2213 Votes**, TIMEX

### How do I manually throw/raise an exception in Python?


Use the most specific Exception constructor that semantically fits your issue.  
Be specific in your message, e.g.:

```python
raise ValueError('A very specific bad thing happened.')
```


### Don't raise generic exceptions

Avoid raising a generic `Exception`. To catch it, you'll have to catch all other more specific exceptions that subclass it.
Problem 1: Hiding bugs

```python
raise Exception('I know Python!') # Don't! If you catch, likely to hide bugs.
```

For example:

```python
def demo_bad_catch():
    try:
        raise ValueError('Represents a hidden bug, do not catch this')
        raise Exception('This is the exception you expect to handle')
    except Exception as error:
        print('Caught this error: ' + repr(error))

>>> demo_bad_catch()
Caught this error: ValueError('Represents a hidden bug, do not catch this',)
```

Problem 2: Won't catch
And more specific catches won't catch the general exception:

```python
def demo_no_catch():
    try:
        raise Exception('general exceptions not caught by specific handling')
    except ValueError as e:
        print('we will not catch exception: Exception')


>>> demo_no_catch()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in demo_no_catch
Exception: general exceptions not caught by specific handling
```


### Best Practices: `raise` statement

Instead, use the most specific Exception constructor that semantically fits your issue.

```python
raise ValueError('A very specific bad thing happened')
```

which also handily allows an arbitrary number of arguments to be passed to the constructor:

```python
raise ValueError('A very specific bad thing happened', 'foo', 'bar', 'baz') 
```

These arguments are accessed by the `args` attribute on the `Exception` object. For example:

```python
try:
    some_code_that_may_raise_our_value_error()
except ValueError as err:
    print(err.args)
```

prints 

```python
('message', 'foo', 'bar', 'baz')    
```

In Python 2.5, an actual `message` attribute was added to `BaseException` in favor of encouraging users to subclass Exceptions and stop using `args`, but the introduction of `message` and the original deprecation of args has been retracted.

### Best Practices: `except` clause

When inside an except clause, you might want to, for example, log that a specific type of error happened, and then re-raise. The best way to do this while preserving the stack trace is to use a bare raise statement. For example:

```python
logger = logging.getLogger(__name__)

try:
    do_something_in_app_that_breaks_easily()
except AppError as error:
    logger.error(error)
    raise                 # just this!
    # raise AppError      # Don't do this, you'll lose the stack trace!
```

Don't modify your errors... but if you insist.
You can preserve the stacktrace (and error value) with `sys.exc_info()`, but this is way more error prone and has compatibility problems between Python 2 and 3, prefer to use a bare `raise` to re-raise. 
To explain - the `sys.exc_info()` returns the type, value, and traceback. 

```python
type, value, traceback = sys.exc_info()
```

This is the syntax in Python 2 - note this is not compatible with Python 3:

```python
    raise AppError, error, sys.exc_info()[2] # avoid this.
    # Equivalently, as error *is* the second object:
    raise sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
```

If you want to, you can modify what happens with your new raise - e.g. setting new `args` for the instance:

```python
def error():
    raise ValueError('oops!')

def catch_error_modify_message():
    try:
        error()
    except ValueError:
        error_type, error_instance, traceback = sys.exc_info()
        error_instance.args = (error_instance.args[0] + ' <modification>',)
        raise error_type, error_instance, traceback
```

And we have preserved the whole traceback while modifying the args. Note that this is not a best practice and it is invalid syntax in Python 3 (making keeping compatibility much harder to work around).

```python
>>> catch_error_modify_message()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in catch_error_modify_message
  File "<stdin>", line 2, in error
ValueError: oops! <modification>
```

In Python 3:

```python
    raise error.with_traceback(sys.exc_info()[2])
```

Again: avoid manually manipulating tracebacks. It's less efficient and more error prone. And if you're using threading and `sys.exc_info` you may even get the wrong traceback (especially if you're using exception handling for control flow - which I'd personally tend to avoid.)
Python 3, Exception chaining
In Python 3, you can chain Exceptions, which preserve tracebacks:

```python
    raise RuntimeError('specific message') from error
```

Be aware:

this does allow changing the error type raised, and
this is not compatible with Python 2.

Deprecated Methods:
These can easily hide and even get into production code. You want to raise an exception, and doing them will raise an exception, but not the one intended!
Valid in Python 2, but not in Python 3 is the following:

```python
raise ValueError, 'message' # Don't do this, it's deprecated!
```

Only valid in much older versions of Python (2.4 and lower), you may still see people raising strings:

```python
raise 'message' # really really wrong. don't do this.
```

In all modern versions, this will actually raise a `TypeError`, because you're not raising a `BaseException` type. If you're not checking for the right exception and don't have a reviewer that's aware of the issue, it could get into production.

### Example Usage

I raise Exceptions to warn consumers of my API if they're using it incorrectly:

```python
def api_func(foo):
    '''foo should be either 'baz' or 'bar'. returns something very useful.'''
    if foo not in _ALLOWED_ARGS:
        raise ValueError('{foo} wrong, use "baz" or "bar"'.format(foo=repr(foo)))
```


### Create your own error types when apropos


"I want to make an error on purpose, so that it would go into the except"

You can create your own error types, if you want to indicate something specific is wrong with your application, just subclass the appropriate point in the exception hierarchy:

```python
class MyAppLookupError(LookupError):
    '''raise this when there's a lookup error for my app'''
```

and usage:

```python
if important_key not in resource_dict and not ok_to_be_missing:
    raise MyAppLookupError('resource is missing, and that is not ok.')
```

## [How do you split a list into evenly sized chunks?](https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks)

**2202 Votes**, jespern

Here's a generator that yields the chunks you want:

```python
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
```



```python
import pprint
pprint.pprint(list(chunks(range(10, 75), 10)))
[[10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
 [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
 [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
 [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
 [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
 [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
 [70, 71, 72, 73, 74]]
```


If you're using Python 2, you should use `xrange()` instead of `range()`:

```python
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in xrange(0, len(lst), n):
        yield lst[i:i + n]
```


Also you can simply use list comprehension instead of writing a function, though it's a good idea to encapsulate operations like this in named functions so that your code is easier to understand. Python 3:

```python
[lst[i:i + n] for i in range(0, len(lst), n)]
```

Python 2 version:

```python
[lst[i:i + n] for i in xrange(0, len(lst), n)]
```

## [How do I parse a string to a float or int?](https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int)

**2193 Votes**, Tristan Havelick

```python
>>> a = "545.2222"
>>> float(a)
545.22220000000004
>>> int(float(a))
545
```

## [Convert bytes to a string](https://stackoverflow.com/questions/606191/convert-bytes-to-a-string)

**2191 Votes**, Tomas Sedovic

You need to decode the bytes object to produce a string:

```python
>>> b"abcde"
b'abcde'

# utf-8 is used here because it is a very common encoding, but you
# need to use the encoding your data is actually in.
>>> b"abcde".decode("utf-8") 
'abcde'
```

## [Find current directory and file's directory [duplicate]](https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory)

**2155 Votes**, John Howard

To get the full path to the directory a Python file is contained in, write this in that file:

```python
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
```

(Note that the incantation above won't work if you've already used `os.chdir()` to change your current working directory, since the value of the `__file__` constant is relative to the current working directory and is not changed by an `os.chdir()` call.)

To get the current working directory use 

```python
import os
cwd = os.getcwd()
```


Documentation references for the modules, constants and functions used above:

The `os` and `os.path` modules.
The `__file__` constant
`os.path.realpath(path)` (returns "the canonical path of the specified filename, eliminating any symbolic links encountered in the path")
`os.path.dirname(path)` (returns "the directory name of pathname `path`")
`os.getcwd()` (returns "a string representing the current working directory")
`os.chdir(path)` ("change the current working directory to `path`")

## [Converting string into datetime](https://stackoverflow.com/questions/466345/converting-string-into-datetime)

**2133 Votes**, Oli

`datetime.strptime` is the main routine for parsing strings into datetimes. It can handle all sorts of formats, with the format determined by a format string you give it:

```python
from datetime import datetime

datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
```

The resulting `datetime` object is timezone-naive.
Links:

Python documentation for `strptime`: Python 2, Python 3
Python documentation for `strptime`/`strftime` format strings: Python 2, Python 3
strftime.org is also a really nice reference for strftime

Notes:

`strptime` = "string parse time"
`strftime` = "string format time"
Pronounce it out loud today & you won't have to search for it again in 6 months.

## [How do I get a substring of a string in Python?](https://stackoverflow.com/questions/663171/how-do-i-get-a-substring-of-a-string-in-python)

**2101 Votes**, Joan Venge

```python
>>> x = "Hello World!"
>>> x[2:]
'llo World!'
>>> x[:2]
'He'
>>> x[:-2]
'Hello Worl'
>>> x[-2:]
'd!'
>>> x[2:-2]
'llo Worl'
```

Python calls this concept "slicing" and it works on more than just strings. Take a look here for a comprehensive introduction.

## [Is there a way to run Python on Android?](https://stackoverflow.com/questions/101754/is-there-a-way-to-run-python-on-android)

**2093 Votes**, e-satis

One way is to use Kivy:

Open source Python library for rapid development of applications
  that make use of innovative user interfaces, such as multi-touch apps.



Kivy runs on Linux, Windows, OS X, Android and iOS. You can run the same [python] code on all supported platforms.

Kivy Showcase app

## [How to delete a file or folder?](https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder)

**2077 Votes**, Zygimantas

`os.remove()` removes a file.
`os.rmdir()` removes an empty directory.
`shutil.rmtree()` deletes a directory and all its contents.


`Path` objects from the Python 3.4+ `pathlib` module also expose these instance methods:

`pathlib.Path.unlink()` removes a file or symbolic link.
`pathlib.Path.rmdir()` removes an empty directory.

## [How to print colored text in terminal in Python?](https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python)

**2066 Votes**, aboSamoor

This somewhat depends on what platform you are on. The most common way to do this is by printing ANSI escape sequences. For a simple example, here's some python code from the blender build scripts:

```python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
```

To use code like this, you can do something like 

```python
print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
```

or, with Python3.6+:

```python
print(f"{bcolors.WARNING}Warning: No active frommets remain. Continue?{bcolors.ENDC}")
```

This will work on unixes including OS X, linux and windows (provided you use ANSICON, or in Windows 10 provided you enable VT100 emulation). There are ansi codes for setting the color, moving the cursor, and more.
If you are going to get complicated with this (and it sounds like you are if you are writing a game), you should look into the "curses" module, which handles a lot of the complicated parts of this for you. The Python Curses HowTO is a good introduction.
If you are not using extended ASCII (i.e. not on a PC), you are stuck with the ascii characters below 127, and '#' or '@' is probably your best bet for a block. If you can ensure your terminal is using a IBM extended ascii character set, you have many more options. Characters 176, 177, 178 and 219 are the "block characters".
Some modern text-based programs, such as "Dwarf Fortress", emulate text mode in a graphical mode, and use images of the classic PC font. You can find some of these bitmaps that you can use on the Dwarf Fortress Wiki see (user-made tilesets).
The Text Mode Demo Contest has more resources for doing graphics in text mode.
Hmm.. I think got a little carried away on this answer. I am in the midst of planning an epic text-based adventure game, though. Good luck with your colored text!

## [Why is 1000000000000000 in range(1000000000000001) so fast in Python 3?](https://stackoverflow.com/questions/30081275/why-is-1000000000000000-in-range1000000000000001-so-fast-in-python-3)

**2046 Votes**, Rick supports Monica

The Python 3 `range()` object doesn't produce numbers immediately; it is a smart sequence object that produces numbers on demand. All it contains is your start, stop and step values, then as you iterate over the object the next integer is calculated each iteration.
The object also implements the `object.__contains__` hook, and calculates if your number is part of its range. Calculating is a (near) constant time operation *. There is never a need to scan through all possible integers in the range.
From the `range()` object documentation:

The advantage of the `range` type over a regular `list` or `tuple` is that a range object will always take the same (small) amount of memory, no matter the size of the range it represents (as it only stores the `start`, `stop` and `step` values, calculating individual items and subranges as needed).

So at a minimum, your `range()` object would do:

```python
class my_range(object):
    def __init__(self, start, stop=None, step=1):
        if stop is None:
            start, stop = 0, start
        self.start, self.stop, self.step = start, stop, step
        if step < 0:
            lo, hi, step = stop, start, -step
        else:
            lo, hi = start, stop
        self.length = 0 if lo > hi else ((hi - lo - 1) // step) + 1

    def __iter__(self):
        current = self.start
        if self.step < 0:
            while current > self.stop:
                yield current
                current += self.step
        else:
            while current < self.stop:
                yield current
                current += self.step

    def __len__(self):
        return self.length

    def __getitem__(self, i):
        if i < 0:
            i += self.length
        if 0 <= i < self.length:
            return self.start + i * self.step
        raise IndexError('Index out of range: {}'.format(i))

    def __contains__(self, num):
        if self.step < 0:
            if not (self.stop < num <= self.start):
                return False
        else:
            if not (self.start <= num < self.stop):
                return False
        return (num - self.start) % self.step == 0
```

This is still missing several things that a real `range()` supports (such as the `.index()` or `.count()` methods, hashing, equality testing, or slicing), but should give you an idea.
I also simplified the `__contains__` implementation to only focus on integer tests; if you give a real `range()` object a non-integer value (including subclasses of `int`), a slow scan is initiated to see if there is a match, just as if you use a containment test against a list of all the contained values. This was done to continue to support other numeric types that just happen to support equality testing with integers but are not expected to support integer arithmetic as well. See the original Python issue that implemented the containment test.

* Near constant time because Python integers are unbounded and so math operations also grow in time as N grows, making this a O(log N) operation. Since its all executed in optimised C code and Python stores integer values in 30-bit chunks, youd run out of memory before you saw any performance impact due to the size of the integers involved here.

## [How to access environment variable values?](https://stackoverflow.com/questions/4906977/how-to-access-environment-variable-values)

**2046 Votes**, Amit Yadav

Environment variables are accessed through os.environ

```python
import os
print(os.environ['HOME'])
```

Or you can see a list of all the environment variables using:

```python
os.environ
```

As sometimes you might need to see a complete list!

```python
# using get will return `None` if a key is not present rather than raise a `KeyError`
print(os.environ.get('KEY_THAT_MIGHT_EXIST'))

# os.getenv is equivalent, and can also give a default value instead of `None`
print(os.getenv('KEY_THAT_MIGHT_EXIST', default_value))
```

Python default installation on Windows is `C:\Python`. If you want to find out while running python you can do:

```python
import sys
print(sys.prefix)
```

## [How to read a file line-by-line into a list?](https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list)

**2028 Votes**, Julie Raswick

```python
with open(filename) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 
```

## [How do I lowercase a string in Python?](https://stackoverflow.com/questions/6797984/how-do-i-lowercase-a-string-in-python)

**2015 Votes**, Benjamin Didur

Use `.lower()` - For example:

```python
s = "Kilometer"
print(s.lower())
```

The official 2.x documentation is here: `str.lower()`
The official 3.x documentation is here: `str.lower()`
