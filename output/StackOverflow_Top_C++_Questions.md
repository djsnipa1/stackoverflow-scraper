# StackOverflow Top C++ Questions


## [Why is it faster to process a sorted array than an unsorted array?](https://stackoverflow.com/questions/11227809/why-is-it-faster-to-process-a-sorted-array-than-an-unsorted-array)

**21298 Votes**, GManNickG

You are a victim of branch prediction fail.


### What is Branch Prediction?

Consider a railroad junction:

Image by Mecanismo, via Wikimedia Commons. Used under the CC-By-SA 3.0 license.
Now for the sake of argument, suppose this is back in the 1800s - before long distance or radio communication.
You are the operator of a junction and you hear a train coming. You have no idea which way it is supposed to go. You stop the train to ask the driver which direction they want. And then you set the switch appropriately.
Trains are heavy and have a lot of inertia. So they take forever to start up and slow down.
Is there a better way? You guess which direction the train will go!

If you guessed right, it continues on.
If you guessed wrong, the captain will stop, back up, and yell at you to flip the switch. Then it can restart down the other path.

If you guess right every time, the train will never have to stop.
If you guess wrong too often, the train will spend a lot of time stopping, backing up, and restarting.

Consider an if-statement: At the processor level, it is a branch instruction:

You are a processor and you see a branch. You have no idea which way it will go. What do you do? You halt execution and wait until the previous instructions are complete. Then you continue down the correct path.
Modern processors are complicated and have long pipelines. So they take forever to "warm up" and "slow down".
Is there a better way? You guess which direction the branch will go!

If you guessed right, you continue executing.
If you guessed wrong, you need to flush the pipeline and roll back to the branch. Then you can restart down the other path.

If you guess right every time, the execution will never have to stop.
If you guess wrong too often, you spend a lot of time stalling, rolling back, and restarting.

This is branch prediction. I admit it's not the best analogy since the train could just signal the direction with a flag. But in computers, the processor doesn't know which direction a branch will go until the last moment.
So how would you strategically guess to minimize the number of times that the train must back up and go down the other path? You look at the past history! If the train goes left 99% of the time, then you guess left. If it alternates, then you alternate your guesses. If it goes one way every 3 times, you guess the same...
In other words, you try to identify a pattern and follow it. This is more or less how branch predictors work.
Most applications have well-behaved branches. So modern branch predictors will typically achieve >90% hit rates. But when faced with unpredictable branches with no recognizable patterns, branch predictors are virtually useless.
Further reading: "Branch predictor" article on Wikipedia.


### As hinted from above, the culprit is this if-statement:


```python
if (data[c] >= 128)
    sum += data[c];
```

Notice that the data is evenly distributed between 0 and 255. 
When the data is sorted, roughly the first half of the iterations will not enter the if-statement. After that, they will all enter the if-statement.
This is very friendly to the branch predictor since the branch consecutively goes the same direction many times.
Even a simple saturating counter will correctly predict the branch except for the few iterations after it switches direction.
Quick visualization:

```python
T = branch taken
N = branch not taken

data[] = 0, 1, 2, 3, 4, ... 126, 127, 128, 129, 130, ... 250, 251, 252, ...
branch = N  N  N  N  N  ...   N    N    T    T    T  ...   T    T    T  ...

       = NNNNNNNNNNNN ... NNNNNNNTTTTTTTTT ... TTTTTTTTTT  (easy to predict)
```

However, when the data is completely random, the branch predictor is rendered useless because it can't predict random data.
Thus there will probably be around 50% misprediction. (no better than random guessing)

```python
data[] = 226, 185, 125, 158, 198, 144, 217, 79, 202, 118,  14, 150, 177, 182, 133, ...
branch =   T,   T,   N,   T,   T,   T,   T,  N,   T,   N,   N,   T,   T,   T,   N  ...

       = TTNTTTTNTNNTTTN ...   (completely random - hard to predict)
```


So what can be done?
If the compiler isn't able to optimize the branch into a conditional move, you can try some hacks if you are willing to sacrifice readability for performance.
Replace:

```python
if (data[c] >= 128)
    sum += data[c];
```

with:

```python
int t = (data[c] - 128) >> 31;
sum += ~t & data[c];
```

This eliminates the branch and replaces it with some bitwise operations.
(Note that this hack is not strictly equivalent to the original if-statement. But in this case, it's valid for all the input values of `data[]`.)
Benchmarks: Core i7 920 @ 3.5 GHz
C++ - Visual Studio 2010 - x64 Release

```python
//  Branch - Random
seconds = 11.777

//  Branch - Sorted
seconds = 2.352

//  Branchless - Random
seconds = 2.564

//  Branchless - Sorted
seconds = 2.587
```

Java - Netbeans 7.1.1 JDK 7 - x64

```python
//  Branch - Random
seconds = 10.93293813

//  Branch - Sorted
seconds = 5.643797077

//  Branchless - Random
seconds = 3.113581453

//  Branchless - Sorted
seconds = 3.186068823
```

Observations:

With the Branch: There is a huge difference between the sorted and unsorted data.
With the Hack: There is no difference between sorted and unsorted data.
In the C++ case, the hack is actually a tad slower than with the branch when the data is sorted.

A general rule of thumb is to avoid data-dependent branching in critical loops. (such as in this example)

Update:

GCC 4.6.1 with `-O3` or `-ftree-vectorize` on x64 is able to generate a conditional move. So there is no difference between the sorted and unsorted data - both are fast.
VC++ 2010 is unable to generate conditional moves for this branch even under `/Ox`.
Intel Compiler 11 does something miraculous. It interchanges the two loops, thereby hoisting the unpredictable branch to the outer loop. So not only is it immune the mispredictions, it is also twice as fast as whatever VC++ and GCC can generate! In other words, ICC took advantage of the test-loop to defeat the benchmark...
If you give the Intel Compiler the branchless code, it just out-right vectorizes it... and is just as fast as with the branch (with the loop interchange).

This goes to show that even mature modern compilers can vary wildly in their ability to optimize code...

## [What is the --> operator in C++?](https://stackoverflow.com/questions/1642028/what-is-the-operator-in-c)

**7607 Votes**, community-wiki

`-->` is not an operator. It is in fact two separate operators, `--` and ``>.
The conditional's code decrements ``x, while returning ``x's original (not decremented) value, and then compares the original value with ``0 using the ``> operator.
To better understand, the statement could be written as follows:

```python
while( (x--) > 0 )
```

## [The Definitive C++ Book Guide and List](https://stackoverflow.com/questions/388242/the-definitive-c-book-guide-and-list)

**4253 Votes**, community-wiki

### Beginner

Introductory, no previous programming experience

C++ Primer * (Stanley Lippman, Jose Lajoie, and Barbara E. Moo)  (updated for C++11) Coming at 1k pages, this is a very thorough introduction into C++ that covers just about everything in the language in a very accessible format and in great detail. The fifth edition (released August 16, 2012) covers C++11. [Review] 
Programming: Principles and Practice Using C++ (Bjarne Stroustrup, 2nd Edition - May 25, 2014) (updated for C++11/C++14) An introduction to programming using C++ by the creator of the language. A good read, that assumes no previous programming experience, but is not only for beginners. 


* Not to be confused with C++ Primer Plus (Stephen Prata), with a significantly less favorable review.

Introductory, with previous programming experience

A Tour of C++ (Bjarne Stroustrup) (2nd edition coming with update for C++17) (EBOOK) The tour is a quick (about 180 pages and 14 chapters) tutorial overview of all of standard C++ (language and standard library, and using C++11) at a moderately high level for people who already know C++ or at least are experienced programmers. This book is an extended version of the material that constitutes Chapters 2-5 of The C++ Programming Language, 4th edition.
Accelerated C++ (Andrew Koenig and Barbara Moo, 1st Edition - August 24, 2000)  This basically covers the same ground as the C++ Primer, but does so on a fourth of its space. This is largely because it does not attempt to be an introduction to programming, but an introduction to C++ for people who've previously programmed in some other language. It has a steeper learning curve, but, for those who can cope with this, it is a very compact introduction to the language. (Historically, it broke new ground by being the first beginner's book to use a modern approach to teaching the language.) Despite this, the C++
it teaches is purely C++98. [Review]

Best practices

Effective C++ (Scott Meyers, 3rd Edition - May 22, 2005)  This was written with the aim of being the best second book C++ programmers should read, and it succeeded. Earlier editions were aimed at programmers coming from C, the third edition changes this and targets programmers coming from languages like Java. It presents ~50 easy-to-remember rules of thumb along with their rationale in a very accessible (and enjoyable) style. For C++11 and C++14 the examples and a few issues are outdated and Effective Modern C++ should be preferred. [Review]
Effective Modern C++ (Scott Meyers) This is basically the new version of Effective C++, aimed at C++ programmers making the transition from C++03 to C++11 and C++14. 
Effective STL (Scott Meyers)  This aims to do the same to the part of the standard library coming from the STL what Effective C++ did to the language as a whole: It presents rules of thumb along with their rationale. [Review]



### Intermediate


More Effective C++ (Scott Meyers) Even more rules of thumb than Effective C++. Not as important as the ones in the first book, but still good to know.
Exceptional C++ (Herb Sutter)  Presented as a set of puzzles, this has one of the best and thorough discussions of the proper resource management and exception safety in C++ through Resource Acquisition is Initialization (RAII) in addition to in-depth coverage of a variety of other topics including the pimpl idiom, name lookup, good class design, and the C++ memory model. [Review]
More Exceptional C++ (Herb Sutter)  Covers additional exception safety topics not covered in Exceptional C++, in addition to discussion of effective object-oriented programming in C++ and correct use of the STL. [Review]
Exceptional C++ Style (Herb Sutter)  Discusses generic programming, optimization, and resource management; this book also has an excellent exposition of how to write modular code in C++ by using non-member functions and the single responsibility principle. [Review]
C++ Coding Standards (Herb Sutter and Andrei Alexandrescu) Coding standards here doesn't mean how many spaces should I indent my code?  This book contains 101 best practices, idioms, and common pitfalls that can help you to write correct, understandable, and efficient C++ code. [Review]
C++ Templates: The Complete Guide (David Vandevoorde and Nicolai M. Josuttis) This is the book about templates as they existed before C++11.  It covers everything from the very basics to some of the most advanced template metaprogramming and explains every detail of how templates work (both conceptually and at how they are implemented) and discusses many common pitfalls.  Has excellent summaries of the One Definition Rule (ODR) and overload resolution in the appendices. A second edition covering C++11, C++14 and C++17 has been already published . [Review]



### Advanced


Modern C++ Design (Andrei Alexandrescu)  A groundbreaking book on advanced generic programming techniques.  Introduces policy-based design, type lists, and fundamental generic programming idioms then explains how many useful design patterns (including small object allocators, functors, factories, visitors, and multi-methods) can be implemented efficiently, modularly, and cleanly using generic programming. [Review]
C++ Template Metaprogramming (David Abrahams and Aleksey Gurtovoy)
C++ Concurrency In Action (Anthony Williams) A book covering C++11 concurrency support including the thread library, the atomics library, the C++ memory model, locks and mutexes, as well as issues of designing and debugging multithreaded applications.
Advanced C++ Metaprogramming (Davide Di Gennaro) A pre-C++11 manual of TMP techniques, focused more on practice than theory.  There are a ton of snippets in this book, some of which are made obsolete by type traits, but the techniques, are nonetheless useful to know.  If you can put up with the quirky formatting/editing, it is easier to read than Alexandrescu, and arguably, more rewarding.  For more experienced developers, there is a good chance that you may pick up something about a dark corner of C++ (a quirk) that usually only comes about through extensive experience.



### Reference Style - All Levels


The C++ Programming Language (Bjarne Stroustrup) (updated for C++11) The classic introduction to C++ by its creator. Written to parallel the classic K&R, this indeed reads very much like it and covers just about everything from the core language to the standard library, to programming paradigms to the language's philosophy. [Review] 
C++ Standard Library Tutorial and Reference (Nicolai Josuttis) (updated for C++11) The introduction and reference for the C++ Standard Library. The second edition (released on April 9, 2012) covers C++11. [Review]
The C++ IO Streams and Locales (Angelika Langer and Klaus Kreft)  There's very little to say about this book except that, if you want to know anything about streams and locales, then this is the one place to find definitive answers. [Review]

C++11/14 References:

The C++ Standard (INCITS/ISO/IEC 14882-2011) This, of course, is the final arbiter of all that is or isn't C++. Be aware, however, that it is intended purely as a reference for experienced users willing to devote considerable time and effort to its understanding. As usual, the first release was quite expensive ($300+ US), but it has now been released in electronic form for $60US.
The C++14 standard is available, but seemingly not in an economical form  directly from the ISO it costs 198 Swiss Francs (about $200 US). For most people, the final draft before standardization is more than adequate (and free). Many will prefer an even newer draft, documenting new features that are likely to be included in C++17.
Overview of the New C++ (C++11/14) (PDF only) (Scott Meyers) (updated for C++1y/C++14) These are the presentation materials (slides and some lecture notes) of a three-day training course offered by Scott Meyers, who's a highly respected author on C++. Even though the list of items is short, the quality is high.
The C++ Core Guidelines (C++11/14/17/) (edited by Bjarne Stroustrup and Herb Sutter) is an evolving online document consisting of a set of guidelines for using modern C++ well. The guidelines are focused on relatively higher-level issues, such as interfaces, resource management, memory management and concurrency affecting application architecture and library design. The project was announced at CppCon'15 by Bjarne Stroustrup and others and welcomes contributions from the community. Most guidelines are supplemented with a rationale and examples as well as discussions of possible tool support. Many rules are designed specifically to be automatically checkable by static analysis tools.
The C++ Super-FAQ (Marshall Cline, Bjarne Stroustrup and others) is an effort by the Standard C++ Foundation to unify the C++ FAQs previously maintained individually by Marshall Cline and Bjarne Stroustrup and also incorporating new contributions. The items mostly address issues at an intermediate level and are often written with a humorous tone. Not all items might be fully up to date with the latest edition of the C++ standard yet.
cppreference.com (C++03/11/14/17/) (initiated by Nate Kohl) is a wiki that summarizes the basic core-language features and has extensive documentation of the C++ standard library. The documentation is very precise but is easier to read than the official standard document and provides better navigation due to its wiki nature. The project documents all versions of the C++ standard and the site allows filtering the display for a specific version. The project was presented by Nate Kohl at CppCon'14.



### Classics / Older

Note: Some information contained within these books may not be up-to-date or no longer considered best practice.

The Design and Evolution of C++ (Bjarne Stroustrup)  If you want to know why the language is the way it is, this book is where you find answers. This covers everything before the standardization of C++.
Ruminations on C++ - (Andrew Koenig and Barbara Moo) [Review]
Advanced C++ Programming Styles and Idioms (James Coplien)  A predecessor of the pattern movement, it describes many C++-specific idioms. It's certainly a very good book and might still be worth a read if you can spare the time, but quite old and not up-to-date with current C++. 
Large Scale C++ Software Design (John Lakos)  Lakos explains techniques to manage very big C++ software projects. Certainly, a good read, if it only was up to date. It was written long before C++ 98 and misses on many features (e.g. namespaces) important for large-scale projects. If you need to work in a big C++ software project, you might want to read it, although you need to take more than a grain of salt with it. The first volume of a new edition is expected in 2018.
Inside the C++ Object Model (Stanley Lippman)  If you want to know how virtual member functions are commonly implemented and how base objects are commonly laid out in memory in a multi-inheritance scenario, and how all this affects performance, this is where you will find thorough discussions of such topics.
The Annotated C++ Reference Manual (Bjarne Stroustrup, Margaret A. Ellis) This book is quite outdated in the fact that it explores the 1989 C++ 2.0 version - Templates, exceptions, namespaces and new casts were not yet introduced. Saying that however, this book goes through the entire C++ standard of the time explaining the rationale, the possible implementations, and features of the language. This is not a book to learn programming principles and patterns on C++, but to understand every aspect of the C++ language.
Thinking in C++ (Bruce Eckel)  Two volumes; is a tutorial style free set of intro level books. Downloads: vol 1, vol 2. Unfortunately they re marred by a number of trivial errors (e.g. maintaining that temporaries are automatically `const`), with no official errata list. A partial 3rd party errata list is available at (http://www.computersciencelab.com/Eckel.htm), but its apparently not maintained.
Scientific and Engineering C++: An Introduction to Advanced Techniques and Examples (John Barton and Lee Nackman) 
It is a comprehensive and very detailed book that tried to explain and make use of all the features available in C++, in the context of numerical methods. It introduced at the time several new techniques, such as the Curiously Recurring Template Pattern (CRTP, also called Barton-Nackman trick).
It pioneered several techniques such as dimensional analysis and automatic differentiation. 
It came with a lot of compilable and useful code, ranging from an expression parser to a Lapack wrapper. 
The code is still available here: http://www.informit.com/store/scientific-and-engineering-c-plus-plus-an-introduction-9780201533934.
Unfortunately, the books have become somewhat outdated in the style and C++ features, however, it was an incredible tour-de-force at the time (1994, pre-STL).
The chapters on dynamics inheritance are a bit complicated to understand and not very useful.
An updated version of this classic book that includes move semantics and the lessons learned from the STL would be very nice.

## [The most elegant way to iterate the words of a string [closed]](https://stackoverflow.com/questions/236129/the-most-elegant-way-to-iterate-the-words-of-a-string)

**2597 Votes**, community-wiki

For what it's worth, here's another way to extract tokens from an input string, relying only on standard library facilities. It's an example of the power and elegance behind the design of the STL.

```python
#include <iostream>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>

int main() {
    using namespace std;
    string sentence = "And I feel fine...";
    istringstream iss(sentence);
    copy(istream_iterator<string>(iss),
         istream_iterator<string>(),
         ostream_iterator<string>(cout, "\n"));
}
```

Instead of copying the extracted tokens to an output stream, one could insert them into a container, using the same generic `copy` algorithm.

```python
vector<string> tokens;
copy(istream_iterator<string>(iss),
     istream_iterator<string>(),
     back_inserter(tokens));
```

... or create the `vector` directly:

```python
vector<string> tokens{istream_iterator<string>{iss},
                      istream_iterator<string>{}};
```

## [What are the differences between a pointer variable and a reference variable in C++?](https://stackoverflow.com/questions/57483/what-are-the-differences-between-a-pointer-variable-and-a-reference-variable-in)

**2547 Votes**, prakash

A pointer can be re-assigned: 

```python
int x = 5;
int y = 6;
int *p;
p =  &x;
p = &y;
*p = 10;
assert(x == 5);
assert(y == 10);
```

A reference cannot, and must be assigned at initialization:

```python
int x = 5;
int y = 6;
int &r = x;
```

A pointer has its own memory address and size on the stack (4 bytes on x86), whereas a reference shares the same memory address (with the original variable) but also takes up some space on the stack.  Since a reference has the same address as the original variable itself, it is safe to think of a reference as another name for the same variable.  Note: What a pointer points to can be on the stack or heap.  Ditto a reference. My claim in this statement is not that a pointer must point to the stack.  A pointer is just a variable that holds a memory address.  This variable is on the stack.  Since a reference has its own space on the stack, and since the address is the same as the variable it references.  More on stack vs heap.  This implies that there is a real address of a reference that the compiler will not tell you. 

```python
int x = 0;
int &r = x;
int *p = &x;
int *p2 = &r;
assert(p == p2);
```

You can have pointers to pointers to pointers offering extra levels of indirection.  Whereas references only offer one level of indirection. 

```python
int x = 0;
int y = 0;
int *p = &x;
int *q = &y;
int **pp = &p;
pp = &q;//*pp = q
**pp = 4;
assert(y == 4);
assert(x == 0);
```

Pointer can be assigned `nullptr` directly, whereas reference cannot. If you try hard enough, and you know how, you can make the address of a reference `nullptr`.  Likewise, if you try hard enough you can have a reference to a pointer, and then that reference can contain `nullptr`.

```python
int *p = nullptr;
int &r = nullptr; <--- compiling error
int &r = *p;  <--- likely no compiling error, especially if the nullptr is hidden behind a function call, yet it refers to a non-existent int at address 0
```

Pointers can iterate over an array, you can use `++` to go to the next item that a pointer is pointing to, and `+ 4` to go to the 5th element.  This is no matter what size the object is that the pointer points to.
A pointer needs to be dereferenced with ``* to access the memory location it points to, whereas a reference can be used directly.  A pointer to a class/struct uses `->` to access it's members whereas a reference uses a ``..
A pointer is a variable that holds a memory address.  Regardless of how a reference is implemented, a reference has the same memory address as the item it references.
References cannot be stuffed into an array, whereas pointers can be (Mentioned by user @litb)
Const references can be bound to temporaries. Pointers cannot (not without some indirection):

```python
const int &x = int(12); //legal C++
int *y = &int(12); //illegal to dereference a temporary.
```

This makes `const&` safer for use in argument lists and so forth.

## [What does the explicit keyword mean?](https://stackoverflow.com/questions/121162/what-does-the-explicit-keyword-mean)

**2302 Votes**, Skizz

The compiler is allowed to make one implicit conversion to resolve the parameters to a function. What this means is that the compiler can use constructors callable with a single parameter to convert from one type to another in order to get the right type for a parameter. 
Here's an example class with a constructor that can be used for implicit conversions:

```python
class Foo
{
public:
  // single parameter constructor, can be used as an implicit conversion
  Foo (int foo) : m_foo (foo) 
  {
  }

  int GetFoo () { return m_foo; }

private:
  int m_foo;
};
```

Here's a simple function that takes a `Foo` object:

```python
void DoBar (Foo foo)
{
  int i = foo.GetFoo ();
}
```

and here's where the `DoBar` function is called.

```python
int main ()
{
  DoBar (42);
}
```

The argument is not a `Foo` object, but an `int`. However, there exists a constructor for `Foo` that takes an `int` so this constructor can be used to convert the parameter to the correct type.
The compiler is allowed to do this once for each parameter.
Prefixing the `explicit` keyword to the constructor prevents the compiler from using that constructor for implicit conversions. Adding it to the above class will create a compiler error at the function call `DoBar (42)`.  It is now necessary to call for conversion explicitly with  `DoBar (Foo (42))`
The reason you might want to do this is to avoid accidental construction that can hide bugs.  Contrived example:

You have a `MyString(int size)` class with a constructor that constructs a string of the given size.  You have a function `print(const MyString&)`, and you call `print(3)` (when you actually intended to call `print("3")`).  You expect it to print "3", but it prints an empty string of length 3 instead.

## [When should static_cast, dynamic_cast, const_cast and reinterpret_cast be used?](https://stackoverflow.com/questions/332030/when-should-static-cast-dynamic-cast-const-cast-and-reinterpret-cast-be-used)

**2001 Votes**, e.James

`static_cast` is the first cast you should attempt to use. It does things like implicit conversions between types (such as `int` to `float`, or pointer to `void*`), and it can also call explicit conversion functions (or implicit ones). In many cases, explicitly stating `static_cast` isn't necessary, but it's important to note that the `T(something)` syntax is equivalent to `(T)something` and should be avoided (more on that later). A `T(something, something_else)` is safe, however, and guaranteed to call the constructor.
`static_cast` can also cast through inheritance hierarchies. It is unnecessary when casting upwards (towards a base class), but when casting downwards it can be used as long as it doesn't cast through `virtual` inheritance. It does not do checking, however, and it is undefined behavior to `static_cast` down a hierarchy to a type that isn't actually the type of the object.

`const_cast` can be used to remove or add `const` to a variable; no other C++ cast is capable of removing it (not even `reinterpret_cast`). It is important to note that modifying a formerly `const` value is only undefined if the original variable is `const`; if you use it to take the `const` off a reference to something that wasn't declared with `const`, it is safe. This can be useful when overloading member functions based on `const`, for instance. It can also be used to add `const` to an object, such as to call a member function overload.
`const_cast` also works similarly on `volatile`, though that's less common.

`dynamic_cast` is almost exclusively used for handling polymorphism. You can cast a pointer or reference to any polymorphic type to any other class type (a polymorphic type has at least one virtual function, declared or inherited). You can use it for more than just casting downwards -- you can cast sideways or even up another chain. The `dynamic_cast` will seek out the desired object and return it if possible. If it can't, it will return `nullptr` in the case of a pointer, or throw `std::bad_cast` in the case of a reference.
`dynamic_cast` has some limitations, though. It doesn't work if there are multiple objects of the same type in the inheritance hierarchy (the so-called 'dreaded diamond') and you aren't using `virtual` inheritance. It also can only go through public inheritance - it will always fail to travel through `protected` or `private` inheritance. This is rarely an issue, however, as such forms of inheritance are rare.

`reinterpret_cast` is the most dangerous cast, and should be used very sparingly. It turns one type directly into another - such as casting the value from one pointer to another, or storing a pointer in an `int`, or all sorts of other nasty things. Largely, the only guarantee you get with `reinterpret_cast` is that normally if you cast the result back to the original type, you will get the exact same value (but not if the intermediate type is smaller than the original type). There are a number of conversions that `reinterpret_cast` cannot do, too. It's used primarily for particularly weird conversions and bit manipulations, like turning a raw data stream into actual data, or storing data in the low bits of an aligned pointer.

C-style cast and function-style cast are casts using `(type)object` or `type(object)`, respectively. A C-style cast is defined as the first of the following which succeeds:

`const_cast`
`static_cast` (though ignoring access restrictions)
`static_cast` (see above), then `const_cast`
`reinterpret_cast`
`reinterpret_cast`, then `const_cast`

It can therefore be used as a replacement for other casts in some instances, but can be extremely dangerous because of the ability to devolve into a `reinterpret_cast`, and the latter should be preferred when explicit casting is needed, unless you are sure `static_cast` will succeed or `reinterpret_cast` will fail. Even then, consider the longer, more explicit option.
C-style casts also ignore access control when performing a `static_cast`, which means that they have the ability to perform an operation that no other cast can. This is mostly a kludge, though, and in my mind is just another reason to avoid C-style casts.

## [How do you set, clear, and toggle a single bit?](https://stackoverflow.com/questions/47981/how-do-you-set-clear-and-toggle-a-single-bit)

**1992 Votes**, JeffV

Setting a bit
Use the bitwise OR operator (``|) to set a bit.

```python
number |= 1UL << x;
```

That will set bit ``x.
Use `1ULL` if `number` is wider than `unsigned long`; promotion of `1UL << x` doesn't happen until after evaluating `1UL << x` where it's undefined behaviour to shift by more than the width of a `long`.  The same applies to all the rest of the examples.
Clearing a bit
Use the bitwise AND operator (``&) to clear a bit.

```python
number &= ~(1UL << x);
```

That will clear bit ``x. You must invert the bit string with the bitwise NOT operator (``~), then AND it.
Toggling a bit
The XOR operator (``^) can be used to toggle a bit.

```python
number ^= 1UL << x;
```

That will toggle bit ``x.
Checking a bit
You didn't ask for this, but I might as well add it.
To check a bit, shift the number x to the right, then bitwise AND it:

```python
bit = (number >> x) & 1U;
```

That will put the value of bit ``x into the variable `bit`.
Changing the nth bit to x
Setting the ``nth bit to either ``1 or ``0 can be achieved with the following on a 2's complement C++ implementation:

```python
number ^= (-x ^ number) & (1UL << n);
```

Bit ``n will be set if ``x is ``1, and cleared if ``x is ``0.  If ``x has some other value, you get garbage.  `x = !!x` will booleanize it to 0 or 1.
To make this independent of 2's complement negation behaviour (where `-1` has all bits set, unlike on a 1's complement or sign/magnitude C++ implementation), use unsigned negation.

```python
number ^= (-(unsigned long)x ^ number) & (1UL << n);
```

or

```python
unsigned long newbit = !!x;    // Also booleanize to force 0 or 1
number ^= (-newbit ^ number) & (1UL << n);
```

It's generally a good idea to use unsigned types for portable bit manipulation.
It's also generally a good idea to not to copy/paste code in general and so many people use preprocessor macros (like the community wiki answer further down) or some sort of encapsulation.

## [Why is using namespace std considered bad practice?](https://stackoverflow.com/questions/1452721/why-is-using-namespace-std-considered-bad-practice)

**1973 Votes**, akbiggs

This is not related to performance at all. But consider this: you are using two libraries called Foo and Bar:

```python
using namespace foo;
using namespace bar;
```

Everything works fine, you can call `Blah()` from Foo and `Quux()` from Bar without problems. But one day you upgrade to a new version of Foo 2.0, which now offers a function called `Quux()`. Now you've got a conflict: Both Foo 2.0 and Bar import `Quux()` into your global namespace. This is going to take some effort to fix, especially if the function parameters happen to match.
If you had used `foo::Blah()` and `bar::Quux()`, then the introduction of `foo::Quux()` would have been a non-event.

## [Why are elementwise additions much faster in separate loops than in a combined loop?](https://stackoverflow.com/questions/8547778/why-are-elementwise-additions-much-faster-in-separate-loops-than-in-a-combined-l)

**1961 Votes**, Johannes Gerer

Upon further analysis of this, I believe this is (at least partially) caused by data alignment of the four pointers. This will cause some level of cache bank/way conflicts.
If I've guessed correctly on how you are allocating your arrays, they are likely to be aligned to the page line.
This means that all your accesses in each loop will fall on the same cache way. However, Intel processors have had 8-way L1 cache associativity for a while. But in reality, the performance isn't completely uniform. Accessing 4-ways is still slower than say 2-ways.
EDIT : It does in fact look like you are allocating all the arrays separately.
Usually when such large allocations are requested, the allocator will request fresh pages from the OS. Therefore, there is a high chance that large allocations will appear at the same offset from a page-boundary.
Here's the test code:

```python
int main(){
    const int n = 100000;

#ifdef ALLOCATE_SEPERATE
    double *a1 = (double*)malloc(n * sizeof(double));
    double *b1 = (double*)malloc(n * sizeof(double));
    double *c1 = (double*)malloc(n * sizeof(double));
    double *d1 = (double*)malloc(n * sizeof(double));
#else
    double *a1 = (double*)malloc(n * sizeof(double) * 4);
    double *b1 = a1 + n;
    double *c1 = b1 + n;
    double *d1 = c1 + n;
#endif

    //  Zero the data to prevent any chance of denormals.
    memset(a1,0,n * sizeof(double));
    memset(b1,0,n * sizeof(double));
    memset(c1,0,n * sizeof(double));
    memset(d1,0,n * sizeof(double));

    //  Print the addresses
    cout << a1 << endl;
    cout << b1 << endl;
    cout << c1 << endl;
    cout << d1 << endl;

    clock_t start = clock();

    int c = 0;
    while (c++ < 10000){

#if ONE_LOOP
        for(int j=0;j<n;j++){
            a1[j] += b1[j];
            c1[j] += d1[j];
        }
#else
        for(int j=0;j<n;j++){
            a1[j] += b1[j];
        }
        for(int j=0;j<n;j++){
            c1[j] += d1[j];
        }
#endif

    }

    clock_t end = clock();
    cout << "seconds = " << (double)(end - start) / CLOCKS_PER_SEC << endl;

    system("pause");
    return 0;
}
```


Benchmark Results:
EDIT: Results on an actual Core 2 architecture machine:
2 x Intel Xeon X5482 Harpertown @ 3.2 GHz:

```python
#define ALLOCATE_SEPERATE
#define ONE_LOOP
00600020
006D0020
007A0020
00870020
seconds = 6.206

#define ALLOCATE_SEPERATE
//#define ONE_LOOP
005E0020
006B0020
00780020
00850020
seconds = 2.116

//#define ALLOCATE_SEPERATE
#define ONE_LOOP
00570020
00633520
006F6A20
007B9F20
seconds = 1.894

//#define ALLOCATE_SEPERATE
//#define ONE_LOOP
008C0020
00983520
00A46A20
00B09F20
seconds = 1.993
```

Observations:

6.206 seconds with one loop and 2.116 seconds with two loops. This reproduces the OP's results exactly.
In the first two tests, the arrays are allocated separately. You'll notice that they all have the same alignment relative to the page.
In the second two tests, the arrays are packed together to break that alignment. Here you'll notice both loops are faster. Furthermore, the second (double) loop is now the slower one as you would normally expect.

As @Stephen Cannon points out in the comments, there is very likely possibility that this alignment causes false aliasing in the load/store units or the cache. I Googled around for this and found that Intel actually has a hardware counter for partial address aliasing stalls:
http://software.intel.com/sites/products/documentation/doclib/stdxe/2013/~amplifierxe/pmw_dp/events/partial_address_alias.html

5 Regions - Explanations
Region 1:
This one is easy. The dataset is so small that the performance is dominated by overhead like looping and branching.
Region 2:
Here, as the data sizes increases, the amount of relative overhead goes down and the performance "saturates". Here two loops is slower because it has twice as much loop and branching overhead.
I'm not sure exactly what's going on here... Alignment could still play an effect as Agner Fog mentions cache bank conflicts. (That link is about Sandy Bridge, but the idea should still be applicable to Core 2.)
Region 3:
At this point, the data no longer fits in L1 cache. So performance is capped by the L1 <-> L2 cache bandwidth.
Region 4:
The performance drop in the single-loop is what we are observing. And as mentioned, this is due to the alignment which (most likely) causes false aliasing stalls in the processor load/store units.
However, in order for false aliasing to occur, there must be a large enough stride between the datasets. This is why you don't see this in region 3.
Region 5:
At this point, nothing fits in cache. So you're bound by memory bandwidth.

## [What are the basic rules and idioms for operator overloading?](https://stackoverflow.com/questions/4421706/what-are-the-basic-rules-and-idioms-for-operator-overloading)

**1807 Votes**, sbi

Common operators to overload
Most of the work in overloading operators is boiler-plate code. That is little wonder, since operators are merely syntactic sugar, their actual work could be done by (and often is forwarded to) plain functions. But it is important that you get this boiler-plate code right. If you fail, either your operators code wont compile or your users code wont compile or your users code will behave surprisingly.

### Assignment Operator

There's a lot to be said about assignment. However, most of it has already been said in GMan's famous Copy-And-Swap FAQ, so I'll skip most of it here, only listing the perfect assignment operator for reference:

```python
X& X::operator=(X rhs)
{
  swap(rhs);
  return *this;
}
```


### Bitshift Operators (used for Stream I/O)

The bitshift operators `<<` and `>>`, although still used in hardware interfacing for the bit-manipulation functions they inherit from C, have become more prevalent as overloaded stream input and output operators in most applications.  For guidance overloading as bit-manipulation operators, see the section below on Binary Arithmetic Operators.  For implementing your own custom format and parsing logic when your object is used with iostreams, continue.
The stream operators, among the most commonly overloaded operators, are binary infix operators for which the syntax specifies no restriction on whether they should be members or non-members.
Since they change their left argument (they alter the streams state), they should, according to the rules of thumb, be implemented as members of their left operands type. However, their left operands are streams from the standard library, and while most of the stream output and input operators defined by the standard library are indeed defined as members of the stream classes, when you implement output and input operations for your own types, you cannot change the standard librarys stream types. Thats why you need to implement these operators for your own types as non-member functions.
The canonical forms of the two are these:

```python
std::ostream& operator<<(std::ostream& os, const T& obj)
{
  // write obj to stream

  return os;
}

std::istream& operator>>(std::istream& is, T& obj)
{
  // read obj from stream

  if( /* no valid object of T found in stream */ )
    is.setstate(std::ios::failbit);

  return is;
}
```

When implementing `operator>>`, manually setting the streams state is only necessary when the reading itself succeeded, but the result is not what would be expected.

### Function call operator

The function call operator, used to create function objects, also known as functors, must be defined as a member function, so it always has the implicit `this` argument of member functions. Other than this it can be overloaded to take any number of additional arguments, including zero.
Here's an example of the syntax:

```python
class foo {
public:
    // Overloaded call operator
    int operator()(const std::string& y) {
        // ...
    }
};
```

Usage:

```python
foo f;
int a = f("hello");
```

Throughout the C++ standard library, function objects are always copied. Your own function objects should therefore be cheap to copy. If a function object absolutely needs to use data which is expensive to copy, it is better to store that data elsewhere and have the function object refer to it.

### Comparison operators

The binary infix comparison operators should, according to the rules of thumb, be implemented as non-member functions1. The unary prefix negation ``! should (according to the same rules) be implemented as a member function. (but it is usually not a good idea to overload it.)
The standard librarys algorithms (e.g. `std::sort()`) and types (e.g. `std::map`) will always only expect `operator<` to be present. However, the users of your type will expect all the other operators to be present, too, so if you define `operator<`, be sure to follow the third fundamental rule of operator overloading and also define all the other boolean comparison operators. The canonical way to implement them is this:

```python
inline bool operator==(const X& lhs, const X& rhs){ /* do actual comparison */ }
inline bool operator!=(const X& lhs, const X& rhs){return !operator==(lhs,rhs);}
inline bool operator< (const X& lhs, const X& rhs){ /* do actual comparison */ }
inline bool operator> (const X& lhs, const X& rhs){return  operator< (rhs,lhs);}
inline bool operator<=(const X& lhs, const X& rhs){return !operator> (lhs,rhs);}
inline bool operator>=(const X& lhs, const X& rhs){return !operator< (lhs,rhs);}
```

The important thing to note here is that only two of these operators actually do anything, the others are just forwarding their arguments to either of these two to do the actual work.
The syntax for overloading the remaining binary boolean operators (`||`, `&&`) follows the rules of the comparison operators. However, it is very unlikely that you would find a reasonable use case for these2.
1 As with all rules of thumb, sometimes there might be reasons to break this one, too. If so, do not forget that the left-hand operand of the binary comparison operators, which for member functions will be `*this`, needs to be `const`, too. So a comparison operator implemented as a member function would have to have this signature:

```python
bool operator<(const X& rhs) const { /* do actual comparison with *this */ }
```

(Note the `const` at the end.)
2 It should be noted that the built-in version of `||` and `&&` use shortcut semantics. While the user defined ones (because they are syntactic sugar for method calls) do not use shortcut semantics. User will expect these operators to have shortcut semantics, and their code may depend on it, Therefore it is highly advised NEVER to define them.

### Arithmetic Operators

Unary arithmetic operators
The unary increment and decrement operators come in both prefix and postfix flavor. To tell one from the other, the postfix variants take an additional dummy int argument. If you overload increment or decrement, be sure to always implement both prefix and postfix versions.
Here is the canonical implementation of increment, decrement follows the same rules:

```python
class X {
  X& operator++()
  {
    // do actual increment
    return *this;
  }
  X operator++(int)
  {
    X tmp(*this);
    operator++();
    return tmp;
  }
};
```

Note that the postfix variant is implemented in terms of prefix. Also note that postfix does an extra copy.2
Overloading unary minus and plus is not very common and probably best avoided. If needed, they should probably be overloaded as member functions. 
2 Also note that the postfix variant does more work and is therefore less efficient to use than the prefix variant. This is a good reason to generally prefer prefix increment over postfix increment. While compilers can usually optimize away the additional work of postfix increment for built-in types, they might not be able to do the same for user-defined types (which could be something as innocently looking as a list iterator). Once you got used to do `i++`, it becomes very hard to remember to do `++i` instead when ``i is not of a built-in type (plus you'd have to change code when changing a type), so it is better to make a habit of always using prefix increment, unless postfix is explicitly needed.
Binary arithmetic operators
For the binary arithmetic operators, do not forget to obey the third basic rule operator overloading: If you provide ``+, also provide `+=`, if you provide ``-, do not omit `-=`, etc. Andrew Koenig is said to have been the first to observe that the compound assignment operators can be used as a base for their non-compound counterparts. That is, operator ``+ is implemented in terms of `+=`, ``- is implemented in terms of `-=` etc.
According to our rules of thumb, ``+ and its companions should be non-members, while their compound assignment counterparts (`+=` etc.), changing their left argument, should be a member. Here is the exemplary code for `+=` and ``+, the other binary arithmetic operators should be implemented in the same way:

```python
class X {
  X& operator+=(const X& rhs)
  {
    // actual addition of rhs to *this
    return *this;
  }
};
inline X operator+(X lhs, const X& rhs)
{
  lhs += rhs;
  return lhs;
}
```

`operator+=` returns its result per reference, while `operator+` returns a copy of its result. Of course, returning a reference is usually more efficient than returning a copy, but in the case of `operator+`, there is no way around the copying. When you write `a + b`, you expect the result to be a new value, which is why `operator+` has to return a new value.3
Also note that `operator+` takes its left operand by copy rather than by const reference. The reason for this is the same as the reason giving for `operator=` taking its argument per copy.
The bit manipulation operators ``~ ``& ``| ``^ `<<` `>>` should be implemented in the same way as the arithmetic operators. However, (except for overloading `<<` and `>>` for output and input) there are very few reasonable use cases for overloading these.
3 Again, the lesson to be taken from this is that `a += b` is, in general, more efficient than `a + b` and should be preferred if possible.

### Array Subscripting

The array subscript operator is a binary operator which must be implemented as a class member. It is used for container-like types that allow access to their data elements by a key.
The canonical form of providing these is this:

```python
class X {
        value_type& operator[](index_type idx);
  const value_type& operator[](index_type idx) const;
  // ...
};
```

Unless you do not want users of your class to be able to change data elements returned by `operator[]` (in which case you can omit the non-const variant), you should always provide both variants of the operator.
If value_type is known to refer to a built-in type, the const variant of the operator should return a copy instead of a const reference.

### Operators for Pointer-like Types

For defining your own iterators or smart pointers, you have to overload the unary prefix dereference operator ``* and the binary infix pointer member access operator `->`:

```python
class my_ptr {
        value_type& operator*();
  const value_type& operator*() const;
        value_type* operator->();
  const value_type* operator->() const;
};
```

Note that these, too, will almost always need both a const and a non-const version.
For the `->` operator, if `value_type` is of `class` (or `struct` or `union`) type, another `operator->()` is called recursively, until an `operator->()` returns a value of non-class type.
The unary address-of operator should never be overloaded.
For `operator->*()` see this question. It's rarely used and thus rarely ever overloaded. In fact, even iterators do not overload it.

Continue to Conversion Operators

## [What is The Rule of Three?](https://stackoverflow.com/questions/4172722/what-is-the-rule-of-three)

**1804 Votes**, fredoverflow

Introduction
C++ treats variables of user-defined types with value semantics.
This means that objects are implicitly copied in various contexts,
and we should understand what "copying an object" actually means.
Let us consider a simple example:

```python
class person
{
    std::string name;
    int age;

public:

    person(const std::string& name, int age) : name(name), age(age)
    {
    }
};

int main()
{
    person a("Bjarne Stroustrup", 60);
    person b(a);   // What happens here?
    b = a;         // And here?
}
```

(If you are puzzled by the `name(name), age(age)` part,
this is called a member initializer list.)
Special member functions
What does it mean to copy a `person` object?
The `main` function shows two distinct copying scenarios.
The initialization `person b(a);` is performed by the copy constructor.
Its job is to construct a fresh object based on the state of an existing object.
The assignment `b = a` is performed by the copy assignment operator.
Its job is generally a little more complicated,
because the target object is already in some valid state that needs to be dealt with.
Since we declared neither the copy constructor nor the assignment operator (nor the destructor) ourselves,
these are implicitly defined for us. Quote from the standard:

The [...] copy constructor and copy assignment operator, [...] and destructor are special member functions.
  [ Note: The implementation will implicitly declare these member functions
  for some class types when the program does not explicitly declare them.
  The implementation will implicitly define them if they are used. [...] end note ]
  [n3126.pdf section 12 1]

By default, copying an object means copying its members:

The implicitly-defined copy constructor for a non-union class X performs a memberwise copy of its subobjects.
  [n3126.pdf section 12.8 16]
The implicitly-defined copy assignment operator for a non-union class X performs memberwise copy assignment
  of its subobjects.
  [n3126.pdf section 12.8 30]


### Implicit definitions

The implicitly-defined special member functions for `person` look like this:

```python
// 1. copy constructor
person(const person& that) : name(that.name), age(that.age)
{
}

// 2. copy assignment operator
person& operator=(const person& that)
{
    name = that.name;
    age = that.age;
    return *this;
}

// 3. destructor
~person()
{
}
```

Memberwise copying is exactly what we want in this case:
`name` and `age` are copied, so we get a self-contained, independent `person` object.
The implicitly-defined destructor is always empty.
This is also fine in this case since we did not acquire any resources in the constructor.
The members' destructors are implicitly called after the `person` destructor is finished:

After executing the body of the destructor and destroying any automatic objects allocated within the body,
  a destructor for class X calls the destructors for X's direct [...] members
  [n3126.pdf 12.4 6]

Managing resources
So when should we declare those special member functions explicitly?
When our class manages a resource, that is,
when an object of the class is responsible for that resource.
That usually means the resource is acquired in the constructor
(or passed into the constructor) and released in the destructor.
Let us go back in time to pre-standard C++.
There was no such thing as `std::string`, and programmers were in love with pointers.
The `person` class might have looked like this:

```python
class person
{
    char* name;
    int age;

public:

    // the constructor acquires a resource:
    // in this case, dynamic memory obtained via new[]
    person(const char* the_name, int the_age)
    {
        name = new char[strlen(the_name) + 1];
        strcpy(name, the_name);
        age = the_age;
    }

    // the destructor must release this resource via delete[]
    ~person()
    {
        delete[] name;
    }
};
```

Even today, people still write classes in this style and get into trouble:
"I pushed a person into a vector and now I get crazy memory errors!"
Remember that by default, copying an object means copying its members,
but copying the `name` member merely copies a pointer, not the character array it points to!
This has several unpleasant effects:

Changes via ``a can be observed via ``b.
Once ``b is destroyed, `a.name` is a dangling pointer.
If ``a is destroyed, deleting the dangling pointer yields undefined behavior.
Since the assignment does not take into account what `name` pointed to before the assignment,
sooner or later you will get memory leaks all over the place.


### Explicit definitions

Since memberwise copying does not have the desired effect, we must define the copy constructor and the copy assignment operator explicitly to make deep copies of the character array:

```python
// 1. copy constructor
person(const person& that)
{
    name = new char[strlen(that.name) + 1];
    strcpy(name, that.name);
    age = that.age;
}

// 2. copy assignment operator
person& operator=(const person& that)
{
    if (this != &that)
    {
        delete[] name;
        // This is a dangerous point in the flow of execution!
        // We have temporarily invalidated the class invariants,
        // and the next statement might throw an exception,
        // leaving the object in an invalid state :(
        name = new char[strlen(that.name) + 1];
        strcpy(name, that.name);
        age = that.age;
    }
    return *this;
}
```

Note the difference between initialization and assignment:
we must tear down the old state before assigning to `name` to prevent memory leaks.
Also, we have to protect against self-assignment of the form `x = x`.
Without that check, `delete[] name` would delete the array containing the source string,
because when you write `x = x`, both `this->name` and `that.name` contain the same pointer.

### Exception safety

Unfortunately, this solution will fail if `new char[...]` throws an exception due to memory exhaustion.
One possible solution is to introduce a local variable and reorder the statements:

```python
// 2. copy assignment operator
person& operator=(const person& that)
{
    char* local_name = new char[strlen(that.name) + 1];
    // If the above statement throws,
    // the object is still in the same state as before.
    // None of the following statements will throw an exception :)
    strcpy(local_name, that.name);
    delete[] name;
    name = local_name;
    age = that.age;
    return *this;
}
```

This also takes care of self-assignment without an explicit check.
An even more robust solution to this problem is the copy-and-swap idiom,
but I will not go into the details of exception safety here.
I only mentioned exceptions to make the following point: Writing classes that manage resources is hard.

### Noncopyable resources

Some resources cannot or should not be copied, such as file handles or mutexes.
In that case, simply declare the copy constructor and copy assignment operator as `private` without giving a definition:

```python
private:

    person(const person& that);
    person& operator=(const person& that);
```

Alternatively, you can inherit from `boost::noncopyable` or declare them as deleted (C++0x):

```python
person(const person& that) = delete;
person& operator=(const person& that) = delete;
```


### The rule of three

Sometimes you need to implement a class that manages a resource.
(Never manage multiple resources in a single class,
this will only lead to pain.)
In that case, remember the rule of three:

If you need to explicitly declare either the destructor,
  copy constructor or copy assignment operator yourself,
  you probably need to explicitly declare all three of them.

(Unfortunately, this "rule" is not enforced by the C++ standard or any compiler I am aware of.)
Advice
Most of the time, you do not need to manage a resource yourself,
because an existing class such as `std::string` already does it for you.
Just compare the simple code using a `std::string` member
to the convoluted and error-prone alternative using a `char*` and you should be convinced.
As long as you stay away from raw pointer members, the rule of three is unlikely to concern your own code.

## [What is the difference between #include <filename> and #include filename?](https://stackoverflow.com/questions/21593/what-is-the-difference-between-include-filename-and-include-filename)

**1748 Votes**, quest49

In practice, the difference is in the location where the preprocessor searches for the included file. 
For `#include <filename>` the preprocessor searches in an implementation dependent manner, normally in search directories pre-designated by the compiler/IDE. This method is normally used to include standard library header files.
For `#include "filename"` the preprocessor searches first in the same directory as the file containing the directive, and then follows the search path used for the `#include <filename>` form. This method is normally used to include programmer-defined header files.
A more complete description is available in the GCC documentation on search paths.

## [What is the copy-and-swap idiom?](https://stackoverflow.com/questions/3279543/what-is-the-copy-and-swap-idiom)

**1629 Votes**, GManNickG

### Overview

Why do we need the copy-and-swap idiom?
Any class that manages a resource (a wrapper, like a smart pointer) needs to implement The Big Three. While the goals and implementation of the copy-constructor and destructor are straightforward, the copy-assignment operator is arguably the most nuanced and difficult. How should it be done? What pitfalls need to be avoided?
The copy-and-swap idiom is the solution, and elegantly assists the assignment operator in achieving two things: avoiding code duplication, and providing a strong exception guarantee.
How does it work?
Conceptually, it works by using the copy-constructor's functionality to create a local copy of the data, then takes the copied data with a `swap` function, swapping the old data with the new data. The temporary copy then destructs, taking the old data with it. We are left with a copy of the new data.
In order to use the copy-and-swap idiom, we need three things: a working copy-constructor, a working destructor (both are the basis of any wrapper, so should be complete anyway), and a `swap` function.
A swap function is a non-throwing function that swaps two objects of a class, member for member. We might be tempted to use `std::swap` instead of providing our own, but this would be impossible; `std::swap` uses the copy-constructor and copy-assignment operator within its implementation, and we'd ultimately be trying to define the assignment operator in terms of itself!
(Not only that, but unqualified calls to `swap` will use our custom swap operator, skipping over the unnecessary construction and destruction of our class that `std::swap` would entail.)


### An in-depth explanation

The goal
Let's consider a concrete case. We want to manage, in an otherwise useless class, a dynamic array. We start with a working constructor, copy-constructor, and destructor:

```python
#include <algorithm> // std::copy
#include <cstddef> // std::size_t

class dumb_array
{
public:
    // (default) constructor
    dumb_array(std::size_t size = 0)
        : mSize(size),
          mArray(mSize ? new int[mSize]() : nullptr)
    {
    }

    // copy-constructor
    dumb_array(const dumb_array& other)
        : mSize(other.mSize),
          mArray(mSize ? new int[mSize] : nullptr),
    {
        // note that this is non-throwing, because of the data
        // types being used; more attention to detail with regards
        // to exceptions must be given in a more general case, however
        std::copy(other.mArray, other.mArray + mSize, mArray);
    }

    // destructor
    ~dumb_array()
    {
        delete [] mArray;
    }

private:
    std::size_t mSize;
    int* mArray;
};
```

This class almost manages the array successfully, but it needs `operator=` to work correctly.
A failed solution
Here's how a naive implementation might look:

```python
// the hard part
dumb_array& operator=(const dumb_array& other)
{
    if (this != &other) // (1)
    {
        // get rid of the old data...
        delete [] mArray; // (2)
        mArray = nullptr; // (2) *(see footnote for rationale)

        // ...and put in the new
        mSize = other.mSize; // (3)
        mArray = mSize ? new int[mSize] : nullptr; // (3)
        std::copy(other.mArray, other.mArray + mSize, mArray); // (3)
    }

    return *this;
}
```

And we say we're finished; this now manages an array, without leaks. However, it suffers from three problems, marked sequentially in the code as `(n)`.

The first  is the self-assignment test. This check serves two purposes: it's an easy way to prevent us from running needless code on self-assignment, and it protects us from subtle bugs (such as deleting the array only to try and copy it). But in all other cases it merely serves to slow the program down, and act as noise in the code; self-assignment rarely occurs, so most of the time this check is a waste. It would be better if the operator could work properly without it.
The second is that it only provides a basic exception guarantee. If `new int[mSize]` fails, `*this` will have been modified. (Namely, the size is wrong and the data is gone!) For a strong exception guarantee, it would need to be something akin to:

```python
dumb_array& operator=(const dumb_array& other)
{
    if (this != &other) // (1)
    {
        // get the new data ready before we replace the old
        std::size_t newSize = other.mSize;
        int* newArray = newSize ? new int[newSize]() : nullptr; // (3)
        std::copy(other.mArray, other.mArray + newSize, newArray); // (3)

        // replace the old data (all are non-throwing)
        delete [] mArray;
        mSize = newSize;
        mArray = newArray;
    }

    return *this;
}
```

The code has expanded! Which leads us to the third problem: code duplication. Our assignment operator effectively duplicates all the code we've already written elsewhere, and that's a terrible thing.

In our case, the core of it is only two lines (the allocation and the copy), but with more complex resources this code bloat can be quite a hassle. We should strive to never repeat ourselves.
(One might wonder: if this much code is needed to manage one resource correctly, what if my class manages more than one? While this may seem to be a valid concern, and indeed it requires non-trivial `try`/`catch` clauses, this is a non-issue. That's because a class should manage one resource only!)
A successful solution
As mentioned, the copy-and-swap idiom will fix all these issues. But right now, we have all the requirements except one: a `swap` function. While The Rule of Three successfully entails the existence of our copy-constructor, assignment operator, and destructor, it should really be called "The Big Three and A Half": any time your class manages a resource it also makes sense to provide a `swap` function.
We need to add swap functionality to our class, and we do that as follows:

```python
class dumb_array
{
public:
    // ...

    friend void swap(dumb_array& first, dumb_array& second) // nothrow
    {
        // enable ADL (not necessary in our case, but good practice)
        using std::swap;

        // by swapping the members of two objects,
        // the two objects are effectively swapped
        swap(first.mSize, second.mSize);
        swap(first.mArray, second.mArray);
    }

    // ...
};
```

(Here is the explanation why `public friend swap`.) Now not only can we swap our `dumb_array`'s, but swaps in general can be more efficient; it merely swaps pointers and sizes, rather than allocating and copying entire arrays. Aside from this bonus in functionality and efficiency, we are now ready to implement the copy-and-swap idiom.
Without further ado, our assignment operator is:

```python
dumb_array& operator=(dumb_array other) // (1)
{
    swap(*this, other); // (2)

    return *this;
}
```

And that's it! With one fell swoop, all three problems are elegantly tackled at once.
Why does it work?
We first notice an important choice: the parameter argument is taken by-value. While one could just as easily do the following (and indeed, many naive implementations of the idiom do):

```python
dumb_array& operator=(const dumb_array& other)
{
    dumb_array temp(other);
    swap(*this, temp);

    return *this;
}
```

We lose an important optimization opportunity. Not only that, but this choice is critical in C++11, which is discussed later. (On a general note, a remarkably useful guideline is as follows: if you're going to make a copy of something in a function, let the compiler do it in the parameter list.)
Either way, this method of obtaining our resource is the key to eliminating code duplication: we get to use the code from the copy-constructor to make the copy, and never need to repeat any bit of it. Now that the copy is made, we are ready to swap.
Observe that upon entering the function that all the new data is already allocated, copied, and ready to be used. This is what gives us a strong exception guarantee for free: we won't even enter the function if construction of the copy fails, and it's therefore not possible to alter the state of `*this`. (What we did manually before for a strong exception guarantee, the compiler is doing for us now; how kind.)
At this point we are home-free, because `swap` is non-throwing. We swap our current data with the copied data, safely altering our state, and the old data gets put into the temporary. The old data is then released when the function returns. (Where upon the parameter's scope ends and its destructor is called.)
Because the idiom repeats no code, we cannot introduce bugs within the operator. Note that this means we are rid of the need for a self-assignment check, allowing a single uniform implementation of `operator=`. (Additionally, we no longer have a performance penalty on non-self-assignments.)
And that is the copy-and-swap idiom.

### What about C++11?

The next version of C++, C++11, makes one very important change to how we manage resources: the Rule of Three is now The Rule of Four (and a half). Why? Because not only do we need to be able to copy-construct our resource, we need to move-construct it as well.
Luckily for us, this is easy:

```python
class dumb_array
{
public:
    // ...

    // move constructor
    dumb_array(dumb_array&& other)
        : dumb_array() // initialize via default constructor, C++11 only
    {
        swap(*this, other);
    }

    // ...
};
```

What's going on here? Recall the goal of move-construction: to take the resources from another instance of the class, leaving it in a state guaranteed to be assignable and destructible.
So what we've done is simple: initialize via the default constructor (a C++11 feature), then swap with `other`; we know a default constructed instance of our class can safely be assigned and destructed, so we know `other` will be able to do the same, after swapping.
(Note that some compilers do not support constructor delegation; in this case, we have to manually default construct the class. This is an unfortunate but luckily trivial task.)
Why does that work?
That is the only change we need to make to our class, so why does it work? Remember the ever-important decision we made to make the parameter a value and not a reference:

```python
dumb_array& operator=(dumb_array other); // (1)
```

Now, if `other` is being initialized with an rvalue, it will be move-constructed. Perfect. In the same way C++03 let us re-use our copy-constructor functionality by taking the argument by-value, C++11 will automatically pick the move-constructor when appropriate as well. (And, of course, as mentioned in previously linked article, the copying/moving of the value may simply be elided altogether.)
And so concludes the copy-and-swap idiom.

Footnotes
*Why do we set `mArray` to null? Because if any further code in the operator throws, the destructor of `dumb_array` might be called; and if that happens without setting it to null, we attempt to delete memory that's already been deleted! We avoid this by setting it to null, as deleting null is a no-operation.
There are other claims that we should specialize `std::swap` for our type, provide an in-class `swap` along-side a free-function `swap`, etc. But this is all unnecessary: any proper use of `swap` will be through an unqualified call, and our function will be found through ADL. One function will do.
The reason is simple: once you have the resource to yourself, you may swap and/or move it (C++11) anywhere it needs to be. And by making the copy in the parameter list, you maximize optimization.

## [Cycles in family tree software](https://stackoverflow.com/questions/6163683/cycles-in-family-tree-software)

**1594 Votes**, Partick Hse

It seems you (and/or your company) have a fundamental misunderstanding of what a family tree is supposed to be. 
Let me clarify, I also work for a company that has (as one of its products) a family tree in its portfolio, and we have been struggling with similar problems.
The problem, in our case, and I assume your case as well, comes from the GEDCOM format that is extremely opinionated about what a family should be. However this format contains some severe misconceptions about what a family tree really looks like.
GEDCOM has many issues, such as incompatibility with same sex relations, incest, etc... Which in real life happens more often than you'd imagine (especially when going back in time to the 1700-1800).
We have modeled our family tree to what happens in the real world: Events (for example, births, weddings, engagement, unions, deaths, adoptions, etc.). We do not put any restrictions on these, except for logically impossible ones (for example, one can't be one's own parent, relations need two individuals, etc...)
The lack of validations gives us a more "real world", simpler and more flexible solution.
As for this specific case, I would suggest removing the assertions as they do not hold universally.
For displaying issues (that will arise) I would suggest drawing the same node as many times as needed, hinting at the duplication by lighting up all the copies on selecting one of them.

## [C++11 introduced a standardized memory model. What does it mean? And how is it going to affect C++ programming?](https://stackoverflow.com/questions/6319146/c11-introduced-a-standardized-memory-model-what-does-it-mean-and-how-is-it-g)

**1508 Votes**, Nawaz

First, you have to learn to think like a Language Lawyer.
The C++ specification does not make reference to any particular compiler, operating system, or CPU.  It makes reference to an abstract machine that is a generalization of actual systems.  In the Language Lawyer world, the job of the programmer is to write code for the abstract machine; the job of the compiler is to actualize that code on a concrete machine.  By coding rigidly to the spec, you can be certain that your code will compile and run without modification on any system with a compliant C++ compiler, whether today or 50 years from now.
The abstract machine in the C++98/C++03 specification is fundamentally single-threaded.  So it is not possible to write multi-threaded C++ code that is "fully portable" with respect to the spec.  The spec does not even say anything about the atomicity of memory loads and stores or the order in which loads and stores might happen, never mind things like mutexes.
Of course, you can write multi-threaded code in practice for particular concrete systems -- like pthreads or Windows.  But there is no standard way to write multi-threaded code for C++98/C++03.
The abstract machine in C++11 is multi-threaded by design.  It also has a well-defined memory model; that is, it says what the compiler may and may not do when it comes to accessing memory.
Consider the following example, where a pair of global variables are accessed concurrently by two threads:

```python
           Global
           int x, y;

Thread 1            Thread 2
x = 17;             cout << y << " ";
y = 37;             cout << x << endl;
```

What might Thread 2 output?
Under C++98/C++03, this is not even Undefined Behavior; the question itself is meaningless because the standard does not contemplate anything called a "thread".
Under C++11, the result is Undefined Behavior, because loads and stores need not be atomic in general.  Which may not seem like much of an improvement...  And by itself, it's not.
But with C++11, you can write this:

```python
           Global
           atomic<int> x, y;

Thread 1                 Thread 2
x.store(17);             cout << y.load() << " ";
y.store(37);             cout << x.load() << endl;
```

Now things get much more interesting.  First of all, the behavior here is defined.  Thread 2 could now print `0 0` (if it runs before Thread 1), `37 17` (if it runs after Thread 1), or `0 17` (if it runs after Thread 1 assigns to x but before it assigns to y).
What it cannot print is `37 0`, because the default mode for atomic loads/stores in C++11 is to enforce sequential consistency.  This just means all loads and stores must be "as if" they happened in the order you wrote them within each thread, while operations among threads can be interleaved however the system likes.  So the default behavior of atomics provides both atomicity and ordering for loads and stores.
Now, on a modern CPU, ensuring sequential consistency can be expensive.  In particular, the compiler is likely to emit full-blown memory barriers between every access here.  But if your algorithm can tolerate out-of-order loads and stores; i.e., if it requires atomicity but not ordering; i.e., if it can tolerate `37 0` as output from this program, then you can write this:

```python
           Global
           atomic<int> x, y;

Thread 1                            Thread 2
x.store(17,memory_order_relaxed);   cout << y.load(memory_order_relaxed) << " ";
y.store(37,memory_order_relaxed);   cout << x.load(memory_order_relaxed) << endl;
```

The more modern the CPU, the more likely this is to be faster than the previous example.
Finally, if you just need to keep particular loads and stores in order, you can write:

```python
           Global
           atomic<int> x, y;

Thread 1                            Thread 2
x.store(17,memory_order_release);   cout << y.load(memory_order_acquire) << " ";
y.store(37,memory_order_release);   cout << x.load(memory_order_acquire) << endl;
```

This takes us back to the ordered loads and stores -- so `37 0` is no longer a possible output -- but it does so with minimal overhead.  (In this trivial example, the result is the same as full-blown sequential consistency; in a larger program, it would not be.)
Of course, if the only outputs you want to see are `0 0` or `37 17`, you can just wrap a mutex around the original code.  But if you have read this far, I bet you already know how that works, and this answer is already longer than I intended :-).
So, bottom line. Mutexes are great, and C++11 standardizes them. But sometimes for performance reasons you want lower-level primitives (e.g., the classic double-checked locking pattern).  The new standard provides high-level gadgets like mutexes and condition variables, and it also provides low-level gadgets like atomic types and the various flavors of memory barrier.  So now you can write sophisticated, high-performance concurrent routines entirely within the language specified by the standard, and you can be certain your code will compile and run unchanged on both today's systems and tomorrow's.
Although to be frank, unless you are an expert and working on some serious low-level code, you should probably stick to mutexes and condition variables.  That's what I intend to do.
For more on this stuff, see this blog post.

## [How can I profile C++ code running in Linux?](https://stackoverflow.com/questions/375913/how-can-i-profile-c-code-running-in-linux)

**1464 Votes**, Gabriel Isenberg

If your goal is to use a profiler, use one of the suggested ones.
However, if you're in a hurry and you can manually interrupt your program under the debugger while it's being subjectively slow, there's a simple way to find performance problems.
Just halt it several times, and each time look at the call stack. If there is some code that is wasting some percentage of the time, 20% or 50% or whatever, that is the probability that you will catch it in the act on each sample. So that is roughly the percentage of samples on which you will see it. There is no educated guesswork required.
If you do have a guess as to what the problem is, this will prove or disprove it.
You may have multiple performance problems of different sizes. If you clean out any one of them, the remaining ones will take a larger percentage, and be easier to spot, on subsequent passes.
This magnification effect, when compounded over multiple problems, can lead to truly massive speedup factors.
Caveat: Programmers tend to be skeptical of this technique unless they've used it themselves. They will say that profilers give you this information, but that is only true if they sample the entire call stack, and then let you examine a random set of samples. (The summaries are where the insight is lost.) Call graphs don't give you the same information, because 

they don't summarize at the instruction level, and
they give confusing summaries in the presence of recursion.

They will also say it only works on toy programs, when actually it works on any program, and it seems to work better on bigger programs, because they tend to have more problems to find.
They will say it sometimes finds things that aren't problems, but that is only true if you see something once. If you see a problem on more than one sample, it is real.
P.S. This can also be done on multi-thread programs if there is a way to collect call-stack samples of the thread pool at a point in time, as there is in Java.
P.P.S As a rough generality, the more layers of abstraction you have in your software, the more likely you are to find that that is the cause of performance problems (and the opportunity to get speedup).
Added: It might not be obvious, but the stack sampling technique works equally well in the presence of recursion. The reason is that the time that would be saved by removal of an instruction is approximated by the fraction of samples containing it, regardless of the number of times it may occur within a sample.
Another objection I often hear is: "It will stop someplace random, and it will miss the real problem".
This comes from having a prior concept of what the real problem is.
A key property of performance problems is that they defy expectations.
Sampling tells you something is a problem, and your first reaction is disbelief.
That is natural, but you can be sure if it finds a problem it is real, and vice-versa.
ADDED: Let me make a Bayesian explanation of how it works.  Suppose there is some instruction ``I (call or otherwise) which is on the call stack some fraction ``f of the time (and thus costs that much). For simplicity, suppose we don't know what ``f is, but assume it is either 0.1, 0.2, 0.3, ... 0.9, 1.0, and the prior probability of each of these possibilities is 0.1, so all of these costs are equally likely a-priori.
Then suppose we take just 2 stack samples, and we see instruction ``I on both samples, designated observation `o=2/2`. This gives us new estimates of the frequency ``f of ``I, according to this:

```python
Prior                                    
P(f=x) x  P(o=2/2|f=x) P(o=2/2&&f=x)  P(o=2/2&&f >= x)  P(f >= x)

0.1    1     1             0.1          0.1            0.25974026
0.1    0.9   0.81          0.081        0.181          0.47012987
0.1    0.8   0.64          0.064        0.245          0.636363636
0.1    0.7   0.49          0.049        0.294          0.763636364
0.1    0.6   0.36          0.036        0.33           0.857142857
0.1    0.5   0.25          0.025        0.355          0.922077922
0.1    0.4   0.16          0.016        0.371          0.963636364
0.1    0.3   0.09          0.009        0.38           0.987012987
0.1    0.2   0.04          0.004        0.384          0.997402597
0.1    0.1   0.01          0.001        0.385          1

                  P(o=2/2) 0.385                
```

The last column says that, for example, the probability that ``f >= 0.5 is 92%, up from the prior assumption of 60%.
Suppose the prior assumptions are different. Suppose we assume P(f=0.1) is .991 (nearly certain), and all the other possibilities are almost impossible (0.001). In other words, our prior certainty is that ``I is cheap. Then we get:

```python
Prior                                    
P(f=x) x  P(o=2/2|f=x) P(o=2/2&& f=x)  P(o=2/2&&f >= x)  P(f >= x)

0.001  1    1              0.001        0.001          0.072727273
0.001  0.9  0.81           0.00081      0.00181        0.131636364
0.001  0.8  0.64           0.00064      0.00245        0.178181818
0.001  0.7  0.49           0.00049      0.00294        0.213818182
0.001  0.6  0.36           0.00036      0.0033         0.24
0.001  0.5  0.25           0.00025      0.00355        0.258181818
0.001  0.4  0.16           0.00016      0.00371        0.269818182
0.001  0.3  0.09           0.00009      0.0038         0.276363636
0.001  0.2  0.04           0.00004      0.00384        0.279272727
0.991  0.1  0.01           0.00991      0.01375        1

                  P(o=2/2) 0.01375                
```

Now it says P(f >= 0.5) is 26%, up from the prior assumption of 0.6%. So Bayes allows us to update our estimate of the probable cost of ``I. If the amount of data is small, it doesn't tell us accurately what the cost is, only that it is big enough to be worth fixing.
Yet another way to look at it is called the Rule Of Succession.
If you flip a coin 2 times, and it comes up heads both times, what does that tell you about the probable weighting of the coin?
The respected way to answer is to say that it's a Beta distribution, with average value (number of hits + 1) / (number of tries + 2) = (2+1)/(2+2) = 75%.
(The key is that we see ``I more than once. If we only see it once, that doesn't tell us much except that ``f > 0.)
So, even a very small number of samples can tell us a lot about the cost of instructions that it sees. (And it will see them with a frequency, on average, proportional to their cost. If ``n samples are taken, and ``f is the cost, then ``I will appear on `nf+/-sqrt(nf(1-f))` samples. Example, `n=10`, `f=0.3`, that is `3+/-1.4` samples.)

ADDED, to give an intuitive feel for the difference between measuring and random stack sampling:
There are profilers now that sample the stack, even on wall-clock time, but what comes out is measurements (or hot path, or hot spot, from which a "bottleneck" can easily hide). What they don't show you (and they easily could) is the actual samples themselves. And if your goal is to find the bottleneck, the number of them you need to see is, on average, 2 divided by the fraction of time it takes.
So if it takes 30% of time, 2/.3 = 6.7 samples, on average, will show it, and the chance that 20 samples will show it is 99.2%.
Here is an off-the-cuff illustration of the difference between examining measurements and examining stack samples.
The bottleneck could be one big blob like this, or numerous small ones, it makes no difference.

Measurement is horizontal; it tells you what fraction of time specific routines take.
Sampling is vertical.
If there is any way to avoid what the whole program is doing at that moment, and if you see it on a second sample, you've found the bottleneck.
That's what makes the difference - seeing the whole reason for the time being spent, not just how much.

## [Regular cast vs. static_cast vs. dynamic_cast [duplicate]](https://stackoverflow.com/questions/28002/regular-cast-vs-static-cast-vs-dynamic-cast)

**1443 Votes**, Graeme Perrow

### static_cast

`static_cast` is used for cases where you basically want to reverse an implicit conversion, with a few restrictions and additions. `static_cast` performs no runtime checks. This should be used if you know that you refer to an object of a specific type, and thus a check would be unnecessary. Example:

```python
void func(void *data) {
  // Conversion from MyClass* -> void* is implicit
  MyClass *c = static_cast<MyClass*>(data);
  ...
}

int main() {
  MyClass c;
  start_thread(&func, &c)  // func(&c) will be called
      .join();
}
```

In this example, you know that you passed a `MyClass` object, and thus there isn't any need for a runtime check to ensure this.

### dynamic_cast

`dynamic_cast` is useful when you don't know what the dynamic type of the object is. It returns a null pointer if the object referred to doesn't contain the type casted to as a base class (when you cast to a reference, a `bad_cast` exception is thrown in that case).

```python
if (JumpStm *j = dynamic_cast<JumpStm*>(&stm)) {
  ...
} else if (ExprStm *e = dynamic_cast<ExprStm*>(&stm)) {
  ...
}
```

You cannot use `dynamic_cast` if you downcast (cast to a derived class) and the argument type is not polymorphic. For example, the following code is not valid, because `Base` doesn't contain any virtual function:

```python
struct Base { };
struct Derived : Base { };
int main() {
  Derived d; Base *b = &d;
  dynamic_cast<Derived*>(b); // Invalid
}
```

An "up-cast" (cast to the base class) is always valid with both `static_cast` and `dynamic_cast`, and also without any cast, as an "up-cast" is an implicit conversion.

### Regular Cast

These casts are also called C-style cast. A C-style cast is basically identical to trying out a range of sequences of C++ casts, and taking the first C++ cast that works, without ever considering `dynamic_cast`. Needless to say, this is much more powerful as it combines all of `const_cast`, `static_cast` and `reinterpret_cast`, but it's also unsafe, because it does not use `dynamic_cast`.
In addition, C-style casts not only allow you to do this, but they also allow you to safely cast to a private base-class, while the "equivalent" `static_cast` sequence would give you a compile-time error for that.
Some people prefer C-style casts because of their brevity. I use them for numeric casts only, and use the appropriate C++ casts when user defined types are involved, as they provide stricter checking.

## [What is a smart pointer and when should I use one?](https://stackoverflow.com/questions/106508/what-is-a-smart-pointer-and-when-should-i-use-one)

**1387 Votes**, Alex Reynolds

A smart pointer is a class that wraps a 'raw' (or 'bare') C++ pointer, to manage the lifetime of the object being pointed to. There is no single smart pointer type, but all of them try to abstract a raw pointer in a practical way.
Smart pointers should be preferred over raw pointers. If you feel you need to use pointers (first consider if you really do), you would normally want to use a smart pointer as this can alleviate many of the problems with raw pointers, mainly forgetting to delete the object and leaking memory.
With raw pointers, the programmer has to explicitly destroy the object when it is no longer useful.

```python
// Need to create the object to achieve some goal
MyObject* ptr = new MyObject(); 
ptr->DoSomething(); // Use the object in some way
delete ptr; // Destroy the object. Done with it.
// Wait, what if DoSomething() raises an exception...?
```

A smart pointer by comparison defines a policy as to when the object is destroyed. You still have to create the object, but you no longer have to worry about destroying it.

```python
SomeSmartPtr<MyObject> ptr(new MyObject());
ptr->DoSomething(); // Use the object in some way.

// Destruction of the object happens, depending 
// on the policy the smart pointer class uses.

// Destruction would happen even if DoSomething() 
// raises an exception
```

The simplest policy in use involves the scope of the smart pointer wrapper object, such as implemented by `boost::scoped_ptr` or `std::unique_ptr`. 

```python
void f()
{
    {
       boost::scoped_ptr<MyObject> ptr(new MyObject());
       ptr->DoSomethingUseful();
    } // boost::scopted_ptr goes out of scope -- 
      // the MyObject is automatically destroyed.

    // ptr->Oops(); // Compile error: "ptr" not defined
                    // since it is no longer in scope.
}
```

Note that `scoped_ptr` instances cannot be copied. This prevents the pointer from being deleted multiple times (incorrectly). You can, however, pass references to it around to other functions you call.
Scoped pointers are useful when you want to tie the lifetime of the object to a particular block of code, or if you embedded it as member data inside another object, the lifetime of that other object. The object exists until the containing block of code is exited, or until the containing object is itself destroyed.
A more complex smart pointer policy involves reference counting the pointer. This does allow the pointer to be copied. When the last "reference" to the object is destroyed, the object is deleted. This policy is implemented by `boost::shared_ptr` and `std::shared_ptr`.

```python
void f()
{
    typedef std::shared_ptr<MyObject> MyObjectPtr; // nice short alias
    MyObjectPtr p1; // Empty

    {
        MyObjectPtr p2(new MyObject());
        // There is now one "reference" to the created object
        p1 = p2; // Copy the pointer.
        // There are now two references to the object.
    } // p2 is destroyed, leaving one reference to the object.
} // p1 is destroyed, leaving a reference count of zero. 
  // The object is deleted.
```

Reference counted pointers are very useful when the lifetime of your object is much more complicated, and is not tied directly to a particular section of code or to another object.
There is one drawback to reference counted pointers  the possibility of creating a dangling reference:

```python
// Create the smart pointer on the heap
MyObjectPtr* pp = new MyObjectPtr(new MyObject())
// Hmm, we forgot to destroy the smart pointer,
// because of that, the object is never destroyed!
```

Another possibility is creating circular references:

```python
struct Owner {
   boost::shared_ptr<Owner> other;
};

boost::shared_ptr<Owner> p1 (new Owner());
boost::shared_ptr<Owner> p2 (new Owner());
p1->other = p2; // p1 references p2
p2->other = p1; // p2 references p1

// Oops, the reference count of of p1 and p2 never goes to zero!
// The objects are never destroyed!
```

To work around this problem, both Boost and C++11 have defined a `weak_ptr` to define a weak (uncounted) reference to a `shared_ptr`.

UPDATE
This answer is rather old, and so describes what was 'good' at the time, which was smart pointers provided by the Boost library. Since C++11, the standard library has provided sufficient smart pointers types, and so you should favour the use of `std::unique_ptr`, `std::shared_ptr` and `std::weak_ptr`. 
There is also `std::auto_ptr`. It is very much like a scoped pointer, except that it also has the "special" dangerous ability to be copied  which also unexpectedly transfers ownership! It is deprecated in the newest standards, so you shouldn't use it. Use the `std::unique_ptr` instead.

```python
std::auto_ptr<MyObject> p1 (new MyObject());
std::auto_ptr<MyObject> p2 = p1; // Copy and transfer ownership. 
                                 // p1 gets set to empty!
p2->DoSomething(); // Works.
p1->DoSomething(); // Oh oh. Hopefully raises some NULL pointer exception.
```

## [Why is reading lines from stdin much slower in C++ than Python?](https://stackoverflow.com/questions/9371238/why-is-reading-lines-from-stdin-much-slower-in-c-than-python)

**1376 Votes**, community-wiki

By default, `cin` is synchronized with stdio, which causes it to avoid any input buffering.  If you add this to the top of your main, you should see much better performance:

```python
std::ios_base::sync_with_stdio(false);
```

Normally, when an input stream is buffered, instead of reading one character at a time, the stream will be read in larger chunks.  This reduces the number of system calls, which are typically relatively expensive.  However, since the `FILE*` based `stdio` and `iostreams` often have separate implementations and therefore separate buffers, this could lead to a problem if both were used together.  For example:

```python
int myvalue1;
cin >> myvalue1;
int myvalue2;
scanf("%d",&myvalue2);
```

If more input was read by `cin` than it actually needed, then the second integer value wouldn't be available for the `scanf` function, which has its own independent buffer.  This would lead to unexpected results.
To avoid this, by default, streams are synchronized with `stdio`.  One common way to achieve this is to have `cin` read each character one at a time as needed using `stdio` functions.  Unfortunately, this introduces a lot of overhead.  For small amounts of input, this isn't a big problem, but when you are reading millions of lines, the performance penalty is significant.
Fortunately, the library designers decided that you should also be able to disable this feature to get improved performance if you knew what you were doing, so they provided the `sync_with_stdio` method.

## [Image Processing: Algorithm Improvement for 'Coca-Cola Can' Recognition](https://stackoverflow.com/questions/10168686/image-processing-algorithm-improvement-for-coca-cola-can-recognition)

**1361 Votes**, Charles Menguy

An alternative approach would be to extract features (keypoints) using the scale-invariant feature transform (SIFT) or Speeded Up Robust Features (SURF).
It is implemented in OpenCV 2.3.1.
You can find a nice code example using features in Features2D + Homography to find a known object
Both algorithms are invariant to scaling and rotation. Since they work with features, you can also handle occlusion (as long as enough keypoints are visible).

Image source: tutorial example
The processing takes a few hundred ms for SIFT, SURF is bit faster, but it not suitable for real-time applications. ORB uses FAST which is weaker regarding rotation invariance.
The original papers

SURF: Speeded Up Robust Features
Distinctive Image Features
from Scale-Invariant Keypoints
ORB: an efficient alternative to SIFT or SURF

## [Is < faster than <=?](https://stackoverflow.com/questions/12135518/is-faster-than)

**1357 Votes**, Vincius Magalhes Horta

No, it will not be faster on most architectures. You didn't specify, but on x86, all of the integral comparisons will be typically implemented in two machine instructions:

A `test` or `cmp` instruction, which sets `EFLAGS`
And a `Jcc` (jump) instruction, depending on the comparison type (and code layout):

`jne` - Jump if not equal --> `ZF = 0`
`jz` - Jump if zero (equal) --> `ZF = 1`
`jg` - Jump if greater --> `ZF = 0 and SF = OF`
(etc...)



Example (Edited for brevity) Compiled with `$ gcc -m32 -S -masm=intel test.c`

```python
    if (a < b) {
        // Do something 1
    }
```

Compiles to:

```python
    mov     eax, DWORD PTR [esp+24]      ; a
    cmp     eax, DWORD PTR [esp+28]      ; b
    jge     .L2                          ; jump if a is >= b
    ; Do something 1
.L2:
```

And

```python
    if (a <= b) {
        // Do something 2
    }
```

Compiles to:

```python
    mov     eax, DWORD PTR [esp+24]      ; a
    cmp     eax, DWORD PTR [esp+28]      ; b
    jg      .L5                          ; jump if a is > b
    ; Do something 2
.L5:
```

So the only difference between the two is a `jg` versus a `jge` instruction. The two will take the same amount of time.

I'd like to address the comment that nothing indicates that the different jump instructions take the same amount of time.  This one is a little tricky to answer, but here's what I can give: In the Intel Instruction Set Reference, they are all grouped together under one common instruction, `Jcc` (Jump if condition is met). The same grouping is made together under the Optimization Reference Manual, in Appendix C. Latency and Throughput.

Latency  The number of clock cycles that are required for the
  execution core to  complete the execution of all of the ops that form
  an instruction.
Throughput  The number of clock cycles required to
  wait before the issue  ports are free to accept the same instruction
  again. For many instructions, the  throughput of an instruction can be
  significantly less than its latency

The values for `Jcc` are:

```python
      Latency   Throughput
Jcc     N/A        0.5
```

with the following footnote on `Jcc`:

7) Selection of conditional jump instructions should be based on the recommendation of section Section 3.4.1, Branch Prediction Optimization, to improve the  predictability of branches. When branches are predicted successfully, the latency of `jcc` is effectively zero.

So, nothing in the Intel docs ever treats one `Jcc` instruction any differently from the others.
If one thinks about the actual circuitry used to implement the instructions, one can assume that there would be simple AND/OR gates on the different bits in `EFLAGS`, to determine whether the conditions are met. There is then, no reason that an instruction testing two bits should take any more or less time than one testing only one (Ignoring gate propagation delay, which is much less than the clock period.)

Edit: Floating Point
This holds true for x87 floating point as well:  (Pretty much same code as above, but with `double` instead of `int`.)

```python
        fld     QWORD PTR [esp+32]
        fld     QWORD PTR [esp+40]
        fucomip st, st(1)              ; Compare ST(0) and ST(1), and set CF, PF, ZF in EFLAGS
        fstp    st(0)
        seta    al                     ; Set al if above (CF=0 and ZF=0).
        test    al, al
        je      .L2
        ; Do something 1
.L2:

        fld     QWORD PTR [esp+32]
        fld     QWORD PTR [esp+40]
        fucomip st, st(1)              ; (same thing as above)
        fstp    st(0)
        setae   al                     ; Set al if above or equal (CF=0).
        test    al, al
        je      .L5
        ; Do something 2
.L5:
        leave
        ret
```

## [Why does changing 0.1f to 0 slow down performance by 10x?](https://stackoverflow.com/questions/9314534/why-does-changing-0-1f-to-0-slow-down-performance-by-10x)

**1346 Votes**, Dragarro

Welcome to the world of denormalized floating-point! They can wreak havoc on performance!!!
Denormal (or subnormal) numbers are kind of a hack to get some extra values very close to zero out of the floating point representation. Operations on denormalized floating-point can be tens to hundreds of times slower than on normalized floating-point. This is because many processors can't handle them directly and must trap and resolve them using microcode.
If you print out the numbers after 10,000 iterations, you will see that they have converged to different values depending on whether ``0 or `0.1` is used.
Here's the test code compiled on x64:

```python
int main() {

    double start = omp_get_wtime();

    const float x[16]={1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6};
    const float z[16]={1.123,1.234,1.345,156.467,1.578,1.689,1.790,1.812,1.923,2.034,2.145,2.256,2.367,2.478,2.589,2.690};
    float y[16];
    for(int i=0;i<16;i++)
    {
        y[i]=x[i];
    }
    for(int j=0;j<9000000;j++)
    {
        for(int i=0;i<16;i++)
        {
            y[i]*=x[i];
            y[i]/=z[i];
#ifdef FLOATING
            y[i]=y[i]+0.1f;
            y[i]=y[i]-0.1f;
#else
            y[i]=y[i]+0;
            y[i]=y[i]-0;
#endif

            if (j > 10000)
                cout << y[i] << "  ";
        }
        if (j > 10000)
            cout << endl;
    }

    double end = omp_get_wtime();
    cout << end - start << endl;

    system("pause");
    return 0;
}
```

Output:

```python
#define FLOATING
1.78814e-007  1.3411e-007  1.04308e-007  0  7.45058e-008  6.70552e-008  6.70552e-008  5.58794e-007  3.05474e-007  2.16067e-007  1.71363e-007  1.49012e-007  1.2666e-007  1.11759e-007  1.04308e-007  1.04308e-007
1.78814e-007  1.3411e-007  1.04308e-007  0  7.45058e-008  6.70552e-008  6.70552e-008  5.58794e-007  3.05474e-007  2.16067e-007  1.71363e-007  1.49012e-007  1.2666e-007  1.11759e-007  1.04308e-007  1.04308e-007

//#define FLOATING
6.30584e-044  3.92364e-044  3.08286e-044  0  1.82169e-044  1.54143e-044  2.10195e-044  2.46842e-029  7.56701e-044  4.06377e-044  3.92364e-044  3.22299e-044  3.08286e-044  2.66247e-044  2.66247e-044  2.24208e-044
6.30584e-044  3.92364e-044  3.08286e-044  0  1.82169e-044  1.54143e-044  2.10195e-044  2.45208e-029  7.56701e-044  4.06377e-044  3.92364e-044  3.22299e-044  3.08286e-044  2.66247e-044  2.66247e-044  2.24208e-044
```

Note how in the second run the numbers are very close to zero.
Denormalized numbers are generally rare and thus most processors don't try to handle them efficiently.

To demonstrate that this has everything to do with denormalized numbers, if we flush denormals to zero by adding this to the start of the code:

```python
_MM_SET_FLUSH_ZERO_MODE(_MM_FLUSH_ZERO_ON);
```

Then the version with ``0 is no longer 10x slower and actually becomes faster. (This requires that the code be compiled with SSE enabled.)
This means that rather than using these weird lower precision almost-zero values, we just round to zero instead.
Timings: Core i7 920 @ 3.5 GHz:

```python
//  Don't flush denormals to zero.
0.1f: 0.564067
0   : 26.7669

//  Flush denormals to zero.
0.1f: 0.587117
0   : 0.341406
```

In the end, this really has nothing to do with whether it's an integer or floating-point. The ``0 or `0.1f` is converted/stored into a register outside of both loops. So that has no effect on performance.

## [Why can templates only be implemented in the header file?](https://stackoverflow.com/questions/495021/why-can-templates-only-be-implemented-in-the-header-file)

**1335 Votes**, MainID

It is not necessary to put the implementation in the header file, see the alternative solution at the end of this answer.
Anyway, the reason your code is failing is that, when instantiating a template, the compiler creates a new class with the given template argument. For example:

```python
template<typename T>
struct Foo
{
    T bar;
    void doSomething(T param) {/* do stuff using T */}
};

// somewhere in a .cpp
Foo<int> f; 
```

When reading this line, the compiler will create a new class (let's call it `FooInt`), which is equivalent to the following:

```python
struct FooInt
{
    int bar;
    void doSomething(int param) {/* do stuff using int */}
}
```

Consequently, the compiler needs to have access to the implementation of the methods, to instantiate them with the template argument (in this case `int`). If these implementations were not in the header, they wouldn't be accessible, and therefore the compiler wouldn't be able to instantiate the template.
A common solution to this is to write the template declaration in a header file, then implement the class in an implementation file (for example .tpp), and include this implementation file at the end of the header.

```python
// Foo.h
template <typename T>
struct Foo
{
    void doSomething(T param);
};

#include "Foo.tpp"

// Foo.tpp
template <typename T>
void Foo<T>::doSomething(T param)
{
    //implementation
}
```

This way, implementation is still separated from declaration, but is accessible to the compiler.
Another solution is to keep the implementation separated, and explicitly instantiate all the template instances you'll need:

```python
// Foo.h

// no implementation
template <typename T> struct Foo { ... };

//----------------------------------------    
// Foo.cpp

// implementation of Foo's methods

// explicit instantiations
template class Foo<int>;
template class Foo<float>;
// You will only be able to use Foo with int or float
```

If my explanation isn't clear enough, you can have a look at the C++ Super-FAQ on this subject.

## [What are move semantics?](https://stackoverflow.com/questions/3106110/what-are-move-semantics)

**1326 Votes**, dicroce

I find it easiest to understand move semantics with example code. Let's start with a very simple string class which only holds a pointer to a heap-allocated block of memory:

```python
#include <cstring>
#include <algorithm>

class string
{
    char* data;

public:

    string(const char* p)
    {
        size_t size = strlen(p) + 1;
        data = new char[size];
        memcpy(data, p, size);
    }
```

Since we chose to manage the memory ourselves, we need to follow the rule of three. I am going to defer writing the assignment operator and only implement the destructor and the copy constructor for now:

```python
    ~string()
    {
        delete[] data;
    }

    string(const string& that)
    {
        size_t size = strlen(that.data) + 1;
        data = new char[size];
        memcpy(data, that.data, size);
    }
```

The copy constructor defines what it means to copy string objects. The parameter `const string& that` binds to all expressions of type string which allows you to make copies in the following examples:

```python
string a(x);                                    // Line 1
string b(x + y);                                // Line 2
string c(some_function_returning_a_string());   // Line 3
```

Now comes the key insight into move semantics. Note that only in the first line where we copy ``x is this deep copy really necessary, because we might want to inspect ``x later and would be very surprised if ``x had changed somehow. Did you notice how I just said ``x three times (four times if you include this sentence) and meant the exact same object every time? We call expressions such as ``x "lvalues".
The arguments in lines 2 and 3 are not lvalues, but rvalues, because the underlying string objects have no names, so the client has no way to inspect them again at a later point in time.
rvalues denote temporary objects which are destroyed at the next semicolon (to be more precise: at the end of the full-expression that lexically contains the rvalue). This is important because during the initialization of ``b and ``c, we could do whatever we wanted with the source string, and the client couldn't tell a difference!
C++0x introduces a new mechanism called "rvalue reference" which, among other things,
allows us to detect rvalue arguments via function overloading. All we have to do is write a constructor with an rvalue reference parameter. Inside that constructor we can do anything we want with the source, as long as we leave it in some valid state:

```python
    string(string&& that)   // string&& is an rvalue reference to a string
    {
        data = that.data;
        that.data = nullptr;
    }
```

What have we done here? Instead of deeply copying the heap data, we have just copied the pointer and then set the original pointer to null. In effect, we have "stolen" the data that originally belonged to the source string. Again, the key insight is that under no circumstance could the client detect that the source had been modified. Since we don't really do a copy here, we call this constructor a "move constructor". Its job is to move resources from one object to another instead of copying them.
Congratulations, you now understand the basics of move semantics! Let's continue by implementing the assignment operator. If you're unfamiliar with the copy and swap idiom, learn it and come back, because it's an awesome C++ idiom related to exception safety.

```python
    string& operator=(string that)
    {
        std::swap(data, that.data);
        return *this;
    }
};
```

Huh, that's it? "Where's the rvalue reference?" you might ask. "We don't need it here!" is my answer :)
Note that we pass the parameter `that` by value, so `that` has to be initialized just like any other string object. Exactly how is `that` going to be initialized? In the olden days of C++98, the answer would have been "by the copy constructor". In C++0x, the compiler chooses between the copy constructor and the move constructor based on whether the argument to the assignment operator is an lvalue or an rvalue.
So if you say `a = b`, the copy constructor will initialize `that` (because the expression ``b is an lvalue), and the assignment operator swaps the contents with a freshly created, deep copy. That is the very definition of the copy and swap idiom -- make a copy, swap the contents with the copy, and then get rid of the copy by leaving the scope. Nothing new here.
But if you say `a = x + y`, the move constructor will initialize `that` (because the expression `x + y` is an rvalue), so there is no deep copy involved, only an efficient move.
`that` is still an independent object from the argument, but its construction was trivial,
since the heap data didn't have to be copied, just moved. It wasn't necessary to copy it because `x + y` is an rvalue, and again, it is okay to move from string objects denoted by rvalues.
To summarize, the copy constructor makes a deep copy, because the source must remain untouched.
The move constructor, on the other hand, can just copy the pointer and then set the pointer in the source to null. It is okay to "nullify" the source object in this manner, because the client has no way of inspecting the object again.
I hope this example got the main point across. There is a lot more to rvalue references and move semantics which I intentionally left out to keep it simple. If you want more details please see my supplementary answer.

## [Why should I use a pointer rather than the object itself?](https://stackoverflow.com/questions/22146094/why-should-i-use-a-pointer-rather-than-the-object-itself)

**1312 Votes**, gEdringer

It's very unfortunate that you see dynamic allocation so often. That just shows how many bad C++ programmers there are.
In a sense, you have two questions bundled up into one. The first is when should we use dynamic allocation (using `new`)? The second is when should we use pointers?
The important take-home message is that you should always use the appropriate tool for the job. In almost all situations, there is something more appropriate and safer than performing manual dynamic allocation and/or using raw pointers.

### Dynamic allocation

In your question, you've demonstrated two ways of creating an object. The main difference is the storage duration of the object. When doing `Object myObject;` within a block, the object is created with automatic storage duration, which means it will be destroyed automatically when it goes out of scope. When you do `new Object()`, the object has dynamic storage duration, which means it stays alive until you explicitly `delete` it. You should only use dynamic storage duration when you need it. 
That is, you should always prefer creating objects with automatic storage duration when you can.
The main two situations in which you might require dynamic allocation:

You need the object to outlive the current scope - that specific object at that specific memory location, not a copy of it. If you're okay with copying/moving the object (most of the time you should be), you should prefer an automatic object.
You need to allocate a lot of memory, which may easily fill up the stack. It would be nice if we didn't have to concern ourselves with this (most of the time you shouldn't have to), as it's really outside the purview of C++, but unfortunately we have to deal with the reality of the systems we're developing for.

When you do absolutely require dynamic allocation, you should encapsulate it in a smart pointer or some other type that performs RAII (like the standard containers). Smart pointers provide ownership semantics of dynamically allocated objects. Take a look at `std::unique_ptr` and `std::shared_ptr`, for example. If you use them appropriately, you can almost entirely avoid performing your own memory management (see the Rule of Zero).

### Pointers

However, there are other more general uses for raw pointers beyond dynamic allocation, but most have alternatives that you should prefer. As before, always prefer the alternatives unless you really need pointers.

You need reference semantics. Sometimes you want to pass an object using a pointer (regardless of how it was allocated) because you want the function to which you're passing it to have access that that specific object (not a copy of it). However, in most situations, you should prefer reference types to pointers, because this is specifically what they're designed for. Note this is not necessarily about extending the lifetime of the object beyond the current scope, as in situation 1 above. As before, if you're okay with passing a copy of the object, you don't need reference semantics.
You need polymorphism. You can only call functions polymorphically (that is, according to the dynamic type of an object) through a pointer or reference to the object. If that's the behaviour you need, then you need to use pointers or references. Again, references should be preferred.
You want to represent that an object is optional by allowing a `nullptr` to be passed when the object is being omitted. If it's an argument, you should prefer to use default arguments or function overloads. Otherwise, you should prefer use a type that encapsulates this behaviour, such as `std::optional` (introduced in C++17 - with earlier C++ standards, use `boost::optional`).
You want to decouple compilation units to improve compilation time. The useful property of a pointer is that you only require a forward declaration of the pointed-to type (to actually use the object, you'll need a definition). This allows you to decouple parts of your compilation process, which may significantly improve compilation time. See the Pimpl idiom.
You need to interface with a C library or a C-style library. At this point, you're forced to use raw pointers. The best thing you can do is make sure you only let your raw pointers loose at the last possible moment. You can get a raw pointer from a smart pointer, for example, by using its `get` member function. If a library performs some allocation for you which it expects you to deallocate via a handle, you can often wrap the handle up in a smart pointer with a custom deleter that will deallocate the object appropriately.

## [Compiling an application for use in highly radioactive environments](https://stackoverflow.com/questions/36827659/compiling-an-application-for-use-in-highly-radioactive-environments)

**1261 Votes**, rook

Working for about 4-5 years with software/firmware development and environment testing of miniaturized satellites*, I would like to share my experience here.
*(miniaturized satellites are a lot more prone to single event upsets than bigger satellites due to its relatively small, limited sizes for its electronic components)

To be very concise and direct: there is no mechanism to recover from detectable, erroneous
  situation by the software/firmware itself without, at least, one
  copy of minimum working version of the software/firmware somewhere for recovery purpose - and with the hardware supporting the recovery (functional).

Now, this situation is normally handled both in the hardware and software level. Here, as you request, I will share what we can do in the software level.

...recovery purpose.... Provide ability to update/recompile/reflash your software/firmware in real environment. This is an almost must-have feature for any software/firmware in highly ionized environment. Without this, you could have redundant software/hardware as many as you want but at one point, they are all going to blow up. So, prepare this feature!
...minimum working version... Have responsive, multiple copies, minimum version of the software/firmware in your code. This is like Safe mode in Windows. Instead of having only one, fully functional version of your software, have multiple copies of the minimum version of your software/firmware. The minimum copy will usually having much less size than the full copy and almost always have only the following two or three features: 

capable of listening to command from external system, 
capable of updating the current software/firmware, 
capable of monitoring the basic operation's housekeeping data.

...copy... somewhere... Have redundant software/firmware somewhere. 

You could, with or without redundant hardware, try to have redundant software/firmware in your ARM uC. This is normally done by having two or more identical software/firmware in separate addresses which sending heartbeat to each other - but only one will be active at a time. If one or more software/firmware is known to be unresponsive, switch to the other software/firmware. The benefit of using this approach is we can have functional replacement immediately after an error occurs - without any contact with whatever external system/party who is responsible to detect and to repair the error (in satellite case, it is usually the Mission Control Centre (MCC)). 
Strictly speaking, without redundant hardware, the disadvantage of doing this is you actually cannot eliminate all single point of failures. At the very least, you will still have one single point of failure, which is the switch itself (or often the beginning of the code). Nevertheless, for a device limited by size in a highly ionized environment (such as pico/femto satellites), the reduction of the single point of failures to one point without additional hardware will still be worth considering. Somemore, the piece of code for the switching would certainly be much less than the code for the whole program - significantly reducing the risk of getting Single Event in it.
But if you are not doing this, you should have at least one copy in your external system which can come in contact with the device and update the software/firmware (in the satellite case, it is again the mission control centre). 
You could also have the copy in your permanent memory storage in your device which can be triggered to restore the running system's software/firmware

...detectable erroneous situation.. The error must be detectable, usually by the hardware error correction/detection circuit or by a small piece of code for error correction/detection. It is best to put such code small, multiple, and independent from the main software/firmware. Its main task is only for checking/correcting. If the hardware circuit/firmware is reliable (such as it is more radiation hardened than the rests - or having multiple circuits/logics), then you might consider making error-correction with it. But if it is not, it is better to make it as error-detection. The correction can be by external system/device. For the error correction, you could consider making use of a basic error correction algorithm like Hamming/Golay23, because they can be implemented more easily both in the circuit/software. But it ultimately depends on your team's capability. For error detection, normally CRC is used.
...hardware supporting the recovery Now, comes to the most difficult aspect on this issue. Ultimately, the recovery requires the hardware which is responsible for the recovery to be at least functional. If the hardware is permanently broken (normally happen after its Total ionizing dose reaches certain level), then there is (sadly) no way for the software to help in recovery. Thus, hardware is rightly the utmost importance concern for a device exposed to high radiation level (such as satellite). 

In addition to the suggestion for above anticipating firmware's error due to single event upset, I would also like to suggest you to have:

Error detection and/or error correction algorithm in the inter-subsystem communication protocol. This is another almost must have in order to avoid incomplete/wrong signals received from other system
Filter in your ADC reading. Do not use the ADC reading directly. Filter it by median filter, mean filter, or any other filters - never trust single reading value. Sample more, not less - reasonably.

## [What is the effect of extern C in C++?](https://stackoverflow.com/questions/1041866/what-is-the-effect-of-extern-c-in-c)

**1180 Votes**, Litherum

extern "C" makes a function-name in C++ have 'C' linkage (compiler does not mangle the name) so that client C code can link to (i.e use) your function using a 'C' compatible header file that contains just the declaration of your function. Your function definition is contained in a binary format (that was compiled by your C++ compiler) that the client 'C' linker will then link to using the 'C' name.
Since C++ has overloading of function names and C does not, the C++ compiler cannot just use the function name as a unique id to link to, so it mangles the name by adding information about the arguments.  A C compiler does not need to mangle the name since you can not overload function names in C.  When you state that a function has extern "C" linkage in C++, the C++ compiler does not add argument/parameter type information to the name used for linkage.
Just so you know, you can specify "C" linkage to each individual declaration/definition explicitly or use a block to group a sequence of declarations/definitions to have a certain linkage:

```python
extern "C" void foo(int);
extern "C"
{
   void g(char);
   int i;
}
```

If you care about the technicalities, they are listed in section 7.5 of the C++03 standard, here is a brief summary (with emphasis on extern "C"):

extern "C" is a linkage-specification
Every compiler is required to provide "C" linkage
a linkage specification shall occur only in namespace scope
 all function types, function names and variable names have a language linkage  See Richard's Comment: Only function names and variable names with external linkage have a language linkage
two function types with distinct language linkages are distinct types even if otherwise identical
linkage specs nest, inner one determines the final linkage
extern "C" is ignored for class members 
at most one function with a particular name can have "C" linkage (regardless of namespace)
 extern "C" forces a function to have external linkage (cannot make it static)   See Richard's comment:    'static' inside 'extern "C"' is valid; an entity so declared has internal linkage, and so does not have a language linkage 
Linkage from C++ to objects defined in other languages and to objects defined in C++ from other languages is implementation-defined and language-dependent. Only where the object layout strategies of two language implementations are similar enough can such linkage be achieved

## [Easiest way to convert int to string in C++](https://stackoverflow.com/questions/5590381/easiest-way-to-convert-int-to-string-in-c)

**1168 Votes**, Nemo

C++11 introduces `std::stoi` (and variants for each numeric type) and `std::to_string`, the counterparts of the C `atoi` and `itoa` but expressed in term of `std::string`.

```python
#include <string> 

std::string s = std::to_string(42);
```

is therefore the shortest way I can think of. You can even omit naming the type, using the `auto` keyword:

```python
auto s = std::to_string(42);
```

Note: see [string.conversions] (21.5 in n3242)

## [When to use virtual destructors?](https://stackoverflow.com/questions/461203/when-to-use-virtual-destructors)

**1165 Votes**, Lodle

Virtual destructors are useful when you can delete an instance of a derived class through a pointer to base class:

```python
class Base 
{
    // some virtual methods
};

class Derived : public Base
{
    ~Derived()
    {
        // Do some important cleanup
    }
};
```

Here, you'll notice that I didn't declare Base's destructor to be `virtual`. Now, let's have a look at the following snippet:

```python
Base *b = new Derived();
// use b
delete b; // Here's the problem!
```

Since Base's destructor is not `virtual` and ``b is a `Base*` pointing to a `Derived` object, `delete b` has undefined behaviour:

[In `delete b`], if the static type of the
  object to be deleted is different from its dynamic type, the static
  type shall be a base class of the dynamic type of the object to be
  deleted and the static type shall have a virtual destructor or the
  behavior is undefined.

In most implementations, the call to the destructor will be resolved like any non-virtual code, meaning that the destructor of the base class will be called but not the one of the derived class, resulting in a resources leak.
To sum up, always make base classes' destructors `virtual` when they're meant to be manipulated polymorphically.
If you want to prevent the deletion of an instance through a base class pointer, you can make the base class destructor protected and nonvirtual; by doing so, the compiler won't let you call `delete` on a base class pointer.
You can learn more about virtuality and virtual base class destructor in this article from Herb Sutter.

## [What is an undefined reference/unresolved external symbol error and how do I fix it?](https://stackoverflow.com/questions/12573816/what-is-an-undefined-reference-unresolved-external-symbol-error-and-how-do-i-fix)

**1164 Votes**, Luchian Grigore

Compiling a C++ program takes place in several steps, as specified by 2.2 (credits to Keith Thompson for the reference):

The precedence among the syntax rules of translation is specified by the following phases [see footnote].

Physical source file characters are mapped, in an implementation-defined manner, to the basic source character set
  (introducing new-line characters for end-of-line indicators) if
  necessary. [SNIP]
Each instance of a backslash character (\) immediately followed by a new-line character is deleted, splicing physical source lines to
  form logical source lines. [SNIP]
The source file is decomposed into preprocessing tokens (2.5) and sequences of white-space characters (including comments). [SNIP]
Preprocessing directives are executed, macro invocations are expanded, and _Pragma unary operator expressions are executed. [SNIP]
Each source character set member in a character literal or a string literal, as well as each escape sequence and universal-character-name
  in a character literal or a non-raw string literal, is converted to
  the corresponding member of the execution character set; [SNIP]
Adjacent string literal tokens are concatenated.
White-space characters separating tokens are no longer significant. Each preprocessing token is converted into a token. (2.7). The
  resulting tokens are syntactically and semantically analyzed and
  translated as a translation unit. [SNIP]
Translated translation units and instantiation units are combined as follows: [SNIP]
All external entity references are resolved. Library components are linked to satisfy external references to entities not defined in the
  current translation. All such translator output is collected into a
  program image which contains information needed for execution in its
  execution environment. (emphasis mine)

[footnote] Implementations must behave as if these separate phases occur, although in practice different phases might be folded together.

The specified errors occur during this last stage of compilation, most commonly referred to as linking. It basically means that you compiled a bunch of implementation files into object files or libraries and now you want to get them to work together.
Say you defined symbol ``a in `a.cpp`. Now, `b.cpp` declared that symbol and used it. Before linking, it simply assumes that that symbol was defined somewhere, but it doesn't yet care where. The linking phase is responsible for finding the symbol and correctly linking it to `b.cpp` (well, actually to the object or library that uses it).
If you're using Microsoft Visual Studio, you'll see that projects generate `.lib` files. These contain a table of exported symbols, and a table of imported symbols. The imported symbols are resolved against the libraries you link against, and the exported symbols are provided for the libraries that use that `.lib` (if any).
Similar mechanisms exist for other compilers/ platforms.
Common error messages are `error LNK2001`, `error LNK1120`, `error LNK2019` for Microsoft Visual Studio and `undefined reference to` symbolName for GCC.
The code:

```python
struct X
{
   virtual void foo();
};
struct Y : X
{
   void foo() {}
};
struct A
{
   virtual ~A() = 0;
};
struct B: A
{
   virtual ~B(){}
};
extern int x;
void foo();
int main()
{
   x = 0;
   foo();
   Y y;
   B b;
}
```

will generate the following errors with GCC:

```python
/home/AbiSfw/ccvvuHoX.o: In function `main':
prog.cpp:(.text+0x10): undefined reference to `x'
prog.cpp:(.text+0x19): undefined reference to `foo()'
prog.cpp:(.text+0x2d): undefined reference to `A::~A()'
/home/AbiSfw/ccvvuHoX.o: In function `B::~B()':
prog.cpp:(.text._ZN1BD1Ev[B::~B()]+0xb): undefined reference to `A::~A()'
/home/AbiSfw/ccvvuHoX.o: In function `B::~B()':
prog.cpp:(.text._ZN1BD0Ev[B::~B()]+0x12): undefined reference to `A::~A()'
/home/AbiSfw/ccvvuHoX.o:(.rodata._ZTI1Y[typeinfo for Y]+0x8): undefined reference to `typeinfo for X'
/home/AbiSfw/ccvvuHoX.o:(.rodata._ZTI1B[typeinfo for B]+0x8): undefined reference to `typeinfo for A'
collect2: ld returned 1 exit status
```

and similar errors with Microsoft Visual Studio:

```python
1>test2.obj : error LNK2001: unresolved external symbol "void __cdecl foo(void)" (?foo@@YAXXZ)
1>test2.obj : error LNK2001: unresolved external symbol "int x" (?x@@3HA)
1>test2.obj : error LNK2001: unresolved external symbol "public: virtual __thiscall A::~A(void)" (??1A@@UAE@XZ)
1>test2.obj : error LNK2001: unresolved external symbol "public: virtual void __thiscall X::foo(void)" (?foo@X@@UAEXXZ)
1>...\test2.exe : fatal error LNK1120: 4 unresolved externals
```

Common causes include:

Failure to link against appropriate libraries/object files or compile implementation files
Declared and undefined variable or function.
Common issues with class-type members
Template implementations not visible.
Symbols were defined in a C program and used in C++ code.
Incorrectly importing/exporting methods/classes across modules/dll. (MSVS specific)
Circular library dependency
undefined reference to `WinMain@16'
Interdependent library order
Multiple source files of the same name
Mistyping or not including the .lib extension when using the `#pragma` (Microsoft Visual Studio)
Problems with template friends
Inconsistent `UNICODE` definitions

## [What is a lambda expression in C++11?](https://stackoverflow.com/questions/7627098/what-is-a-lambda-expression-in-c11)

**1155 Votes**, Nawaz

The problem
C++ includes useful generic functions like `std::for_each` and `std::transform`, which can be very handy. Unfortunately they can also be quite cumbersome to use, particularly if the functor you would like to apply is unique to the particular function.

```python
#include <algorithm>
#include <vector>

namespace {
  struct f {
    void operator()(int) {
      // do something
    }
  };
}

void func(std::vector<int>& v) {
  f f;
  std::for_each(v.begin(), v.end(), f);
}
```

If you only use f once and in that specific place it seems overkill to be writing a whole class just to do something trivial and one off.
In C++03 you might be tempted to write something like the following, to keep the functor local:

```python
void func2(std::vector<int>& v) {
  struct {
    void operator()(int) {
       // do something
    }
  } f;
  std::for_each(v.begin(), v.end(), f);
}
```

however this is not allowed, ``f cannot be passed to a template function in C++03.
The new solution
C++11 introduces lambdas allow you to write an inline, anonymous functor to replace the `struct f`. For small simple examples this can be cleaner to read (it keeps everything in one place) and potentially simpler to maintain, for example in the simplest form:

```python
void func3(std::vector<int>& v) {
  std::for_each(v.begin(), v.end(), [](int) { /* do something here*/ });
}
```

Lambda functions are just syntactic sugar for anonymous functors.

### Return types

In simple cases the return type of the lambda is deduced for you, e.g.:

```python
void func4(std::vector<double>& v) {
  std::transform(v.begin(), v.end(), v.begin(),
                 [](double d) { return d < 0.00001 ? 0 : d; }
                 );
}
```

however when you start to write more complex lambdas you will quickly encounter cases where the return type cannot be deduced by the compiler, e.g.:

```python
void func4(std::vector<double>& v) {
    std::transform(v.begin(), v.end(), v.begin(),
        [](double d) {
            if (d < 0.0001) {
                return 0;
            } else {
                return d;
            }
        });
}
```

To resolve this you are allowed to explicitly specify a return type for a lambda function, using `-> T`:

```python
void func4(std::vector<double>& v) {
    std::transform(v.begin(), v.end(), v.begin(),
        [](double d) -> double {
            if (d < 0.0001) {
                return 0;
            } else {
                return d;
            }
        });
}
```


### "Capturing" variables

So far we've not used anything other than what was passed to the lambda within it, but we can also use other variables, within the lambda. If you want to access other variables you can use the capture clause (the `[]` of the expression), which has so far been unused in these examples, e.g.:

```python
void func5(std::vector<double>& v, const double& epsilon) {
    std::transform(v.begin(), v.end(), v.begin(),
        [epsilon](double d) -> double {
            if (d < epsilon) {
                return 0;
            } else {
                return d;
            }
        });
}
```

You can capture by both reference and value, which you can specify using ``& and ``= respectively:

`[&epsilon]` capture by reference
`[&]` captures all variables used in the lambda by reference
`[=]` captures all variables used in the lambda by value
`[&, epsilon]` captures variables like with [&], but epsilon by value
`[=, &epsilon]` captures variables like with [=], but epsilon by reference

The generated `operator()` is `const` by default, with the implication that captures will be `const` when you access them by default. This has the effect that each call with the same input would produce the same result, however you can mark the lambda as `mutable` to request that the `operator()` that is produced is not `const`.

## [What are rvalues, lvalues, xvalues, glvalues, and prvalues?](https://stackoverflow.com/questions/3601602/what-are-rvalues-lvalues-xvalues-glvalues-and-prvalues)

**1071 Votes**, James McNellis

I guess this document might serve as a not so short introduction : n3055
The whole massacre began with the move semantics. Once we have expressions that can be moved and not copied, suddenly easy to grasp rules demanded distinction between expressions that can be moved, and in which direction.
From what I guess based on the draft, the r/l value distinction stays the same, only in the context of moving things get messy. 
Are they needed? Probably not if we wish to forfeit the new features. But to allow better optimization we should probably embrace them.
Quoting n3055:

An lvalue (so-called, historically,
because lvalues could appear on the
left-hand side  of an assignment
expression) designates a function or
an object.  [Example: If ``E is  an
expression of pointer type, then `*E`
is an lvalue expression referring to
the object  or function to which ``E
points.  As another example, the
result of calling a function  whose
return type is an lvalue reference is
an lvalue.] 
An xvalue (an
eXpiring value) also refers to an
object, usually near the end of its 
lifetime (so that its resources may
be moved, for example).  An xvalue is
the result  of certain kinds of
expressions involving rvalue
references.  [Example: The 
result of calling a function whose
return type is an rvalue reference is
an xvalue.]
A glvalue   (generalized lvalue) is an lvalue
or an xvalue. 
An rvalue (so-called,
historically, because rvalues could
appear on the right-hand  side of an
assignment expression) is an xvalue,
a temporary object or
subobject thereof, or a value that is
not associated with an object. 
A
prvalue (pure rvalue) is an rvalue
that is not an xvalue.  [Example: The
result  of calling a function whose
return type is not a reference is a
prvalue]

The document in question is a great reference for this question, because it shows the exact changes in the standard that have happened as a result of the introduction of the new nomenclature.

## [Replacing a 32-bit loop count variable with 64-bit introduces crazy performance deviations](https://stackoverflow.com/questions/25078285/replacing-a-32-bit-loop-count-variable-with-64-bit-introduces-crazy-performance)

**1046 Votes**, gexicide

Culprit: False Data Dependency (and the compiler isn't even aware of it)
On Sandy/Ivy Bridge and Haswell processors, the instruction:

```python
popcnt  src, dest
```

appears to have a false dependency on the destination register `dest`. Even though the instruction only writes to it, the instruction will wait until `dest` is ready before executing.
This dependency doesn't just hold up the 4 `popcnt`s from a single loop iteration. It can carry across loop iterations making it impossible for the processor to parallelize different loop iterations.
The `unsigned` vs. `uint64_t` and other tweaks don't directly affect the problem. But they influence the register allocator which assigns the registers to the variables.
In your case, the speeds are a direct result of what is stuck to the (false) dependency chain depending on what the register allocator decided to do.

13 GB/s has a chain: `popcnt`-`add`-`popcnt`-`popcnt`  next iteration
15 GB/s has a chain: `popcnt`-`add`-`popcnt`-`add`  next iteration
20 GB/s has a chain: `popcnt`-`popcnt`  next iteration
26 GB/s has a chain: `popcnt`-`popcnt`  next iteration

The difference between 20 GB/s and 26 GB/s seems to be a minor artifact of the indirect addressing. Either way, the processor starts to hit other bottlenecks once you reach this speed.

To test this, I used inline assembly to bypass the compiler and get exactly the assembly I want. I also split up the `count` variable to break all other dependencies that might mess with the benchmarks.
Here are the results:
Sandy Bridge Xeon @ 3.5 GHz: (full test code can be found at the bottom)

GCC 4.6.3: `g++ popcnt.cpp -std=c++0x -O3 -save-temps -march=native`
Ubuntu 12

Different Registers: 18.6195 GB/s

```python
.L4:
    movq    (%rbx,%rax,8), %r8
    movq    8(%rbx,%rax,8), %r9
    movq    16(%rbx,%rax,8), %r10
    movq    24(%rbx,%rax,8), %r11
    addq    $4, %rax

    popcnt %r8, %r8
    add    %r8, %rdx
    popcnt %r9, %r9
    add    %r9, %rcx
    popcnt %r10, %r10
    add    %r10, %rdi
    popcnt %r11, %r11
    add    %r11, %rsi

    cmpq    $131072, %rax
    jne .L4
```

Same Register: 8.49272 GB/s

```python
.L9:
    movq    (%rbx,%rdx,8), %r9
    movq    8(%rbx,%rdx,8), %r10
    movq    16(%rbx,%rdx,8), %r11
    movq    24(%rbx,%rdx,8), %rbp
    addq    $4, %rdx

    # This time reuse "rax" for all the popcnts.
    popcnt %r9, %rax
    add    %rax, %rcx
    popcnt %r10, %rax
    add    %rax, %rsi
    popcnt %r11, %rax
    add    %rax, %r8
    popcnt %rbp, %rax
    add    %rax, %rdi

    cmpq    $131072, %rdx
    jne .L9
```

Same Register with broken chain: 17.8869 GB/s

```python
.L14:
    movq    (%rbx,%rdx,8), %r9
    movq    8(%rbx,%rdx,8), %r10
    movq    16(%rbx,%rdx,8), %r11
    movq    24(%rbx,%rdx,8), %rbp
    addq    $4, %rdx

    # Reuse "rax" for all the popcnts.
    xor    %rax, %rax    # Break the cross-iteration dependency by zeroing "rax".
    popcnt %r9, %rax
    add    %rax, %rcx
    popcnt %r10, %rax
    add    %rax, %rsi
    popcnt %r11, %rax
    add    %rax, %r8
    popcnt %rbp, %rax
    add    %rax, %rdi

    cmpq    $131072, %rdx
    jne .L14
```


So what went wrong with the compiler?
It seems that neither GCC nor Visual Studio are aware that `popcnt` has such a false dependency. Nevertheless, these false dependencies aren't uncommon. It's just a matter of whether the compiler is aware of it.
`popcnt` isn't exactly the most used instruction. So it's not really a surprise that a major compiler could miss something like this. There also appears to be no documentation anywhere that mentions this problem. If Intel doesn't disclose it, then nobody outside will know until someone runs into it by chance.
(Update: As of version 4.9.2, GCC is aware of this false-dependency and generates code to compensate it when optimizations are enabled. Major compilers from other vendors, including Clang, MSVC, and even Intel's own ICC are not yet aware of this microarchitectural erratum and will not emit code that compensates for it.)
Why does the CPU have such a false dependency?
We can only speculate, but it's likely that Intel has the same handling for a lot of two-operand instructions. Common instructions like `add`, `sub` take two operands both of which are inputs. So Intel probably shoved `popcnt` into the same category to keep the processor design simple.
AMD processors do not appear to have this false dependency.

The full test code is below for reference:

```python
#include <iostream>
#include <chrono>
#include <x86intrin.h>

int main(int argc, char* argv[]) {

   using namespace std;
   uint64_t size=1<<20;

   uint64_t* buffer = new uint64_t[size/8];
   char* charbuffer=reinterpret_cast<char*>(buffer);
   for (unsigned i=0;i<size;++i) charbuffer[i]=rand()%256;

   uint64_t count,duration;
   chrono::time_point<chrono::system_clock> startP,endP;
   {
      uint64_t c0 = 0;
      uint64_t c1 = 0;
      uint64_t c2 = 0;
      uint64_t c3 = 0;
      startP = chrono::system_clock::now();
      for( unsigned k = 0; k < 10000; k++){
         for (uint64_t i=0;i<size/8;i+=4) {
            uint64_t r0 = buffer[i + 0];
            uint64_t r1 = buffer[i + 1];
            uint64_t r2 = buffer[i + 2];
            uint64_t r3 = buffer[i + 3];
            __asm__(
                "popcnt %4, %4  \n\t"
                "add %4, %0     \n\t"
                "popcnt %5, %5  \n\t"
                "add %5, %1     \n\t"
                "popcnt %6, %6  \n\t"
                "add %6, %2     \n\t"
                "popcnt %7, %7  \n\t"
                "add %7, %3     \n\t"
                : "+r" (c0), "+r" (c1), "+r" (c2), "+r" (c3)
                : "r"  (r0), "r"  (r1), "r"  (r2), "r"  (r3)
            );
         }
      }
      count = c0 + c1 + c2 + c3;
      endP = chrono::system_clock::now();
      duration=chrono::duration_cast<std::chrono::nanoseconds>(endP-startP).count();
      cout << "No Chain\t" << count << '\t' << (duration/1.0E9) << " sec \t"
            << (10000.0*size)/(duration) << " GB/s" << endl;
   }
   {
      uint64_t c0 = 0;
      uint64_t c1 = 0;
      uint64_t c2 = 0;
      uint64_t c3 = 0;
      startP = chrono::system_clock::now();
      for( unsigned k = 0; k < 10000; k++){
         for (uint64_t i=0;i<size/8;i+=4) {
            uint64_t r0 = buffer[i + 0];
            uint64_t r1 = buffer[i + 1];
            uint64_t r2 = buffer[i + 2];
            uint64_t r3 = buffer[i + 3];
            __asm__(
                "popcnt %4, %%rax   \n\t"
                "add %%rax, %0      \n\t"
                "popcnt %5, %%rax   \n\t"
                "add %%rax, %1      \n\t"
                "popcnt %6, %%rax   \n\t"
                "add %%rax, %2      \n\t"
                "popcnt %7, %%rax   \n\t"
                "add %%rax, %3      \n\t"
                : "+r" (c0), "+r" (c1), "+r" (c2), "+r" (c3)
                : "r"  (r0), "r"  (r1), "r"  (r2), "r"  (r3)
                : "rax"
            );
         }
      }
      count = c0 + c1 + c2 + c3;
      endP = chrono::system_clock::now();
      duration=chrono::duration_cast<std::chrono::nanoseconds>(endP-startP).count();
      cout << "Chain 4   \t"  << count << '\t' << (duration/1.0E9) << " sec \t"
            << (10000.0*size)/(duration) << " GB/s" << endl;
   }
   {
      uint64_t c0 = 0;
      uint64_t c1 = 0;
      uint64_t c2 = 0;
      uint64_t c3 = 0;
      startP = chrono::system_clock::now();
      for( unsigned k = 0; k < 10000; k++){
         for (uint64_t i=0;i<size/8;i+=4) {
            uint64_t r0 = buffer[i + 0];
            uint64_t r1 = buffer[i + 1];
            uint64_t r2 = buffer[i + 2];
            uint64_t r3 = buffer[i + 3];
            __asm__(
                "xor %%rax, %%rax   \n\t"   // <--- Break the chain.
                "popcnt %4, %%rax   \n\t"
                "add %%rax, %0      \n\t"
                "popcnt %5, %%rax   \n\t"
                "add %%rax, %1      \n\t"
                "popcnt %6, %%rax   \n\t"
                "add %%rax, %2      \n\t"
                "popcnt %7, %%rax   \n\t"
                "add %%rax, %3      \n\t"
                : "+r" (c0), "+r" (c1), "+r" (c2), "+r" (c3)
                : "r"  (r0), "r"  (r1), "r"  (r2), "r"  (r3)
                : "rax"
            );
         }
      }
      count = c0 + c1 + c2 + c3;
      endP = chrono::system_clock::now();
      duration=chrono::duration_cast<std::chrono::nanoseconds>(endP-startP).count();
      cout << "Broken Chain\t"  << count << '\t' << (duration/1.0E9) << " sec \t"
            << (10000.0*size)/(duration) << " GB/s" << endl;
   }

   free(charbuffer);
}
```


An equally interesting benchmark can be found here: http://pastebin.com/kbzgL8si

This benchmark varies the number of `popcnt`s that are in the (false) dependency chain.

```python
False Chain 0:  41959360000 0.57748 sec     18.1578 GB/s
False Chain 1:  41959360000 0.585398 sec    17.9122 GB/s
False Chain 2:  41959360000 0.645483 sec    16.2448 GB/s
False Chain 3:  41959360000 0.929718 sec    11.2784 GB/s
False Chain 4:  41959360000 1.23572 sec     8.48557 GB/s
```

## [What is the difference between const int*, const int * const, and int const *?](https://stackoverflow.com/questions/1143262/what-is-the-difference-between-const-int-const-int-const-and-int-const)

**951 Votes**, 
        ultraman
        



Read it backwards (as driven by Clockwise/Spiral Rule):

`int*` - pointer to int
`int const *` - pointer to const int
`int * const` - const pointer to int
`int const * const` - const pointer to const int

Now the first `const` can be on either side of the type so:

`const int *` == `int const *`
`const int * const` == `int const * const`

If you want to go really crazy you can do things like this:

`int **` - pointer to pointer to int
`int ** const` - a const pointer to a pointer to an int
`int * const *` - a pointer to a const pointer to an int
`int const **` - a pointer to a pointer to a const int
`int * const * const` - a const pointer to a const pointer to an int
...

And to make sure we are clear on the meaning of const

```python
const int* foo;
int *const bar; //note, you actually need to set the pointer 
                //here because you can't change it later ;)
```

`foo` is a variable pointer to a constant integer. This lets you change what you point to but not the value that you point to. Most often this is seen with C-style strings where you have a pointer to a `const char`. You may change which string you point to but you can't change the content of these strings. This is important when the string itself is in the data segment of a program and shouldn't be changed.
`bar` is a constant or fixed pointer to a value that can be changed. This is like a reference without the extra syntactic sugar. Because of this fact, usually you would use a reference where you would use a `T* const` pointer unless you need to allow `NULL` pointers.

## [Why do we need virtual functions in C++?](https://stackoverflow.com/questions/2391679/why-do-we-need-virtual-functions-in-c)

**926 Votes**, Jake Wilson

Here is how I understood not just what `virtual` functions are, but why they're required:
Let's say you have these two classes:

```python
class Animal
{
    public:
        void eat() { std::cout << "I'm eating generic food."; }
};

class Cat : public Animal
{
    public:
        void eat() { std::cout << "I'm eating a rat."; }
};
```

In your main function:

```python
Animal *animal = new Animal;
Cat *cat = new Cat;

animal->eat(); // Outputs: "I'm eating generic food."
cat->eat();    // Outputs: "I'm eating a rat."
```

So far so good, right? Animals eat generic food, cats eat rats, all without `virtual`.
Let's change it a little now so that `eat()` is called via an intermediate function (a trivial function just for this example):

```python
// This can go at the top of the main.cpp file
void func(Animal *xyz) { xyz->eat(); }
```

Now our main function is:

```python
Animal *animal = new Animal;
Cat *cat = new Cat;

func(animal); // Outputs: "I'm eating generic food."
func(cat);    // Outputs: "I'm eating generic food."
```

Uh oh... we passed a Cat into `func()`, but it won't eat rats. Should you overload `func()` so it takes a `Cat*`? If you have to derive more animals from Animal they would all need their own `func()`.
The solution is to make `eat()` from the `Animal` class a virtual function:

```python
class Animal
{
    public:
        virtual void eat() { std::cout << "I'm eating generic food."; }
};

class Cat : public Animal
{
    public:
        void eat() { std::cout << "I'm eating a rat."; }
};
```

Main:

```python
func(animal); // Outputs: "I'm eating generic food."
func(cat);    // Outputs: "I'm eating a rat."
```

Done.

## [Undefined behavior and sequence points](https://stackoverflow.com/questions/4176328/undefined-behavior-and-sequence-points)

**885 Votes**, community-wiki

C++98 and C++03
This answer is for the older versions of the C++ standard.  The C++11 and C++14 versions of the standard do not formally contain 'sequence points'; operations are 'sequenced before' or 'unsequenced' or 'indeterminately sequenced' instead.  The net effect is essentially the same, but the terminology is different.

Disclaimer : Okay. This answer is a bit long. So have patience while reading it. If you already know these things, reading them again won't make you crazy. 
Pre-requisites : An elementary knowledge of C++ Standard 


### What are Sequence Points?

The Standard says 

At  certain specified points in the execution sequence called sequence points, all side effects of previous evaluations 
  shall be complete and no side effects of subsequent evaluations shall have taken place. (1.9/7)


### Side effects? What are side effects?

Evaluation  of  an  expression produces something and if in addition there is a change in the state of the execution environment it is said that the expression (its evaluation) has some side effect(s).
For example:

```python
int x = y++; //where y is also an int
```

In addition to the initialization operation the value of ``y gets changed due to the side effect of `++` operator. 
So far so good. Moving on to sequence points. An alternation definition of seq-points given by the comp.lang.c author `Steve Summit`:

Sequence point is a point in time at which the dust has settled and all side effects which have been seen so far are guaranteed to be complete.



### What are the common sequence points listed in the C++ Standard ?

Those are:

at the end of the evaluation of full expression (`1.9/16`) (A full-expression is an expression that is not a subexpression of another expression.)1

Example :

```python
int a = 5; // ; is a sequence point here
```


in the evaluation of each of the following expressions after the evaluation of the first expression(`1.9/18`) 2

`a && b (5.14)` 
`a || b (5.15)`
`a ? b : c (5.16)`
`a , b (5.18)` (here a , b is a comma operator; in `func(a,a++)` ``, is not a comma operator, it's merely a separator between the arguments ``a and `a++`. Thus the behaviour is undefined in that case (if ``a is considered to be a primitive type)) 

at a function call (whether or not the function is inline), after the evaluation of all function arguments (if any) which 
takes place before execution of any expressions or statements in the function body (`1.9/17`).

1 : Note : the evaluation of a full-expression can include the evaluation of subexpressions that are not lexically
part of the full-expression.  For example, subexpressions involved in evaluating default argument expressions (8.3.6) are considered to be created in the expression that calls the function, not the expression that defines the default argument
2 : The operators indicated are the built-in operators, as described in clause 5.  When one of these operators is overloaded (clause 13) in a valid context, thus designating a user-defined operator function, the expression designates a function invocation and the operands form an argument list, without an implied sequence point between them.


### What is Undefined Behaviour?

The Standard defines Undefined Behaviour in Section `1.3.12` as

behaviour, such as might arise upon use of an erroneous program construct or erroneous data, for which this International Standard imposes no  requirements 3.
Undefined  behaviour  may  also  be  expected  when  this
  International Standard omits the description of any explicit definition of behavior.

 3 : permissible undefined behavior ranges from ignoring the situation completely with unpredictable results, to behaving during translation or program execution in a documented manner characteristic of the environment (with or with-
out the issuance of a diagnostic message), to terminating a translation or execution (with the issuance of a diagnostic message).
In short, undefined behaviour means anything can happen from daemons flying out of your nose to  your girlfriend getting pregnant.


### What is the relation between Undefined Behaviour and Sequence Points?

Before I get into that you must know the difference(s) between Undefined Behaviour, Unspecified Behaviour and Implementation Defined Behaviour.
You must also know that `the order of evaluation of operands of individual operators and subexpressions of individual expressions, and the order in which side effects take place, is unspecified`.
For example:

```python
int x = 5, y = 6;

int z = x++ + y++; //it is unspecified whether x++ or y++ will be evaluated first.
```

Another example here.

Now the Standard in `5/4` says

1) Between the previous and next sequence point a scalar object shall have its stored value modified at most once by the evaluation of an expression. 

What does it mean?
Informally it means that between two sequence points a variable must not be modified more than once.
In an expression statement, the `next sequence point` is usually at the terminating semicolon, and the `previous sequence point` is at the end of the previous statement. An expression may also contain intermediate `sequence points`.
From the above sentence the following expressions invoke Undefined Behaviour:

```python
i++ * ++i;   // UB, i is modified more than once btw two SPs
i = ++i;     // UB, same as above
++i = 2;     // UB, same as above
i = ++i + 1; // UB, same as above
++++++i;     // UB, parsed as (++(++(++i)))

i = (i, ++i, ++i); // UB, there's no SP between `++i` (right most) and assignment to `i` (`i` is modified more than once btw two SPs)
```

But the following expressions are fine:

```python
i = (i, ++i, 1) + 1; // well defined (AFAIK)
i = (++i, i++, i);   // well defined 
int j = i;
j = (++i, i++, j*i); // well defined
```



2) Furthermore, the prior value shall be accessed only to determine the value to be stored.

What does it mean? It means if an object is written to within a full expression, any and all accesses to it within the same expression must be directly involved in the computation of the value to be written. 
For example in `i = i + 1` all the access of ``i (in L.H.S and in R.H.S) are directly involved in computation of the value to be written. So it is fine.
This rule effectively constrains legal expressions to those in which the accesses demonstrably precede the modification.
Example 1:

```python
std::printf("%d %d", i,++i); // invokes Undefined Behaviour because of Rule no 2
```

Example 2:

```python
a[i] = i++ // or a[++i] = i or a[i++] = ++i etc
```

is disallowed because one of the accesses of ``i (the one in `a[i]`) has nothing to do with the value which ends up being stored in i (which happens over in `i++`), and so there's no good way to define--either for our understanding or the compiler's--whether the access should take place before or after the incremented value is stored. So the behaviour is undefined.
Example 3 :

```python
int x = i + i++ ;// Similar to above
```


Follow up answer here.

## [Do the parentheses after the type name make a difference with new?](https://stackoverflow.com/questions/620137/do-the-parentheses-after-the-type-name-make-a-difference-with-new)

**873 Votes**, David Read

Let's get pedantic, because there are differences that can actually affect your code's behavior. Much of the following is taken from comments made to an "Old New Thing" article.
Sometimes the memory returned by the new operator will be initialized, and sometimes it won't depending on whether the type you're newing up is a POD (plain old data), or if it's a class that contains POD members and is using a compiler-generated default constructor.

In C++1998 there are 2 types of initialization: zero and default
In C++2003 a 3rd type of initialization, value initialization was added.

Assume:

```python
struct A { int m; }; // POD
struct B { ~B(); int m; }; // non-POD, compiler generated default ctor
struct C { C() : m() {}; ~C(); int m; }; // non-POD, default-initialising m
```

In a C++98 compiler, the following should occur:

`new A`   - indeterminate value
`new A()` - zero-initialize
`new B`   - default construct (B::m is uninitialized)
`new B()` - default construct (B::m is uninitialized)
`new C`   - default construct (C::m is zero-initialized)
`new C()` - default construct (C::m is zero-initialized)

In a C++03 conformant compiler, things should work like so:

`new A`    - indeterminate value
`new A()`  - value-initialize A, which is zero-initialization since it's a POD.
`new B`    - default-initializes (leaves B::m uninitialized)
`new B()`  - value-initializes B which zero-initializes all fields since its default ctor is compiler generated as opposed to user-defined.
`new C`    - default-initializes C, which calls the default ctor.
`new C()`  - value-initializes C, which calls the default ctor.

So in all versions of C++ there's a difference between `new A` and `new A()` because A is a POD.
And there's a difference in behavior between C++98 and C++03 for the case `new B()`.
This is one of the dusty corners of C++ that can drive you crazy. When constructing an object, sometimes you want/need the parens, sometimes you absolutely cannot have them, and sometimes it doesn't matter.

## [Where and why do I have to put the template and typename keywords?](https://stackoverflow.com/questions/610245/where-and-why-do-i-have-to-put-the-template-and-typename-keywords)

**862 Votes**, MSalters

In order to parse a C++ program, the compiler needs to know whether certain names are types or not. The following example demonstrates that:

```python
t * f;
```

How should this be parsed? For many languages a compiler doesn't need to know the meaning of a name in order to parse and basically know what action a line of code does. In C++, the above however can yield vastly different interpretations depending on what ``t means. If it's a type, then it will be a declaration of a pointer ``f. However if it's not a type, it will be a multiplication. So the C++ Standard says at paragraph (3/7):

Some names denote types or templates. In general, whenever a name is encountered it is necessary to determine whether that name denotes one of these entities before continuing to parse the program that contains it. The process that determines this is called name lookup.

How will the compiler find out what a name `t::x` refers to, if ``t refers to a template type parameter? ``x could be a static int data member that could be multiplied or could equally well be a nested class or typedef that could yield to a declaration. If a name has this property - that it can't be looked up until the actual template arguments are known - then it's called a dependent name (it "depends" on the template parameters). 
You might recommend to just wait till the user instantiates the template: 

Let's wait until the user instantiates the template, and then later find out the real meaning of `t::x * f;`. 

This will work and actually is allowed by the Standard as a possible implementation approach. These compilers basically copy the template's text into an internal buffer, and only when an instantiation is needed, they parse the template and possibly detect errors in the definition. But instead of bothering the template's users (poor colleagues!) with errors made by a template's author, other implementations choose to check templates early on and give errors in the definition as soon as possible, before an instantiation even takes place. 
So there has to be a way to tell the compiler that certain names are types and that certain names aren't. 

### The "typename" keyword

The answer is: We decide how the compiler should parse this. If `t::x` is a dependent name, then we need to prefix it by `typename` to tell the compiler to parse it in a certain way. The Standard says at (14.6/2):

A name used in a template declaration or definition and that is dependent on a template-parameter is
  assumed not to name a type unless the applicable name lookup finds a type name or the name is qualified
  by the keyword typename. 

There are many names for which `typename` is not necessary, because the compiler can, with the applicable name lookup in the template definition, figure out how to parse a construct itself - for example with `T *f;`, when ``T is a type template parameter. But for `t::x * f;` to be a declaration, it must be written as `typename t::x *f;`. If you omit the keyword and the name is taken to be a non-type, but when instantiation finds it denotes a type, the usual error messages are emitted by the compiler. Sometimes, the error consequently is given at definition time:

```python
// t::x is taken as non-type, but as an expression the following misses an
// operator between the two names or a semicolon separating them.
t::x f;
```

The syntax allows `typename` only before qualified names - it is therefor taken as granted that unqualified names are always known to refer to types if they do so.
A similar gotcha exists for names that denote templates, as hinted at by the introductory text.

### The "template" keyword

Remember the initial quote above and how the Standard requires special handling for templates as well? Let's take the following innocent-looking example: 

```python
boost::function< int() > f;
```

It might look obvious to a human reader. Not so for the compiler. Imagine the following arbitrary definition of `boost::function` and ``f:

```python
namespace boost { int function = 0; }
int main() { 
  int f = 0;
  boost::function< int() > f; 
}
```

That's actually a valid expression! It uses the less-than operator to compare `boost::function` against zero (`int()`), and then uses the greater-than operator to compare the resulting `bool` against ``f. However as you might well know, `boost::function` in real life is a template, so the compiler knows (14.2/3):

After name lookup (3.4) finds that a name is a template-name, if this name is followed by a <, the < is
  always taken as the beginning of a template-argument-list and never as a name followed by the less-than
  operator.

Now we are back to the same problem as with `typename`. What if we can't know yet whether the name is a template when parsing the code? We will need to insert `template` immediately before the template name, as specified by `14.2/4`. This looks like:

```python
t::template f<int>(); // call a function template
```

Template names can not only occur after a `::` but also after a `->` or ``. in a class member access. You need to insert the keyword there too:

```python
this->template f<int>(); // call a function template
```



### Dependencies

For the people that have thick Standardese books on their shelf and that want to know what exactly I was talking about, I'll talk a bit about how this is specified in the Standard.
In template declarations some constructs have different meanings depending on what template arguments you use to instantiate the template: Expressions may have different types or values, variables may have different types or function calls might end up calling different functions. Such constructs are generally said to depend on template parameters.
The Standard defines precisely the rules by whether a construct is dependent or not. It separates them into logically different groups: One catches types, another catches expressions. Expressions may depend by their value and/or their type. So we have, with typical examples appended:

Dependent types (e.g: a type template parameter ``T)
Value-dependent expressions (e.g: a non-type template parameter ``N)
Type-dependent expressions (e.g: a cast to a type template parameter `(T)0`)

Most of the rules are intuitive and are built up recursively: For example, a type constructed as `T[N]` is a dependent type if ``N is a value-dependent expression or ``T is a dependent type. The details of this can be read in section `(14.6.2/1`) for dependent types, `(14.6.2.2)` for type-dependent expressions and `(14.6.2.3)` for value-dependent expressions. 
Dependent names
The Standard is a bit unclear about what exactly is a dependent name. On a simple read (you know, the principle of least surprise), all it defines as a dependent name is the special case for function names below. But since clearly `T::x` also needs to be looked up in the instantiation context, it also needs to be a dependent name (fortunately, as of mid C++14 the committee has started to look into how to fix this confusing definition). 
To avoid this problem, I have resorted to a simple interpretation of the Standard text. Of all the constructs that denote dependent types or expressions, a subset of them represent names. Those names are therefore "dependent names". A name can take different forms - the Standard says:

A name is a use of an identifier (2.11), operator-function-id (13.5), conversion-function-id (12.3.2), or template-id (14.2) that denotes an entity or label (6.6.4, 6.1)

An identifier is just a plain sequence of characters / digits, while the next two are the `operator +` and `operator type` form. The last form is `template-name <argument list>`. All these are names, and by conventional use in the Standard, a name can also include qualifiers that say what namespace or class a name should be looked up in.
A value dependent expression `1 + N` is not a name, but ``N is. The subset of all dependent constructs that are names is called dependent name. Function names, however, may have different meaning in different instantiations of a template, but unfortunately are not caught by this general rule. 
Dependent function names
Not primarily a concern of this article, but still worth mentioning: Function names are an exception that are handled separately. An identifier function name is dependent not by itself, but by the type dependent argument expressions used in a call. In the example `f((T)0)`, ``f is a dependent name. In the Standard, this is specified at `(14.6.2/1)`.

### Additional notes and examples

In enough cases we need both of `typename` and `template`. Your code should look like the following

```python
template <typename T, typename Tail>
struct UnionNode : public Tail {
    // ...
    template<typename U> struct inUnion {
        typedef typename Tail::template inUnion<U> dummy;
    };
    // ...
};
```

The keyword `template` doesn't always have to appear in the last part of a name. It can appear in the middle before a class name that's used as a scope, like in the following example

```python
typename t::template iterator<int>::value_type v;
```

In some cases, the keywords are forbidden, as detailed below

On the name of a dependent base class you are not allowed to write `typename`. It's assumed that the name given is a class type name. This is true for both names in the base-class list and the constructor initializer list:

```python
 template <typename T>
 struct derive_from_Has_type : /* typename */ SomeBase<T>::type 
 { };
```

In using-declarations it's not possible to use `template` after the last `::`, and the C++ committee said not to work on a solution. 

```python
 template <typename T>
 struct derive_from_Has_type : SomeBase<T> {
    using SomeBase<T>::template type; // error
    using typename SomeBase<T>::type; // typename *is* allowed
 };
```

## [Can a local variable's memory be accessed outside its scope?](https://stackoverflow.com/questions/6441218/can-a-local-variables-memory-be-accessed-outside-its-scope)

**852 Votes**, community-wiki

How can it be? Isn't the memory of a local variable inaccessible outside its function?

You rent a hotel room. You put a book in the top drawer of the bedside table and go to sleep.  You check out the next morning, but "forget" to give back your key. You steal the key!
A week later, you return to the hotel, do not check in, sneak into your old room with your stolen key, and look in the drawer. Your book is still there. Astonishing!
How can that be? Aren't the contents of a hotel room drawer inaccessible if you haven't rented the room?
Well, obviously that scenario can happen in the real world no problem. There is no mysterious force that causes your book to disappear when you are no longer authorized to be in the room. Nor is there a mysterious force that prevents you from entering a room with a stolen key.
The hotel management is not required to remove your book. You didn't make a contract with them that said that if you leave stuff behind, they'll shred it for you. If you illegally re-enter your room with a stolen key to get it back, the hotel security staff is not required to catch you sneaking in. You didn't make a contract with them that said "if I try to sneak back into my room later, you are required to stop me." Rather, you signed a contract with them that said "I promise not to sneak back into my room later", a contract which you broke.
In this situation anything can happen. The book can be there -- you got lucky. Someone else's book can be there and yours could be in the hotel's furnace. Someone could be there right when you come in, tearing your book to pieces. The hotel could have removed the table and book entirely and replaced it with a wardrobe. The entire hotel could be just about to be torn down and replaced with a football stadium, and you are going to die in an explosion while you are sneaking around. 
You don't know what is going to happen; when you checked out of the hotel and stole a key to illegally use later, you gave up the right to live in a predictable, safe world because you chose to break the rules of the system.
C++ is not a safe language. It will cheerfully allow you to break the rules of the system. If you try to do something illegal and foolish like going back into a room you're not authorized to be in and rummaging through a desk that might not even be there anymore, C++ is not going to stop you. Safer languages than C++ solve this problem by restricting your power -- by having much stricter control over keys, for example.

### UPDATE

Holy goodness, this answer is getting a lot of attention. (I'm not sure why -- I considered it to be just a "fun" little analogy, but whatever.)
I thought it might be germane to update this a bit with a few more technical thoughts.
Compilers are in the business of generating code which manages the storage of the data manipulated by that program. There are lots of different ways of generating code to manage memory, but over time two basic techniques have become entrenched. 
The first is to have some sort of "long lived" storage area where the "lifetime" of each byte in the storage -- that is, the period of time when it is validly associated with some program variable -- cannot be easily predicted ahead of time. The compiler generates calls into a "heap manager" that knows how to dynamically allocate storage when it is needed and reclaim it when it is no longer needed.
The second is to have some sort of "short lived" storage area where the lifetime of each byte in the storage is well known, and, in particular, lifetimes of storages follow a "nesting" pattern. That is, the allocation of the longest-lived of the short-lived variables strictly overlaps the allocations of shorter-lived variables that come after it. 
Local variables follow the latter pattern; when a method is entered, its local variables come alive. When that method calls another method, the new method's local variables come alive. They'll be dead before the first method's local variables are dead.  The relative order of the beginnings and endings of lifetimes of storages associated with local variables can be worked out ahead of time.
For this reason, local variables are usually generated as storage on a "stack" data structure, because a stack has the property that the first thing pushed on it is going to be the last thing popped off. 
It's like the hotel decides to only rent out rooms sequentially, and you can't check out until everyone with a room number higher than you has checked out. 
So let's think about the stack. In many operating systems you get one stack per thread and the stack is allocated to be a certain fixed size. When you call a method, stuff is pushed onto the stack. If you then pass a pointer to the stack back out of your method, as the original poster does here, that's just a pointer to the middle of some entirely valid million-byte memory block. In our analogy, you check out of the hotel; when you do, you just checked out of the highest-numbered occupied room.  If no one else checks in after you, and you go back to your room illegally, all your stuff is guaranteed to still be there in this particular hotel.
We use stacks for temporary stores because they are really cheap and easy. An implementation of C++ is not required to use a stack for storage of locals; it could use the heap. It doesn't, because that would make the program slower. 
An implementation of C++ is not required to leave the garbage you left on the stack untouched so that you can come back for it later illegally; it is perfectly legal for the compiler to generate code that turns back to zero everything in the "room" that you just vacated. It doesn't because again, that would be expensive.
An implementation of C++ is not required to ensure that when the stack logically shrinks, the addresses that used to be valid are still mapped into memory. The implementation is allowed to tell the operating system "we're done using this page of stack now. Until I say otherwise, issue an exception that destroys the process if anyone touches the previously-valid stack page".  Again, implementations do not actually do that because it is slow and unnecessary.
Instead, implementations let you make mistakes and get away with it. Most of the time. Until one day something truly awful goes wrong and the process explodes.
This is problematic. There are a lot of rules and it is very easy to break them accidentally. I certainly have many times. And worse, the problem often only surfaces when memory is detected to be corrupt billions of nanoseconds after the corruption happened, when it is very hard to figure out who messed it up.
More memory-safe languages solve this problem by restricting your power. In "normal" C# there simply is no way to take the address of a local and return it or store it for later. You can take the address of a local, but the language is cleverly designed so that it is impossible to use it after the lifetime of the local ends. In order to take the address of a local and pass it back, you have to put the compiler in a special "unsafe" mode, and put the word "unsafe" in your program, to call attention to the fact that you are probably doing something dangerous that could be breaking the rules. 
For further reading:

What if C# did allow returning references? Coincidentally that is the subject of today's blog post:
http://blogs.msdn.com/b/ericlippert/archive/2011/06/23/ref-returns-and-ref-locals.aspx
Why do we use stacks to manage memory? Are value types in C# always stored on the stack? How does virtual memory work? And many more topics in how the C# memory manager works. Many of these articles are also germane to C++ programmers:
https://blogs.msdn.microsoft.com/ericlippert/tag/memory-management/

## [What are the new features in C++17?](https://stackoverflow.com/questions/38060436/what-are-the-new-features-in-c17)

**791 Votes**, Yakk - Adam Nevraumont

Language features:

### Templates and Generic Code


Template argument deduction for class templates

Like how functions deduce template arguments, now constructors can deduce the template arguments of the class
http://wg21.link/p0433r2 http://wg21.link/p0620r0 http://wg21.link/p0512r0

`template <auto>`

Represents a value of any (non-type template argument) type.

Non-type template arguments fixes
`template<template<class...>typename bob> struct foo {}`
( Folding + ... + expressions )  and Revisions
`auto x{8};` is an `int`
modernizing `using` with `...` and lists


### Lambda


constexpr lambdas

Lambdas are implicitly constexpr if they qualify

Capturing `*this` in lambdas

`[*this]{ std::cout << could << " be " << useful << '\n'; }`



### Attributes


`[[fallthrough]]`, `[[nodiscard]]`, `[[maybe_unused]]` attributes 
`[[attributes]]` on `namespace`s and `enum { erator[[s]] }`
`using` in attributes to avoid having to repeat an attribute namespace.
Compilers are now required to ignore non-standard attributes they don't recognize.

The C++14 wording allowed compilers to reject unknown scoped attributes.



### Syntax cleanup


Inline variables

Like inline functions
Compiler picks where the instance is instantiated
Deprecate static constexpr redeclaration, now implicitly inline.

`namespace A::B`
Simple `static_assert(expression);` with no string
no `throw` unless `throw()`, and `throw()` is `noexcept(true)`.


### Cleaner multi-return and flow control


Structured bindings

Basically, first-class `std::tie` with `auto`
Example:


`const auto [it, inserted] = map.insert( {"foo", bar} );`
Creates variables `it` and `inserted` with deduced type from the `pair` that `map::insert` returns.

Works with tuple/pair-likes & `std::array`s and relatively flat structs
Actually named structured bindings in standard

`if (init; condition)` and `switch (init; condition)`

`if (const auto [it, inserted] = map.insert( {"foo", bar} ); inserted)`
Extends the `if(decl)` to cases where `decl` isn't convertible-to-bool sensibly.

Generalizing range-based for loops

Appears to be mostly support for sentinels, or end iterators that are not the same type as begin iterators, which helps with null-terminated loops and the like.

if constexpr

Much requested feature to simplify almost-generic code.



### Misc


Hexadecimal float point literals
Dynamic memory allocation for over-aligned data
Guaranteed copy elision

Finally!
Not in all cases, but distinguishes syntax where you are "just creating something" that was called elision, from "genuine elision".

Fixed order-of-evaluation for (some) expressions with some modifications

Not including function arguments, but function argument evaluation interleaving now banned
Makes a bunch of broken code work mostly, and makes `.then` on future work.

Direct list-initialization of enums
Forward progress guarantees (FPG) (also, FPGs for parallel algorithms)

I think this is saying "the implementation may not stall threads forever"?

`u8'U', u8'T', u8'F', u8'8'` character literals (string already existed)
"noexcept" in the type system
`__has_include`

Test if a header file include would be an error
makes migrating from experimental to std almost seamless

Arrays of pointer conversion fixes
inherited constructors fixes to some corner cases (see P0136R0 for examples of behavior changes)
aggregate initialization with inheritance.
`std::launder`, type punning, etc

Library additions:

### Data types


`std::variant<Ts...>`

Almost-always non-empty last I checked?
Tagged union type
{awesome|useful}

`std::optional`

Maybe holds one of something
Ridiculously useful

`std::any`

Holds one of anything (that is copyable)

`std::string_view`

`std::string` like reference-to-character-array or substring
Never take a `string const&` again.  Also can make parsing a bajillion times faster.
`"hello world"sv`
constexpr `char_traits`

`std::byte` off more than they could chew.

Neither an integer nor a character, just data



### Invoke stuff


`std::invoke`

Call any callable (function pointer, function, member pointer) with one syntax.  From the standard INVOKE concept.

`std::apply`

Takes a function-like and a tuple, and unpacks the tuple into the call.

`std::make_from_tuple`, `std::apply` applied to object construction
`is_invocable`, `is_invocable_r`, `invoke_result`

http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0077r2.html
http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0604r0.html
Deprecates `result_of`
`is_invocable<Foo(Args...), R>` is "can you call `Foo` with `Args...` and get something compatible with ``R", where `R=void` is default.
`invoke_result<Foo, Args...>` is `std::result_of_t<Foo(Args...)>` but apparently less confusing?



### File System TS v1


`[class.path]`
`[class.filesystem.error]`
`[class.file_status]`
`[class.directory_entry]`
`[class.directory_iterator]` and `[class.recursive_directory_iterator]`
`[fs.ops.funcs]`
`fstream`s can be opened with `path`s, as well as with `const path::value_type*` strings.


### New algorithms


`for_each_n`
`reduce`
`transform_reduce`
`exclusive_scan`
`inclusive_scan`
`transform_exclusive_scan`
`transform_inclusive_scan`
Added for threading purposes, exposed even if you aren't using them threaded


### Threading


`std::shared_mutex`

Untimed, which can be more efficient if you don't need it.

`atomic<T>``::is_always_lockfree`
`scoped_lock<Mutexes...>`

Saves some `std::lock` pain when locking more than one mutex at a time.

Parallelism TS v1

The linked paper from 2014, may be out of date
Parallel versions of `std` algorithms, and related machinery

hardware_*_interference_size


### (parts of) Library Fundamentals TS v1 not covered above or below


`[func.searchers]` and `[alg.search]`

A searching algorithm and techniques

`[pmr]`

Polymorphic allocator, like `std::function` for allocators
And some standard memory resources to go with it.
http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0358r1.html

`std::sample`, sampling from a range?


### Container Improvements


`try_emplace` and `insert_or_assign`

gives better guarantees in some cases where spurious move/copy would be bad

Splicing for `map<>`, `unordered_map<>`, `set<>`, and `unordered_set<>`

Move nodes between containers cheaply.
Merge whole containers cheaply.

non-const `.data()` for string.
non-member `std::size`, `std::empty`, `std::data`

like `std::begin`/`end`

Minimal incomplete type support in containers
Contiguous iterator "concept"
`constexpr` iterators
The `emplace` family of functions now returns a reference to the created object.


### Smart pointer changes


`unique_ptr<T[]>` fixes and other `unique_ptr` tweaks.
`weak_from_this` and some fixed to shared from this


### Other `std` datatype improvements:


`{}` construction of `std::tuple` and other improvements
TriviallyCopyable reference_wrapper, can be performance boost


### Misc


C++17 library is based on C11 instead of C99
Reserved `std[0-9]+` for future standard libraries
`destroy(_at|_n)`, `uninitialized_move(_n)`, `uninitialized_value_construct(_n)`, `uninitialized_default_construct(_n)`

utility code already in most `std` implementations exposed

Special math functions

scientists may like them

`std::clamp()`

`std::clamp( a, b, c ) == std::max( b, std::min( a, c ) )` roughly

`gcd` and `lcm`
`std::uncaught_exceptions`

Required if you want to only throw if safe from destructors

`std::as_const`
`std::bool_constant`
A whole bunch of `_v` template variables
`std::void_t<T>`

Surprisingly useful when writing templates

`std::owner_less<void>`

like `std::less<void>`, but for smart pointers to sort based on contents

`std::chrono` polish
`std::conjunction`, `std::disjunction`, `std::negation` exposed
`std::not_fn`

http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0358r1.html

Rules for noexcept within `std`
std::is_contiguous_layout, useful for efficient hashing
std::to_chars/std::from_chars, high performance, locale agnostic number conversion; finally a way to serialize/deserialize to human readable formats (JSON & co) 
std::default_order, indirection over `std::less`. (breaks ABI of some compilers due to name mangling, removed.)


### Traits


swap
is_aggregate
has_unique_object_representations


### Deprecated


Some C libraries, 
`<codecvt>`
`memory_order_consume`
`result_of`, replaced with `invoke_result`
`shared_ptr::unique`, it isn't very threadsafe

Isocpp.org has has an independent list of changes since C++14; it has been partly pillaged.
Naturally TS work continues in parallel, so there are some TS that are not-quite-ripe that will have to wait for the next iteration.  The target for the next iteration is C++20 as previously planned, not C++19 as some rumors implied.  C++1O has been avoided.
Initial list taken from this reddit post and this reddit post, with links added via googling or from the above isocpp.org page.
Additional entries pillaged from SD-6 feature-test list.
clang's feature list and library feature list are next to be pillaged.  This doesn't seem to be reliable, as it is C++1z, not C++17.
these slides had some features missing elsewhere.
While "what was removed" was not asked, here is a short list of a few things ((mostly?) previous deprecated) that are removed in C++17 from C++:
Removed:

`register`, keyword reserved for future use
`bool b; ++b;`
trigraphs

if you still need them, they are now part of your source file encoding, not part of language

ios aliases
auto_ptr, old `<functional>` stuff, `random_shuffle`
allocators in `std::function`

There were rewordings.  I am unsure if these have any impact on code, or if they are just cleanups in the standard:
Papers not yet integrated into above:

P0505R0 (constexpr chrono)
P0418R2 (atomic tweaks)
P0512R0 (template argument deduction tweaks)
P0490R0 (structured binding tweaks)
P0513R0 (changes to `std::hash`)
P0502R0 (parallel exceptions)
P0509R1 (updating restrictions on exception handling)
P0012R1 (make exception specifications be part of the type system)
P0510R0 (restrictions on variants)
P0504R0 (tags for optional/variant/any)
P0497R0 (shared ptr tweaks)
P0508R0 (structured bindings node handles)
P0521R0 (shared pointer use count and unique changes?)

Spec changes:

exception specs and throw expressions

Further reference:

papers grouped by year; not all accepted
https://isocpp.org/files/papers/p0636r0.html

Should be updated to "Modifications to existing features" here.

## [Difference between private, public, and protected inheritance](https://stackoverflow.com/questions/860339/difference-between-private-public-and-protected-inheritance)

**787 Votes**, 
        user106599
        



To answer that question, I'd like to describe member's accessors first in my own words. If you already know this, skip to the heading "next:".
There are three accessors that I'm aware of: `public`, `protected` and `private`. 
Let:

```python
class Base {
    public:
        int publicMember;
    protected:
        int protectedMember;
    private:
        int privateMember;
};
```


Everything that is aware of `Base` is also aware that `Base` contains `publicMember`.
Only the children (and their children) are aware that `Base` contains `protectedMember`.
No one but `Base` is aware of `privateMember`.

By "is aware of", I mean "acknowledge the existence of, and thus be able to access".

### next:

The same happens with public, private and protected inheritance. Let's consider a class `Base` and a class `Child` that inherits from `Base`.

If the inheritance is `public`, everything that is aware of `Base` and `Child` is also aware that `Child` inherits from `Base`.
If the inheritance is `protected`, only `Child`, and its children, are aware that they inherit from `Base`.
If the inheritance is `private`, no one other than `Child` is aware of the inheritance.

## [What are the rules about using an underscore in a C++ identifier?](https://stackoverflow.com/questions/228783/what-are-the-rules-about-using-an-underscore-in-a-c-identifier)

**784 Votes**, Roger Lipscombe

The rules (which did not change in C++11):

Reserved in any scope, including for use as implementation macros:


identifiers beginning with an underscore followed immediately by an uppercase letter
identifiers containing adjacent underscores (or "double underscore")

Reserved in the global namespace:


identifiers beginning with an underscore

Also, everything in the `std` namespace is reserved. (You are allowed to add template specializations, though.) 

From the 2003 C++ Standard:

17.4.3.1.2 Global names [lib.global.names]
Certain sets of names and function signatures are always reserved to the implementation:

Each name that contains a double underscore (`__`) or begins with an underscore followed by an uppercase letter (2.11) is reserved to the implementation for any use.
Each name that begins with an underscore is reserved to the implementation for use as a name in the global namespace.165

165) Such names are also reserved in namespace `::std` (17.4.3.1). 

Because C++ is based on the C standard (1.1/2, C++03) and C99 is a normative reference (1.2/1, C++03) these also apply, from the 1999 C Standard:

7.1.3 Reserved identifiers
Each header declares or defines all identifiers listed in its associated subclause, and
  optionally declares or defines identifiers listed in its associated future library directions subclause and identifiers which are always reserved either for any use or for use as file scope identifiers.

All identifiers that begin with an underscore and either an uppercase letter or another
  underscore are always reserved for any use.
All identifiers that begin with an underscore are always reserved for use as identifiers
  with file scope in both the ordinary and tag name spaces.
Each macro name in any of the following subclauses (including the future library
  directions) is reserved for use as specified if any of its associated headers is included;
  unless explicitly stated otherwise (see 7.1.4).
All identifiers with external linkage in any of the following subclauses (including the
  future library directions) are always reserved for use as identifiers with external
  linkage.154
Each identifier with file scope listed in any of the following subclauses (including the
  future library directions) is reserved for use as a macro name and as an identifier with
  file scope in the same name space if any of its associated headers is included.

No other identifiers are reserved. If the program declares or defines an identifier in a
  context in which it is reserved (other than as allowed by 7.1.4), or defines a reserved
  identifier as a macro name, the behavior is undefined.
If the program removes (with `#undef`) any macro definition of an identifier in the first
  group listed above, the behavior is undefined.
154) The list of reserved identifiers with external linkage includes `errno`, `math_errhandling`, `setjmp`, and `va_end`.

Other restrictions might apply. For example, the POSIX standard reserves a lot of identifiers that are likely to show up in normal code:

Names beginning with a capital ``E followed a digit or uppercase letter:


may be used for additional error code names.

Names that begin with either `is` or `to` followed by a lowercase letter


may be used for additional character testing and conversion functions.

Names that begin with `LC_` followed by an uppercase letter


may be used for additional macros specifying locale attributes.

Names of all existing mathematics functions suffixed with ``f or ``l are reserved


for corresponding functions that operate on float and long double arguments, respectively.

Names that begin with `SIG` followed by an uppercase letter are reserved


for additional signal names.

Names that begin with `SIG_` followed by an uppercase letter are reserved


for additional signal actions.

Names beginning with `str`, `mem`, or `wcs` followed by a lowercase letter are reserved


for additional string and array functions.

Names beginning with `PRI` or `SCN` followed by any lowercase letter or ``X are reserved


for additional format specifier macros

Names that end with `_t` are reserved


for additional type names.


While using these names for your own purposes right now might not cause a problem, they do raise the possibility of conflict with future versions of that standard.

Personally I just don't start identifiers with underscores. New addition to my rule: Don't use double underscores anywhere, which is easy as I rarely use underscore.
After doing research on this article I no longer end my identifiers with `_t`
as this is reserved by the POSIX standard.
The rule about any identifier ending with `_t` surprised me a lot. I think that is a POSIX standard (not sure yet) looking for clarification and official chapter and verse. This is from the GNU libtool manual, listing reserved names.
CesarB provided the following link to the POSIX 2004 reserved symbols and notes 'that many other reserved prefixes and suffixes ... can be found there'.  The
POSIX 2008 reserved symbols are defined here.  The restrictions are somewhat more nuanced than those above.

## [Why can't variables be declared in a switch statement?](https://stackoverflow.com/questions/92396/why-cant-variables-be-declared-in-a-switch-statement)

**766 Votes**, Rob

`Case` statements are only labels. This means the compiler will interpret this as a jump directly to the label. In C++, the problem here is one of scope. Your curly brackets define the scope as everything inside the `switch` statement. This means that you are left with a scope where a jump will be performed further into the code skipping the initialization. The correct way to handle this is to define a scope specific to that `case` statement and define your variable within it. 

```python
switch (val)
{   
case VAL:  
{
  // This will work
  int newVal = 42;  
  break;
}
case ANOTHER_VAL:  
...
break;
}
```

## [How to convert a std::string to const char* or char*?](https://stackoverflow.com/questions/347949/how-to-convert-a-stdstring-to-const-char-or-char)

**764 Votes**, user37875

If you just want to pass a `std::string` to a function that needs `const char*` you can use 

```python
std::string str;
const char * c = str.c_str();
```

If you want to get a writable copy, like `char *`, you can do that with this:

```python
std::string str;
char * writable = new char[str.size() + 1];
std::copy(str.begin(), str.end(), writable);
writable[str.size()] = '\0'; // don't forget the terminating 0

// don't forget to free the string after finished using it
delete[] writable;
```

Edit: Notice that the above is not exception safe. If anything between the `new` call and the `delete` call throws, you will leak memory, as nothing will call `delete` for you automatically. There are two immediate ways to solve this.
boost::scoped_array
`boost::scoped_array` will delete the memory for you upon going out of scope:

```python
std::string str;
boost::scoped_array<char> writable(new char[str.size() + 1]);
std::copy(str.begin(), str.end(), writable.get());
writable[str.size()] = '\0'; // don't forget the terminating 0

// get the char* using writable.get()

// memory is automatically freed if the smart pointer goes 
// out of scope
```

std::vector
This is the standard way (does not require any external library). You use `std::vector`, which completely manages the memory for you.

```python
std::string str;
std::vector<char> writable(str.begin(), str.end());
writable.push_back('\0');

// get the char* using &writable[0] or &*writable.begin()
```

## [What are POD types in C++?](https://stackoverflow.com/questions/146452/what-are-pod-types-in-c)

**745 Votes**, paxos1977

POD stands for Plain Old Data - that is, a class (whether defined with the keyword `struct` or the keyword `class`) without constructors, destructors and virtual members functions. Wikipedia's article on POD goes into a bit more detail and defines it as:

A Plain Old Data Structure in C++ is an aggregate class that contains only PODS as members, has no user-defined destructor, no user-defined copy assignment operator, and no nonstatic members of pointer-to-member type.

Greater detail can be found in this answer for C++98/03. C++11 changed the rules surrounding POD, relaxing them greatly, thus necessitating a follow-up answer here.

## [Why should C++ programmers minimize use of 'new'?](https://stackoverflow.com/questions/6500313/why-should-c-programmers-minimize-use-of-new)

**732 Votes**, bitgarden

There are two widely-used memory allocation techniques: automatic allocation and dynamic allocation.  Commonly, there is a corresponding region of memory for each: the stack and the heap.
Stack
The stack always allocates memory in a sequential fashion.  It can do so because it requires you to release the memory in the reverse order (First-In, Last-Out: FILO).  This is the memory allocation technique for local variables in many programming languages.  It is very, very fast because it requires minimal bookkeeping and the next address to allocate is implicit.
In C++, this is called automatic storage because the storage is claimed automatically at the end of scope.  As soon as execution of current code block (delimited using `{}`) is completed, memory for all variables in that block is automatically collected.  This is also the moment where destructors are invoked to clean up resources.
Heap
The heap allows for a more flexible memory allocation mode.  Bookkeeping is more complex and allocation is slower.  Because there is no implicit release point, you must release the memory manually, using `delete` or `delete[]` (`free` in C).  However, the absence of an implicit release point is the key to the heap's flexibility.
Reasons to use dynamic allocation
Even if using the heap is slower and potentially leads to memory leaks or memory fragmentation, there are perfectly good use cases for dynamic allocation, as it's less limited.
Two key reasons to use dynamic allocation:

You don't know how much memory you need at compile time.  For instance, when reading a text file into a string, you usually don't know what size the file has, so you can't decide how much memory to allocate until you run the program.
You want to allocate memory which will persist after leaving the current block.  For instance, you may want to write a function `string readfile(string path)` that returns the contents of a file.  In this case, even if the stack could hold the entire file contents, you could not return from a function and keep the allocated memory block.

Why dynamic allocation is often unnecessary
In C++ there's a neat construct called a destructor.  This mechanism allows you to manage resources by aligning the lifetime of the resource with the lifetime of a variable. This technique is called RAII and is the distinguishing point of C++. It "wraps" resources into objects.  `std::string` is a perfect example.  This snippet:

```python
int main ( int argc, char* argv[] )
{
    std::string program(argv[0]);
}
```

actually allocates a variable amount of memory.  The `std::string` object allocates memory using the heap and releases it in its destructor.  In this case, you did not need to manually manage any resources and still got the benefits of dynamic memory allocation.
In particular, it implies that in this snippet:

```python
int main ( int argc, char* argv[] )
{
    std::string * program = new std::string(argv[0]);  // Bad!
    delete program;
}
```

there is unneeded dynamic memory allocation.  The program requires more typing (!) and introduces the risk of forgetting to deallocate the memory.  It does this with no apparent benefit.
Why you should use automatic storage as often as possible
Basically, the last paragraph sums it up.  Using automatic storage as often as possible makes your programs:

faster to type;
faster when run;
less prone to memory/resource leaks.

Bonus points
In the referenced question, there are additional concerns.  In particular, the following class:

```python
class Line {
public:
    Line();
    ~Line();
    std::string* mString;
};

Line::Line() {
    mString = new std::string("foo_bar");
}

Line::~Line() {
    delete mString;
}
```

Is actually a lot more risky to use than the following one:

```python
class Line {
public:
    Line();
    std::string mString;
};

Line::Line() {
    mString = "foo_bar";
    // note: there is a cleaner way to write this.
}
```

The reason is that `std::string` properly defines a copy constructor.  Consider the following program:

```python
int main ()
{
    Line l1;
    Line l2 = l1;
}
```

Using the original version, this program will likely crash, as it uses `delete` on the same string twice.  Using the modified version, each `Line` instance will own its own string instance, each with its own memory and both will be released at the end of the program.
Other notes
Extensive use of RAII is considered a best practice in C++ because of all the reasons above.  However, there is an additional benefit which is not immediately obvious.  Basically, it's better than the sum of its parts.  The whole mechanism composes.  It scales.
If you use the `Line` class as a building block:

```python
 class Table
 {
      Line borders[4];
 };
```

Then

```python
 int main ()
 {
     Table table;
 }
```

allocates four `std::string` instances, four `Line` instances, one `Table` instance and all the string's contents and everything is freed automagically.

## [Can I call a constructor from another constructor (do constructor chaining) in C++?](https://stackoverflow.com/questions/308276/can-i-call-a-constructor-from-another-constructor-do-constructor-chaining-in-c)

**732 Votes**, Stormenet

C++11: Yes!
C++11 and onwards has this same feature (called delegating constructors). 
The syntax is slightly different from C#:

```python
class Foo {
public: 
  Foo(char x, int y) {}
  Foo(int y) : Foo('a', y) {}
};
```

C++03: No
Unfortunately, there's no way to do this in C++03, but there are two ways of simulating this:

You can combine two (or more) constructors via default parameters:

```python
class Foo {
public:
  Foo(char x, int y=0);  // combines two constructors (char) and (char, int)
  // ...
};
```

Use an init method to share common code:

```python
class Foo {
public:
  Foo(char x);
  Foo(char x, int y);
  // ...
private:
  void init(char x, int y);
};

Foo::Foo(char x)
{
  init(x, int(x) + 7);
  // ...
}

Foo::Foo(char x, int y)
{
  init(x, y);
  // ...
}

void Foo::init(char x, int y)
{
  // ...
}
```


See the C++FAQ entry for reference.

## [Why is this C++ code faster than my hand-written assembly for testing the Collatz conjecture?](https://stackoverflow.com/questions/40354978/why-is-this-c-code-faster-than-my-hand-written-assembly-for-testing-the-collat)

**725 Votes**, jeffer son

If you think a 64-bit DIV instruction is a good way to divide by two, then no wonder the compiler's asm output beat your hand-written code, even with `-O0` (compile fast, no extra optimization, and store/reload to memory after/before every C statement so a debugger can modify variables).
See Agner Fog's Optimizing Assembly guide to learn how to write efficient asm.  He also has instruction tables and a microarch guide for specific details for specific CPUs.  See also the x86 tag wiki for more perf links.
See also this more general question about beating the compiler with hand-written asm: Is inline assembly language slower than native C++ code?.  TL:DR: yes if you do it wrong (like this question).
Usually you're fine letting the compiler do its thing, especially if you try to write C++ that can compile efficiently.  Also see is assembly faster than compiled languages?.  One of the answers links to these neat slides showing how various C compilers optimize some really simple functions with cool tricks.


```python
even:
    mov rbx, 2
    xor rdx, rdx
    div rbx
```

On Intel Haswell, `div r64` is 36 uops, with a latency of 32-96 cycles, and a throughput of one per 21-74 cycles.  (Plus the 2 uops to set up RBX and zero RDX, but out-of-order execution can run those early).  High-uop-count instructions like DIV are microcoded, which can also cause front-end bottlenecks. In this case, latency is the most relevant factor because it's part of a loop-carried dependency chain.
`shr rax, 1` does the same unsigned division: It's 1 uop, with 1c latency, and can run 2 per clock cycle.
For comparison, 32-bit division is faster, but still horrible vs. shifts. `idiv r32` is 9 uops, 22-29c latency, and one per 8-11c throughput on Haswell.

As you can see from looking at gcc's `-O0` asm output (Godbolt compiler explorer), it only uses shifts instructions. clang `-O0` does compile naively like you thought, even using 64-bit IDIV twice. (When optimizing, compilers do use both outputs of IDIV when the source does a division and modulus with the same operands, if they use IDIV at all)
GCC doesn't have a totally-naive mode; it always transforms through GIMPLE, which means some "optimizations" can't be disabled.  This includes recognizing division-by-constant and using shifts (power of 2) or a fixed-point multiplicative inverse (non power of 2) to avoid IDIV (see `div_by_13` in the above godbolt link).
`gcc -Os` (optimize for size) does use IDIV for non-power-of-2 division,
unfortunately even in cases where the multiplicative inverse code is only slightly larger but much slower.

Helping the compiler
(summary for this case: use `uint64_t n`)
First of all, it's only interesting to look at optimized compiler output.  (`-O3`).  `-O0` speed is basically meaningless.
Look at your asm output (on Godbolt, or see How to remove "noise" from GCC/clang assembly output?).  When the compiler doesn't make optimal code in the first place: Writing your C/C++ source in a way that guides the compiler into making better code is usually the best approach.  You have to know asm, and know what's efficient, but you apply this knowledge indirectly.  Compilers are also a good source of ideas: sometimes clang will do something cool, and you can hand-hold gcc into doing the same thing: see this answer and what I did with the non-unrolled loop in @Veedrac's code below.)
This approach is portable, and in 20 years some future compiler can compile it to whatever is efficient on future hardware (x86 or not), maybe using new ISA extension or auto-vectorizing.  Hand-written x86-64 asm from 15 years ago would usually not be optimally tuned for Skylake.  e.g. compare&branch macro-fusion didn't exist back then.  What's optimal now for hand-crafted asm for one microarchitecture might not be optimal for other current and future CPUs. Comments on @johnfound's answer discuss major differences between AMD Bulldozer and Intel Haswell, which have a big effect on this code.  But in theory, `g++ -O3 -march=bdver3` and `g++ -O3 -march=skylake` will do the right thing.  (Or `-march=native`.)   Or `-mtune=...` to just tune, without using instructions that other CPUs might not support.
My feeling is that guiding the compiler to asm that's good for a current CPU you care about shouldn't be a problem for future compilers.  They're hopefully better than current compilers at finding ways to transform code, and can find a way that works for future CPUs.  Regardless, future x86 probably won't be terrible at anything that's good on current x86, and the future compiler will avoid any asm-specific pitfalls while implementing something like the data movement from your C source, if it doesn't see something better.
Hand-written asm is a black-box for the optimizer, so constant-propagation doesn't work when inlining makes an input a compile-time constant.  Other optimizations are also affected.  Read https://gcc.gnu.org/wiki/DontUseInlineAsm before using asm.  (And avoid MSVC-style inline asm: inputs/outputs have to go through memory which adds overhead.)
In this case: your ``n has a signed type, and gcc uses the SAR/SHR/ADD sequence that gives the correct rounding.  (IDIV and arithmetic-shift "round" differently for negative inputs, see the SAR insn set ref manual entry).  (IDK if gcc tried and failed to prove that ``n can't be negative, or what.  Signed-overflow is undefined behaviour, so it should have been able to.)
You should have used `uint64_t n`, so it can just SHR.  And so it's portable to systems where `long` is only 32-bit (e.g. x86-64 Windows).

BTW, gcc's optimized asm output looks pretty good (using `unsigned long n`): the inner loop it inlines into `main()` does this:

```python
 # from gcc5.4 -O3  plus my comments

 # edx= count=1
 # rax= uint64_t n

.L9:                   # do{
    lea    rcx, [rax+1+rax*2]   # rcx = 3*n + 1
    mov    rdi, rax
    shr    rdi         # rdi = n>>1;
    test   al, 1       # set flags based on n%2 (aka n&1)
    mov    rax, rcx
    cmove  rax, rdi    # n= (n%2) ? 3*n+1 : n/2;
    add    edx, 1      # ++count;
    cmp    rax, 1
    jne   .L9          #}while(n!=1)

  cmp/branch to update max and maxi, and then do the next n
```

The inner loop is branchless, and the critical path of the loop-carried dependency chain is:

3-component LEA (3 cycles)
cmov (2 cycles on Haswell, 1c on Broadwell or later).

Total: 5 cycle per iteration, latency bottleneck.  Out-of-order execution takes care of everything else in parallel with this (in theory: I haven't tested with perf counters to see if it really runs at 5c/iter).
The FLAGS input of `cmov` (produced by TEST) is faster to produce than the RAX input (from LEA->MOV), so it's not on the critical path.
Similarly, the MOV->SHR that produces CMOV's RDI input is off the critical path, because it's also faster than the LEA.  MOV on IvyBridge and later has zero latency (handled at register-rename time).  (It still takes a uop, and a slot in the pipeline, so it's not free, just zero latency).  The extra MOV in the LEA dep chain is part of the bottleneck on other CPUs.
The cmp/jne is also not part of the critical path: it's not loop-carried, because control dependencies are handled with branch prediction + speculative execution, unlike data dependencies on the critical path.

Beating the compiler
GCC did a pretty good job here.  It could save one code byte by using `inc edx` instead of `add edx, 1`, because nobody cares about P4 and its false-dependencies for partial-flag-modifying instructions.
It could also save all the MOV instructions, and the TEST:  SHR sets CF= the bit shifted out, so we can use `cmovc` instead of `test` / `cmovz`.

```python
 ### Hand-optimized version of what gcc does
.L9:                       #do{
    lea     rcx, [rax+1+rax*2] # rcx = 3*n + 1
    shr     rax, 1         # n>>=1;    CF = n&1 = n%2
    cmovc   rax, rcx       # n= (n&1) ? 3*n+1 : n/2;
    inc     edx            # ++count;
    cmp     rax, 1
    jne     .L9            #}while(n!=1)
```

See @johnfound's answer for another clever trick: remove the CMP by branching on SHR's flag result as well as using it for CMOV:  zero only if n was 1 (or 0) to start with.  (Fun fact: SHR with count != 1 on Nehalem or earlier causes a stall if you read the flag results.  That's how they made it single-uop.  The shift-by-1 special encoding is fine, though.)
Avoiding MOV doesn't help with the latency at all on Haswell (Can x86's MOV really be "free"? Why can't I reproduce this at all?).  It does help significantly on CPUs like Intel pre-IvB, and AMD Bulldozer-family, where MOV is not zero-latency.  The compiler's wasted MOV instructions do affect the critical path.  BD's complex-LEA and CMOV are both lower latency (2c and 1c respectively), so it's a bigger fraction of the latency.  Also, throughput bottlenecks become an issue, because it only has two integer ALU pipes.  See @johnfound's answer, where he has timing results from an AMD CPU.
Even on Haswell, this version may help a bit by avoiding some occasional delays where a non-critical uop steals an execution port from one on the critical path, delaying execution by 1 cycle.  (This is called a resource conflict).  It also saves a register, which may help when doing multiple ``n values in parallel in an interleaved loop (see below).
LEA's latency depends on the addressing mode, on Intel SnB-family CPUs.  3c for 3 components (`[base+idx+const]`, which takes two separate adds), but only 1c with 2 or fewer components (one add).  Some CPUs (like Core2) do even a 3-component LEA in a single cycle, but SnB-family doesn't.  Worse, Intel SnB-family standardizes latencies so there are no 2c uops, otherwise 3-component LEA would be only 2c like Bulldozer.  (3-component LEA is slower on AMD as well, just not by as much).
So `lea  rcx, [rax + rax*2]` / `inc rcx` is only 2c latency, faster than `lea  rcx, [rax + rax*2 + 1]`, on Intel SnB-family CPUs like Haswell.  Break-even on BD, and worse on Core2.  It does cost an extra uop, which normally isn't worth it to save 1c latency, but latency is the major bottleneck here and Haswell has a wide enough pipeline to handle the extra uop throughput.
Neither gcc, icc, nor clang (on godbolt) used SHR's CF output, always using an AND or TEST.  Silly compilers. :P  They're great pieces of complex machinery, but a clever human can often beat them on small-scale problems.  (Given thousands to millions of times longer to think about it, of course!  Compilers don't use exhaustive algorithms to search for every possible way to do things, because that would take too long when optimizing a lot of inlined code, which is what they do best.  They also don't model of the pipeline in the target microarchitecture; they just use some heuristics.)

Simple loop unrolling won't help; this loop bottlenecks on the latency of a loop-carried dependency chain, not on loop overhead / throughput.  This means it would do well with hyperthreading (or any other kind of SMT), since the CPU has lots of time to interleave instructions from two threads.  This would mean parallelizing the loop in `main`, but that's fine because each thread can just check a range of ``n values and produce a pair of integers as a result.
Interleaving by hand within a single thread might be viable, too.  Maybe compute the sequence for a pair of numbers in parallel, since each one only takes a couple registers, and they can all update the same `max` / `maxi`.  This creates more instruction-level parallelism.
The trick is deciding whether to wait until all the ``n values have reached ``1 before getting another pair of starting ``n values, or whether to break out and get a new start point for just one that reached the end condition, without touching the registers for the other sequence.  Probably it's best to keep each chain working on useful data, otherwise you'd have to conditionally increment its counter.

You could maybe even do this with SSE packed-compare stuff to conditionally increment the counter for vector elements where ``n hadn't reached ``1 yet.  And then to hide the even longer latency of a SIMD conditional-increment implementation, you'd need to keep more vectors of ``n values up in the air.  Maybe only worth with 256b vector (4x `uint64_t`).
I think the best strategy to make detection of a ``1 "sticky" is to mask the vector of all-ones that you add to increment the counter.  So after you've seen a ``1 in an element, the increment-vector will have a zero, and +=0 is a no-op.
Untested idea for manual vectorization

```python
# starting with YMM0 = [ n_d, n_c, n_b, n_a ]  (64-bit elements)
# ymm4 = _mm256_set1_epi64x(1):  increment vector
# ymm5 = all-zeros:  count vector

.inner_loop:
    vpaddq    ymm1, ymm0, xmm0
    vpaddq    ymm1, ymm1, xmm0
    vpaddq    ymm1, ymm1, set1_epi64(1)     # ymm1= 3*n + 1.  Maybe could do this more efficiently?

    vprllq    ymm3, ymm0, 63                # shift bit 1 to the sign bit

    vpsrlq    ymm0, ymm0, 1                 # n /= 2

    # There may be a better way to do this blend, avoiding the bypass delay for an FP blend between integer insns, not sure.  Probably worth it
    vpblendvpd ymm0, ymm0, ymm1, ymm3       # variable blend controlled by the sign bit of each 64-bit element.  I might have the source operands backwards, I always have to look this up.

    # ymm0 = updated n  in each element.

    vpcmpeqq ymm1, ymm0, set1_epi64(1)
    vpandn   ymm4, ymm1, ymm4         # zero out elements of ymm4 where the compare was true

    vpaddq   ymm5, ymm5, ymm4         # count++ in elements where n has never been == 1

    vptest   ymm4, ymm4
    jnz  .inner_loop
    # Fall through when all the n values have reached 1 at some point, and our increment vector is all-zero

    vextracti128 ymm0, ymm5, 1
    vpmaxq .... crap this doesn't exist
    # Actually just delay doing a horizontal max until the very very end.  But you need some way to record max and maxi.
```

You can and should implement this with intrinsics, instead of hand-written asm.


### Algorithmic / implementation improvement:

Besides just implementing the same logic with more efficient asm, look for ways to simplify the logic, or avoid redundant work.  e.g. memoize to detect common endings to sequences.  Or even better, look at 8 trailing bits at once (gnasher's answer)
@EOF points out that `tzcnt` (or `bsf`) could be used to do multiple `n/=2` iterations in one step.  That's probably better than SIMD vectorizing, because no SSE or AVX instruction can do that.  It's still compatible with doing multiple scalar ``ns in parallel in different integer registers, though.
So the loop might look like this:

```python
goto loop_entry;  // C++ structured like the asm, for illustration only
do {
   n = n*3 + 1;
  loop_entry:
   shift = _tzcnt_u64(n);
   n >>= shift;
   count += shift;
} while(n != 1);
```

This may do significantly fewer iterations, but variable-count shifts are slow on Intel SnB-family CPUs without BMI2.  3 uops, 2c latency.  (They have an input dependency on the FLAGS because count=0 means the flags are unmodified.  They handle this as a data dependency, and take multiple uops because a uop can only have 2 inputs (pre-HSW/BDW anyway)).  This is the kind that people complaining about x86's crazy-CISC design are referring to.  It makes x86 CPUs slower than they would be if the ISA was designed from scratch today, even in a mostly-similar way.  (i.e. this is part of the "x86 tax" that costs speed / power.)  SHRX/SHLX/SARX (BMI2) are a big win (1 uop / 1c latency).
It also puts tzcnt (3c on Haswell and later) on the critical path, so it significantly lengthens the total latency of the loop-carried dependency chain.  It does remove any need for a CMOV, or for preparing a register holding `n>>1`, though.  @Veedrac's answer overcomes all this by deferring the tzcnt/shift for multiple iterations, which is highly effective (see below).
We can safely use BSF or TZCNT interchangeably, because ``n can never be zero at that point.  TZCNT's machine-code decodes as BSF on CPUs that don't support BMI1.  (Meaningless prefixes are ignored, so REP BSF runs as BSF).
TZCNT performs much better than BSF on AMD CPUs that support it,  so it can be a good idea to use `REP BSF`, even if you don't care about setting ZF if the input is zero rather than the output.  Some compilers do this when you use `__builtin_ctzll` even with `-mno-bmi`.  
They perform the same on Intel CPUs, so just save the byte if that's all that matters.  TZCNT on Intel (pre-Skylake) still has a false-dependency on the supposedly write-only output operand, just like BSF, to support the undocumented behaviour that BSF with input = 0 leaves its destination unmodified.  So you need to work around that unless optimizing only for Skylake, so there's nothing to gain from the extra REP byte.  (Intel often goes above and beyond what the x86 ISA manual requires, to avoid breaking widely-used code that depends on something it shouldn't, or that is retroactively disallowed.  e.g. Windows 9x's assumes no speculative prefetching of TLB entries, which was safe when the code was written, before Intel updated the TLB management rules.)
Anyway, LZCNT/TZCNT on Haswell have the same false dep as POPCNT: see this Q&A.  This is why in gcc's asm output for @Veedrac's code, you see it breaking the dep chain with xor-zeroing on the register it's about to use as TZCNT's destination, when it doesn't use dst=src.  Since TZCNT/LZCNT/POPCNT never leave their destination undefined or unmodified, this false dependency on the output on Intel CPUs is purely a performance bug / limitation.  Presumably it's worth some transistors / power to have them behave like other uops that go to the same execution unit.  The only software-visible upside is in the interaction with another microarchitectural limitation: they can micro-fuse a memory operand with an indexed addressing mode on Haswell, but on Skylake where Intel removed the false dependency for LZCNT/TZCNT they "un-laminate" indexed addressing modes while POPCNT can still micro-fuse any addr mode.

Improvements to ideas / code from other answers:
@hidefromkgb's answer has a nice observation that you're guaranteed to be able to do one right shift after a 3n+1.  You can compute this more even more efficiently than just leaving out the checks between steps.  The asm implementation in that answer is broken, though (it depends on OF, which is undefined after SHRD with a count > 1), and slow: `ROR rdi,2` is faster than `SHRD rdi,rdi,2`, and using two CMOV instructions on the critical path is slower than an extra TEST that can run in parallel.
I put tidied / improved C (which guides the compiler to produce better asm), and tested+working faster asm (in comments below the C) up on Godbolt: see the link in @hidefromkgb's answer.  (This answer hit the 30k char limit from the large Godbolt URLs, but shortlinks can rot and were too long for goo.gl anyway.)
Also improved the output-printing to convert to a string and make one `write()` instead of writing one char at a time. This minimizes impact on timing the whole program with `perf stat ./collatz` (to record performance counters), and I de-obfuscated some of the non-critical asm.

@Veedrac's code
I got a very small speedup from right-shifting as much as we know needs doing, and checking to continue the loop.  From 7.5s for limit=1e8 down to 7.275s, on Core2Duo (Merom), with an unroll factor of 16.
code + comments on Godbolt.  Don't use this version with clang; it does something silly with the defer-loop.  Using a tmp counter ``k and then adding it to `count` later changes what clang does, but that slightly hurts gcc.
See discussion in comments: Veedrac's code is excellent on CPUs with BMI1 (i.e. not Celeron/Pentium)

## [How do you declare an interface in C++?](https://stackoverflow.com/questions/318064/how-do-you-declare-an-interface-in-c)

**714 Votes**, Aaron Fischer

To expand on the answer by bradtgmurray,  you may want to make one exception to the pure virtual method list of your interface by adding a virtual destructor. This allows you to pass pointer ownership to another party without exposing the concrete derived class. The destructor doesn't have to do anything, because the interface doesn't have any concrete members. It might seem contradictory to define a function as both virtual and inline, but trust me - it isn't.

```python
class IDemo
{
    public:
        virtual ~IDemo() {}
        virtual void OverrideMe() = 0;
};

class Parent
{
    public:
        virtual ~Parent();
};

class Child : public Parent, public IDemo
{
    public:
        virtual void OverrideMe()
        {
            //do stuff
        }
};
```

You don't have to include a body for the virtual destructor - it turns out some compilers have trouble optimizing an empty destructor and you're better off using the default.
