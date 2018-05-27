# StackOverflow Top Javascript Questions


## [How do I redirect to another webpage?](https://stackoverflow.com/questions/503093/how-do-i-redirect-to-another-webpage)

**7740 Votes**, venkatachalam

### One does not simply redirect using jQuery

jQuery is not necessary, and `window.location.replace(...)` will best simulate an HTTP redirect.  
`window.location.replace(...)` is better than using `window.location.href`, because `replace()` does not keep the originating page in the session history, meaning the user won't get stuck in a never-ending back-button fiasco.

If you want to simulate someone clicking on a link, use
  `location.href`
If you want to simulate an HTTP redirect, use `location.replace`

For example:

```javascript
// similar behavior as an HTTP redirect
window.location.replace("http://stackoverflow.com");

// similar behavior as clicking on a link
window.location.href = "http://stackoverflow.com";
```

## [How do JavaScript closures work?](https://stackoverflow.com/questions/111102/how-do-javascript-closures-work)

**7654 Votes**, community-wiki

JavaScript closures for beginners
Submitted by Morris on Tue, 2006-02-21 10:19.  Community-edited since.

### Closures are not magic

This page explains closures so that a programmer can understand them  using working JavaScript code. It is not for gurus or functional programmers.
Closures are not hard to understand once the core concept is grokked. However, they are impossible to understand by reading any academic papers or academically oriented information about them!
This article is intended for programmers with some programming experience in a mainstream language, and who can read the following JavaScript function:



```javascript
function sayHello(name) {
  var text = 'Hello ' + name;
  var say = function() { console.log(text); }
  say();
}
sayHello('Joe');```





### An example of a closure

Two one sentence summaries:

A closure is one way of supporting first-class functions; it is an expression that can reference variables within its scope (when it was first declared), be assigned to a variable, be passed as an argument to a function, or be returned as a function result. 
Or, a closure is a stack frame which is allocated when a function starts its execution, and not freed after the function returns (as if a 'stack frame' were allocated on the heap rather than the stack!).

The following code returns a reference to a function:



```javascript
function sayHello2(name) {
  var text = 'Hello ' + name; // Local variable
  var say = function() { console.log(text); }
  return say;
}
var say2 = sayHello2('Bob');
say2(); // logs "Hello Bob"```




Most JavaScript programmers will understand how a reference to a function is returned to a variable (`say2`) in the above code. If you don't, then you need to look at that before you can learn closures. A programmer using C would think of the function as returning a pointer to a function, and that the variables `say` and `say2` were each a pointer to a function.
There is a critical difference between a C pointer to a function and a JavaScript reference to a function. In JavaScript, you can think of a function reference variable as having both a pointer to a function as well as a hidden pointer to a closure.
The above code has a closure because the anonymous function `function() { console.log(text); }` is declared inside another function, `sayHello2()` in this example. In JavaScript, if you use the `function` keyword inside another function, you are creating a closure.
In C and most other common languages, after a function returns, all the local variables are no longer accessible because the stack-frame is destroyed.
In JavaScript, if you declare a function within another function, then the local variables can remain accessible after returning from the function you called. This is demonstrated above, because we call the function `say2()` after we have returned from `sayHello2()`. Notice that the code that we call references the variable `text`, which was a local variable of the function `sayHello2()`.

```javascript
function() { console.log(text); } // Output of say2.toString();
```

Looking at the output of `say2.toString()`, we can see that the code refers to the variable `text`. The anonymous function can reference `text` which holds the value `'Hello Bob'` because the local variables of `sayHello2()` are kept in a closure.
The magic is that in JavaScript a function reference also has a secret reference to the closure it was created in  similar to how delegates are a method pointer plus a secret reference to an object.

### More examples

For some reason, closures seem really hard to understand when you read about them, but when you see some examples it becomes clear how they work (it took me a while).
I recommend working through the examples carefully until you understand how they work. If you start using closures without fully understanding how they work, you would soon create some very weird bugs!
Example 3
This example shows that the local variables are not copied  they are kept by reference. It is kind of like keeping a stack-frame in memory when the outer function exits!



```javascript
function say667() {
  // Local variable that ends up within closure
  var num = 42;
  var say = function() { console.log(num); }
  num++;
  return say;
}
var sayNumber = say667();
sayNumber(); // logs 43```




Example 4
All three global functions have a common reference to the same closure because they are all declared within a single call to `setupSomeGlobals()`.



```javascript
var gLogNumber, gIncreaseNumber, gSetNumber;
function setupSomeGlobals() {
  // Local variable that ends up within closure
  var num = 42;
  // Store some references to functions as global variables
  gLogNumber = function() { console.log(num); }
  gIncreaseNumber = function() { num++; }
  gSetNumber = function(x) { num = x; }
}

setupSomeGlobals();
gIncreaseNumber();
gLogNumber(); // 43
gSetNumber(5);
gLogNumber(); // 5

var oldLog = gLogNumber;

setupSomeGlobals();
gLogNumber(); // 42

oldLog() // 5```




The three functions have shared access to the same closure  the local variables of `setupSomeGlobals()` when the three functions were defined.
Note that in the above example, if you call `setupSomeGlobals()` again, then a new closure (stack-frame!) is created. The old `gLogNumber`, `gIncreaseNumber`, `gSetNumber` variables are overwritten with new functions that have the new closure. (In JavaScript, whenever you declare a function inside another function, the inside function(s) is/are recreated again each time the outside function is called.)
Example 5
This example shows that the closure contains any local variables that were declared inside the outer function before it exited. Note that the variable `alice` is actually declared after the anonymous function. The anonymous function is declared first; and when that function is called it can access the `alice` variable because `alice` is in the same scope (JavaScript does variable hoisting).
Also `sayAlice()()` just directly calls the function reference returned from `sayAlice()`  it is exactly the same as what was done previously but without the temporary variable.



```javascript
function sayAlice() {
    var say = function() { console.log(alice); }
    // Local variable that ends up within closure
    var alice = 'Hello Alice';
    return say;
}
sayAlice()();// logs "Hello Alice"```




Tricky: note also that the `say` variable is also inside the closure, and could be accessed by any other function that might be declared within `sayAlice()`, or it could be accessed recursively within the inside function.
Example 6
This one is a real gotcha for many people, so you need to understand it. Be very careful if you are defining a function within a loop: the local variables from the closure may not act as you might first think. 
You need to understand the "variable hoisting" feature in Javascript in order to understand this example.



```javascript
function buildList(list) {
    var result = [];
    for (var i = 0; i < list.length; i++) {
        var item = 'item' + i;
        result.push( function() {console.log(item + ' ' + list[i])} );
    }
    return result;
}

function testList() {
    var fnlist = buildList([1,2,3]);
    // Using j only to help prevent confusion -- could use i.
    for (var j = 0; j < fnlist.length; j++) {
        fnlist[j]();
    }
}

 testList() //logs "item2 undefined" 3 times```




The line `result.push( function() {console.log(item + ' ' + list[i])}` adds a reference to an anonymous function three times to the result array. If you are not so familiar with anonymous functions think of it like:

```javascript
pointer = function() {console.log(item + ' ' + list[i])};
result.push(pointer);
```

Note that when you run the example, `"item2 undefined"` is logged three times! This is because just like previous examples, there is only one closure for the local variables for `buildList` (which are `result`, ``i and `item`). When the anonymous functions are called on the line `fnlist[j]()`; they all use the same single closure, and they use the current value for ``i and `item` within that one closure (where ``i has a value of ``3 because the loop had completed, and `item` has a value of `'item2'`). Note we are indexing from 0 hence `item` has a value of `item2`. And the i++ will increment ``i to the value ``3.
It may be helpful to see what happens when a block-level declaration of the variable `item` is used (via the `let` keyword) instead of a function-scoped variable declaration via the `var` keyword. If that change is made, then each anonymous function in the array `result` has its own closure; when the example is run the output is as follows:

```javascript
item0 undefined
item1 undefined
item2 undefined
```

If the variable ``i is also defined using `let` instead of `var`, then the output is:

```javascript
item0 1
item1 2
item2 3
```

Example 7
In this final example, each call to the main function creates a separate closure.



```javascript
function newClosure(someNum, someRef) {
    // Local variables that end up within closure
    var num = someNum;
    var anArray = [1,2,3];
    var ref = someRef;
    return function(x) {
        num += x;
        anArray.push(num);
        console.log('num: ' + num +
            '; anArray: ' + anArray.toString() +
            '; ref.someVar: ' + ref.someVar + ';');
      }
}
obj = {someVar: 4};
fn1 = newClosure(4, obj);
fn2 = newClosure(5, obj);
fn1(1); // num: 5; anArray: 1,2,3,5; ref.someVar: 4;
fn2(1); // num: 6; anArray: 1,2,3,6; ref.someVar: 4;
obj.someVar++;
fn1(2); // num: 7; anArray: 1,2,3,5,7; ref.someVar: 5;
fn2(2); // num: 8; anArray: 1,2,3,6,8; ref.someVar: 5;```





### Summary

If everything seems completely unclear then the best thing to do is to play with the examples. Reading an explanation is much harder than understanding examples.
My explanations of closures and stack-frames, etc. are not technically correct  they are gross simplifications intended to help understanding. Once the basic idea is grokked, you can pick up the details later.

### Final points:


Whenever you use `function` inside another function, a closure is used.
Whenever you use `eval()` inside a function, a closure is used. The text you `eval` can reference local variables of the function, and within `eval` you can even create new local variables by using `eval('var foo = ')`
When you use `new Function()` (the Function constructor) inside a function, it does not create a closure. (The new function cannot reference the local variables of the outer function.)
A closure in JavaScript is like keeping a copy of all the local variables, just as they were when a function exited.
It is probably best to think that a closure is always created just an entry to a function, and the local variables are added to that closure.
A new set of local variables is kept every time a function with a closure is called (given that the function contains a function declaration inside it, and a reference to that inside function is either returned or an external reference is kept for it in some way).
Two functions might look like they have the same source text, but have completely different behaviour because of their 'hidden' closure. I don't think JavaScript code can actually find out if a function reference has a closure or not.
If you are trying to do any dynamic source code modifications (for example: `myFunction = Function(myFunction.toString().replace(/Hello/,'Hola'));`), it won't work if `myFunction` is a closure (of course, you would never even think of doing source code string substitution at runtime, but...).
It is possible to get function declarations within function declarations within functions  and you can get closures at more than one level.
I think normally a closure is the term for both the function along with the variables that are captured. Note that I do not use that definition in this article!
I suspect that closures in JavaScript differ from those normally found in functional languages.


### Links


Douglas Crockford's simulated private attributes and private methods for an object, using closures.
A great explanation of how closures can cause memory leaks in IE if you are not careful.


### Thanks

If you have just learned closures (here or elsewhere!), then I am interested in any feedback from you about any changes you might suggest that could make this article clearer. Send an email to morrisjohns.com (morris_closure @). Please note that I am not a guru on JavaScript  nor on closures.

Original post by Morris can be found in the Internet Archive.

## [How to check whether a string contains a substring in JavaScript?](https://stackoverflow.com/questions/1789945/how-to-check-whether-a-string-contains-a-substring-in-javascript)

**7439 Votes**, community-wiki

Here is a list of current possibilities:
1. (ES6) `includes`go to answer

```javascript
var string = "foo",
    substring = "oo";
string.includes(substring);
```

2. ES5 and older `indexOf`

```javascript
var string = "foo",
    substring = "oo";
string.indexOf(substring) !== -1;
```

`String.prototype.indexOf` returns the position of the string in the other string. If not found, it will return `-1`.
3. `search`go to answer

```javascript
var string = "foo",
    expr = /oo/;
string.search(expr);
```

4. lodash includesgo to answer

```javascript
var string = "foo",
    substring = "oo";
_.includes(string, substring);
```

5. RegExpgo to answer

```javascript
var string = "foo",
    expr = /oo/;  // no quotes here
expr.test(string);
```

6. Matchgo to answer

```javascript
var string = "foo",
    expr = /oo/;
string.match(expr);
```


Performance tests are showing that `indexOf` might be the best choice, if it comes to a point where speed matters.

## [How do I check if an element is hidden in jQuery?](https://stackoverflow.com/questions/178325/how-do-i-check-if-an-element-is-hidden-in-jquery)

**6576 Votes**, Philip Morton

Since the question refers to a single element, this code might be more suitable:

```javascript
// Checks css for display:[none|block], ignores visibility:[true|false]
$(element).is(":visible"); 
```

Same as twernt's suggestion, but applied to a single element; and it matches the algorithm recommended in the jQuery FAQ

## [What does use strict do in JavaScript, and what is the reasoning behind it?](https://stackoverflow.com/questions/1335851/what-does-use-strict-do-in-javascript-and-what-is-the-reasoning-behind-it)

**6575 Votes**, Mark Rogers

This article about Javascript Strict Mode might interest you: John Resig - ECMAScript 5 Strict Mode, JSON, and More
To quote some interesting parts:

Strict Mode is a new feature in ECMAScript 5 that allows you to place a program, or a function, in a "strict" operating context. This strict context prevents certain actions from being taken and throws more exceptions.

And:

Strict mode helps out in a couple ways:

It catches some common coding bloopers, throwing exceptions.
It prevents, or throws errors, when relatively "unsafe" actions are taken (such as gaining access to the global object).
It disables features that are confusing or poorly thought out.


Also note you can apply "strict mode" to the whole file... Or you can use it only for a specific function (still quoting from John Resig's article):


```javascript
// Non-strict code...

(function(){
  "use strict";

  // Define your library strictly...
})();

// Non-strict code... 
```


Which might be helpful if you have to mix old and new code ;-)
So, I suppose it's a bit like the `"use strict"` you can use in Perl (hence the name?): it helps you make fewer errors, by detecting more things that could lead to breakages.
Currently, it's supported by all major browsers (bar IE 9 and below).

## [var functionName = function() {} vs function functionName() {}](https://stackoverflow.com/questions/336859/var-functionname-function-vs-function-functionname)

**5915 Votes**, Richard Garside

The difference is that `functionOne` is a function expression and so only defined when that line is reached, whereas `functionTwo` is a function declaration and is defined as soon as its surrounding function or script is executed (due to hoisting).  
For example, a function expression:



```javascript
// TypeError: functionOne is not a function
functionOne();

var functionOne = function() {
  console.log("Hello!");
};```




And, a function declaration:   



```javascript
// Outputs: "Hello!"
functionTwo();

function functionTwo() {
  console.log("Hello!");
}```




This also means you can't conditionally define functions using function declarations:

```javascript
if (test) {
   // Error or misbehavior
   function functionThree() { doSomething(); }
}
```

The above actually defines `functionThree` irrespective of `test`'s value  unless `use strict` is in effect, in which case it simply raises an error.

## [How do I remove a particular element from an array in JavaScript?](https://stackoverflow.com/questions/5767325/how-do-i-remove-a-particular-element-from-an-array-in-javascript)

**5798 Votes**, Walker

Find the `index` of the array element you want to remove, then remove that index with `splice`.

```javascript
var array = [2, 5, 9];
var index = array.indexOf(5);
if (index > -1) {
  array.splice(index, 1);
}
// array = [2, 9]
```

The second parameter of `splice` is the number of elements to remove. Note that `splice` modifies the array in place and returns a new array containing the elements that have been removed.

Note: browser support for indexOf is limited

## [Which equals operator (== vs ===) should be used in JavaScript comparisons?](https://stackoverflow.com/questions/359494/which-equals-operator-vs-should-be-used-in-javascript-comparisons)

**5557 Votes**, bcasp

The identity (`===`) operator behaves identically to the equality (`==`) operator except no type conversion is done, and the types must be the same to be considered equal.
Reference: Javascript Tutorial: Comparison Operators
The `==` operator will compare for equality after doing any necessary type conversions.  The `===` operator will not do the conversion, so if two values are not the same type `===` will simply return `false`. Both are equally quick.
To quote Douglas Crockford's excellent JavaScript: The Good Parts,

JavaScript has two sets of equality operators: `===` and `!==`, and their evil twins `==` and `!=`.  The good ones work the way you would expect.  If the two operands are of the same type and have the same value, then `===` produces `true` and `!==` produces `false`.  The evil twins do the right thing when the operands are of the same type, but if they are of different types, they attempt to coerce the values.  the rules by which they do that are complicated and unmemorable.  These are some of the interesting cases:

```javascript
'' == '0'           // false
0 == ''             // true
0 == '0'            // true

false == 'false'    // false
false == '0'        // true

false == undefined  // false
false == null       // false
null == undefined   // true

' \t\r\n ' == 0     // true
```

The lack of transitivity is alarming.  My advice is to never use the evil twins.  Instead, always use `===` and `!==`.  All of the comparisons just shown produce `false` with the `===` operator.


Update:
A good point was brought up by @Casebash in the comments and in @Phillipe Laybaert's answer concerning reference types.  For reference types `==` and `===` act consistently with one another (except in a special case).

```javascript
var a = [1,2,3];
var b = [1,2,3];

var c = { x: 1, y: 2 };
var d = { x: 1, y: 2 };

var e = "text";
var f = "te" + "xt";

a == b            // false
a === b           // false

c == d            // false
c === d           // false

e == f            // true
e === f           // true
```

The special case is when you compare a literal with an object that evaluates to the same literal, due to its `toString` or `valueOf` method. For example, consider the comparison of a string literal with a string object created by the `String` constructor.

```javascript
"abc" == new String("abc")    // true
"abc" === new String("abc")   // false
```

Here the `==` operator is checking the values of the two objects and returning `true`, but the `===` is seeing that they're not the same type and returning `false`.  Which one is correct?  That really depends on what you're trying to compare.  My advice is to bypass the question entirely and just don't use the `String` constructor to create string objects.
Reference
http://www.ecma-international.org/ecma-262/5.1/#sec-11.9.3

## [How do I remove a property from a JavaScript object?](https://stackoverflow.com/questions/208105/how-do-i-remove-a-property-from-a-javascript-object)

**4741 Votes**, johnstok

Like this:

```javascript
delete myObject.regex;
// or,
delete myObject['regex'];
// or,
var prop = "regex";
delete myObject[prop];
```

Demo



```javascript
var myObject = {
    "ircEvent": "PRIVMSG",
    "method": "newURI",
    "regex": "^http://.*"
};
delete myObject.regex;

console.log(myObject);```




For anyone interested in reading more about it, Stack Overflow user kangax has written an incredibly in-depth blog post about the `delete` statement on their blog, Understanding delete. It is highly recommended.

## [Thinking in AngularJS if I have a jQuery background? [closed]](https://stackoverflow.com/questions/14994391/thinking-in-angularjs-if-i-have-a-jquery-background)

**4526 Votes**, Mark Rajcok

1. Don't design your page, and then change it with DOM manipulations
In jQuery, you design a page, and then you make it dynamic. This is because jQuery was designed for augmentation and has grown incredibly from that simple premise.
But in AngularJS, you must start from the ground up with your architecture in mind. Instead of starting by thinking "I have this piece of the DOM and I want to make it do X", you have to start with what you want to accomplish, then go about designing your application, and then finally go about designing your view.
2. Don't augment jQuery with AngularJS
Similarly, don't start with the idea that jQuery does X, Y, and Z, so I'll just add AngularJS on top of that for models and controllers. This is really tempting when you're just starting out, which is why I always recommend that new AngularJS developers don't use jQuery at all, at least until they get used to doing things the "Angular Way".
I've seen many developers here and on the mailing list create these elaborate solutions with jQuery plugins of 150 or 200 lines of code that they then glue into AngularJS with a collection of callbacks and `$apply`s that are confusing and convoluted; but they eventually get it working! The problem is that in most cases that jQuery plugin could be rewritten in AngularJS in a fraction of the code, where suddenly everything becomes comprehensible and straightforward.
The bottom line is this: when solutioning, first "think in AngularJS"; if you can't think of a solution, ask the community; if after all of that there is no easy solution, then feel free to reach for the jQuery. But don't let jQuery become a crutch or you'll never master AngularJS.
3. Always think in terms of architecture
First know that single-page applications are applications. They're not webpages. So we need to think like a server-side developer in addition to thinking like a client-side developer. We have to think about how to divide our application into individual, extensible, testable components.
So then how do you do that? How do you "think in AngularJS"? Here are some general principles, contrasted with jQuery.

### The view is the "official record"

In jQuery, we programmatically change the view. We could have a dropdown menu defined as a `ul` like so:

```javascript
<ul class="main-menu">
    <li class="active">
        <a href="#/home">Home</a>
    </li>
    <li>
        <a href="#/menu1">Menu 1</a>
        <ul>
            <li><a href="#/sm1">Submenu 1</a></li>
            <li><a href="#/sm2">Submenu 2</a></li>
            <li><a href="#/sm3">Submenu 3</a></li>
        </ul>
    </li>
    <li>
        <a href="#/home">Menu 2</a>
    </li>
</ul>
```

In jQuery, in our application logic, we would activate it with something like:

```javascript
$('.main-menu').dropdownMenu();
```

When we just look at the view, it's not immediately obvious that there is any functionality here. For small applications, that's fine. But for non-trivial applications, things quickly get confusing and hard to maintain.
In AngularJS, though, the view is the official record of view-based functionality. Our `ul` declaration would look like this instead:

```javascript
<ul class="main-menu" dropdown-menu>
    ...
</ul>
```

These two do the same thing, but in the AngularJS version anyone looking at the template knows what's supposed to happen. Whenever a new member of the development team comes on board, she can look at this and then know that there is a directive called `dropdownMenu` operating on it; she doesn't need to intuit the right answer or sift through any code. The view told us what was supposed to happen. Much cleaner.
Developers new to AngularJS often ask a question like: how do I find all links of a specific kind and add a directive onto them. The developer is always flabbergasted when we reply: you don't. But the reason you don't do that is that this is like half-jQuery, half-AngularJS, and no good. The problem here is that the developer is trying to "do jQuery" in the context of AngularJS. That's never going to work well. The view is the official record. Outside of a directive (more on this below), you never, ever, never change the DOM. And directives are applied in the view, so intent is clear.
Remember: don't design, and then mark up. You must architect, and then design.

### Data binding

This is by far one of the most awesome features of AngularJS and cuts out a lot of the need to do the kinds of DOM manipulations I mentioned in the previous section. AngularJS will automatically update your view so you don't have to! In jQuery, we respond to events and then update content. Something like:

```javascript
$.ajax({
  url: '/myEndpoint.json',
  success: function ( data, status ) {
    $('ul#log').append('<li>Data Received!</li>');
  }
});
```

For a view that looks like this:

```javascript
<ul class="messages" id="log">
</ul>
```

Apart from mixing concerns, we also have the same problems of signifying intent that I mentioned before. But more importantly, we had to manually reference and update a DOM node. And if we want to delete a log entry, we have to code against the DOM for that too. How do we test the logic apart from the DOM? And what if we want to change the presentation?
This a little messy and a trifle frail. But in AngularJS, we can do this:

```javascript
$http( '/myEndpoint.json' ).then( function ( response ) {
    $scope.log.push( { msg: 'Data Received!' } );
});
```

And our view can look like this:

```javascript
<ul class="messages">
    <li ng-repeat="entry in log">{{ entry.msg }}</li>
</ul>
```

But for that matter, our view could look like this:

```javascript
<div class="messages">
    <div class="alert" ng-repeat="entry in log">
        {{ entry.msg }}
    </div>
</div>
```

And now instead of using an unordered list, we're using Bootstrap alert boxes. And we never had to change the controller code! But more importantly, no matter where or how the log gets updated, the view will change too. Automatically. Neat!
Though I didn't show it here, the data binding is two-way. So those log messages could also be editable in the view just by doing this: `<input ng-model="entry.msg" />`. And there was much rejoicing.

### Distinct model layer

In jQuery, the DOM is kind of like the model. But in AngularJS, we have a separate model layer that we can manage in any way we want, completely independently from the view. This helps for the above data binding, maintains separation of concerns, and introduces far greater testability. Other answers mentioned this point, so I'll just leave it at that.

### Separation of concerns

And all of the above tie into this over-arching theme: keep your concerns separate. Your view acts as the official record of what is supposed to happen (for the most part); your model represents your data; you have a service layer to perform reusable tasks; you do DOM manipulation and augment your view with directives; and you glue it all together with controllers. This was also mentioned in other answers, and the only thing I would add pertains to testability, which I discuss in another section below.

### Dependency injection

To help us out with separation of concerns is dependency injection (DI). If you come from a server-side language (from Java to PHP) you're probably familiar with this concept already, but if you're a client-side guy coming from jQuery, this concept can seem anything from silly to superfluous to hipster. But it's not. :-)
From a broad perspective, DI means that you can declare components very freely and then from any other component, just ask for an instance of it and it will be granted. You don't have to know about loading order, or file locations, or anything like that. The power may not immediately be visible, but I'll provide just one (common) example: testing.
Let's say in our application, we require a service that implements server-side storage through a REST API and, depending on application state, local storage as well. When running tests on our controllers, we don't want to have to communicate with the server - we're testing the controller, after all. We can just add a mock service of the same name as our original component, and the injector will ensure that our controller gets the fake one automatically - our controller doesn't and needn't know the difference.
Speaking of testing...
4. Test-driven development - always
This is really part of section 3 on architecture, but it's so important that I'm putting it as its own top-level section.
Out of all of the many jQuery plugins you've seen, used, or written, how many of them had an accompanying test suite? Not very many because jQuery isn't very amenable to that. But AngularJS is.
In jQuery, the only way to test is often to create the component independently with a sample/demo page against which our tests can perform DOM manipulation. So then we have to develop a component separately and then integrate it into our application. How inconvenient! So much of the time, when developing with jQuery, we opt for iterative instead of test-driven development. And who could blame us?
But because we have separation of concerns, we can do test-driven development iteratively in AngularJS! For example, let's say we want a super-simple directive to indicate in our menu what our current route is. We can declare what we want in the view of our application:

```javascript
<a href="/hello" when-active>Hello</a>
```

Okay, now we can write a test for the non-existent `when-active` directive:

```javascript
it( 'should add "active" when the route changes', inject(function() {
    var elm = $compile( '<a href="/hello" when-active>Hello</a>' )( $scope );

    $location.path('/not-matching');
    expect( elm.hasClass('active') ).toBeFalsey();

    $location.path( '/hello' );
    expect( elm.hasClass('active') ).toBeTruthy();
}));
```

And when we run our test, we can confirm that it fails. Only now should we create our directive:

```javascript
.directive( 'whenActive', function ( $location ) {
    return {
        scope: true,
        link: function ( scope, element, attrs ) {
            scope.$on( '$routeChangeSuccess', function () {
                if ( $location.path() == element.attr( 'href' ) ) {
                    element.addClass( 'active' );
                }
                else {
                    element.removeClass( 'active' );
                }
            });
        }
    };
});
```

Our test now passes and our menu performs as requested. Our development is both iterative and test-driven. Wicked-cool.
5. Conceptually, directives are not packaged jQuery
You'll often hear "only do DOM manipulation in a directive". This is a necessity. Treat it with due deference!
But let's dive a little deeper...
Some directives just decorate what's already in the view (think `ngClass`) and therefore sometimes do DOM manipulation straight away and then are basically done. But if a directive is like a "widget" and has a template, it should also respect separation of concerns. That is, the template too should remain largely independent from its implementation in the link and controller functions.
AngularJS comes with an entire set of tools to make this very easy; with `ngClass` we can dynamically update the class; `ngModel` allows two-way data binding; `ngShow` and `ngHide` programmatically show or hide an element; and many more - including the ones we write ourselves. In other words, we can do all kinds of awesomeness without DOM manipulation. The less DOM manipulation, the easier directives are to test, the easier they are to style, the easier they are to change in the future, and the more re-usable and distributable they are.
I see lots of developers new to AngularJS using directives as the place to throw a bunch of jQuery. In other words, they think "since I can't do DOM manipulation in the controller, I'll take that code put it in a directive". While that certainly is much better, it's often still wrong.
Think of the logger we programmed in section 3. Even if we put that in a directive, we still want to do it the "Angular Way". It still doesn't take any DOM manipulation! There are lots of times when DOM manipulation is necessary, but it's a lot rarer than you think! Before doing DOM manipulation anywhere in your application, ask yourself if you really need to. There might be a better way.
Here's a quick example that shows the pattern I see most frequently. We want a toggleable button. (Note: this example is a little contrived and a skosh verbose to represent more complicated cases that are solved in exactly the same way.)

```javascript
.directive( 'myDirective', function () {
    return {
        template: '<a class="btn">Toggle me!</a>',
        link: function ( scope, element, attrs ) {
            var on = false;

            $(element).click( function () {
                on = !on;
                $(element).toggleClass('active', on);
            });
        }
    };
});
```

There are a few things wrong with this:

First, jQuery was never necessary. There's nothing we did here that needed jQuery at all!
Second, even if we already have jQuery on our page, there's no reason to use it here; we can simply use `angular.element` and our component will still work when dropped into a project that doesn't have jQuery.
Third, even assuming jQuery was required for this directive to work, jqLite (`angular.element`) will always use jQuery if it was loaded! So we needn't use the ``$ - we can just use `angular.element`.
Fourth, closely related to the third, is that jqLite elements needn't be wrapped in ``$ - the `element` that is passed to the `link` function would already be a jQuery element! 
And fifth, which we've mentioned in previous sections, why are we mixing template stuff into our logic?

This directive can be rewritten (even for very complicated cases!) much more simply like so:

```javascript
.directive( 'myDirective', function () {
    return {
        scope: true,
        template: '<a class="btn" ng-class="{active: on}" ng-click="toggle()">Toggle me!</a>',
        link: function ( scope, element, attrs ) {
            scope.on = false;

            scope.toggle = function () {
                scope.on = !scope.on;
            };
        }
    };
});
```

Again, the template stuff is in the template, so you (or your users) can easily swap it out for one that meets any style necessary, and the logic never had to be touched. Reusability - boom!
And there are still all those other benefits, like testing - it's easy! No matter what's in the template, the directive's internal API is never touched, so refactoring is easy. You can change the template as much as you want without touching the directive. And no matter what you change, your tests still pass.
w00t!
So if directives aren't just collections of jQuery-like functions, what are they? Directives are actually extensions of HTML. If HTML doesn't do something you need it to do, you write a directive to do it for you, and then use it just as if it was part of HTML.
Put another way, if AngularJS doesn't do something out of the box, think how the team would accomplish it to fit right in with `ngClick`, `ngClass`, et al.
Summary
Don't even use jQuery. Don't even include it. It will hold you back. And when you come to a problem that you think you know how to solve in jQuery already, before you reach for the ``$, try to think about how to do it within the confines the AngularJS. If you don't know, ask! 19 times out of 20, the best way to do it doesn't need jQuery and to try to solve it with jQuery results in more work for you.

## [What is the most efficient way to deep clone an object in JavaScript?](https://stackoverflow.com/questions/122102/what-is-the-most-efficient-way-to-deep-clone-an-object-in-javascript)

**4426 Votes**, community-wiki

Note: This is a reply to another answer, not a proper response to this question. If you wish to have fast object cloning please follow Corban's advice in their answer to this question.


I want to note that the `.clone()` method in jQuery only clones DOM elements. In order to clone JavaScript objects, you would do:

```javascript
// Shallow copy
var newObject = jQuery.extend({}, oldObject);

// Deep copy
var newObject = jQuery.extend(true, {}, oldObject);
```

More information can be found in the jQuery documentation.
I also want to note that the deep copy is actually much smarter than what is shown above  it's able to avoid many traps (trying to deep extend a DOM element, for example). It's used frequently in jQuery core and in plugins to great effect.

## [How do I return the response from an asynchronous call?](https://stackoverflow.com/questions/14220321/how-do-i-return-the-response-from-an-asynchronous-call)

**4134 Votes**, Felix Kling

`->` For a more general explanation of async behaviour with different examples, please see Why is my variable unaltered after I modify it inside of a function? - Asynchronous code reference 
`->` If you already understand the problem, skip to the possible solutions below.

The problem
The A in Ajax stands for asynchronous . That means sending the request (or rather receiving the response) is taken out of the normal execution flow. In your example, `$.ajax` returns immediately and the next statement, `return result;`, is executed before the function you passed as `success` callback was even called.
Here is an analogy which hopefully makes the difference between synchronous and asynchronous flow clearer: 

### Synchronous

Imagine you make a phone call to a friend and ask him to look something up for you. Although it might take a while, you wait on the phone and stare into space, until your friend gives you the answer that you needed.
The same is happening when you make a function call containing "normal" code:

```javascript
function findItem() {
    var item;
    while(item_not_found) {
        // search
    }
    return item;
}

var item = findItem();

// Do something with item
doSomethingElse();
```

Even though `findItem` might take a long time to execute, any code coming after `var item = findItem();` has to wait until the function returns the result.

### Asynchronous

You call your friend again for the same reason. But this time you tell him that you are in a hurry and he should call you back on your mobile phone. You hang up, leave the house and do whatever you planned to do. Once your friend calls you back, you are dealing with the information he gave to you.
That's exactly what's happening when you do an Ajax request. 

```javascript
findItem(function(item) {
    // Do something with item
});
doSomethingElse();
```

Instead of waiting for the response, the execution continues immediately and the statement after the Ajax call is executed. To get the response eventually, you provide a function to be called once the response was received, a callback (notice something? call back ?). Any statement coming after that call is executed before the callback is called.


Solution(s)
Embrace the asynchronous nature of JavaScript! While certain asynchronous operations provide synchronous counterparts (so does "Ajax"), it's generally discouraged to use them, especially in a browser context.
Why is it bad do you ask?
JavaScript runs in the UI thread of the browser and any long running process will lock the UI, making it unresponsive. Additionally, there is an upper limit on the execution time for JavaScript and the browser will ask the user whether to continue the execution or not. 
All of this is really bad user experience. The user won't be able to tell whether everything is working fine or not. Furthermore, the effect will be worse for users with a slow connection.
In the following we will look at three different solutions that are all building on top of each other:

Promises with `async/await` (ES2017+, available in older browsers if you use a transpiler or regenerator)
Callbacks (popular in node)
Promises with `then()` (ES2015+, available in older browsers if you use one of the many promise libraries)

All three are available in current browsers, and node 7+. 


### ES2017+: Promises with `async/await`

The new ECMAScript version released in 2017 introduced syntax-level support for asynchronous functions. With the help of `async` and `await`, you can write asynchronous in a "synchronous style". Make no mistake though: The code is still asynchronous, but it's easier to read/understand.
`async/await` builds on top of promises: an `async` function always returns a promise. `await` "unwraps" a promise and either result in the value the promise was resolved with or throws an error if the promise was rejected.
Important: You can only use `await` inside an `async` function. That means that at the very top level, you still have to work directly with the promise.
You can read more about `async` and `await` on MDN.
Here is an example that builds on top of delay above:

```javascript
// Using 'superagent' which will return a promise.
var superagent = require('superagent')

// This is isn't declared as `async` because it already returns a promise
function delay() {
  // `delay` returns a promise
  return new Promise(function(resolve, reject) {
    // Only `delay` is able to resolve or reject the promise
    setTimeout(function() {
      resolve(42); // After 3 seconds, resolve the promise with value 42
    }, 3000);
  });
}


async function getAllBooks() {
  try {
    // GET a list of book IDs of the current user
    var bookIDs = await superagent.get('/user/books');
    // wait for a second (just for the sake of this example)
    await delay(1000);
    // GET information about each book
    return await superagent.get('/books/ids='+JSON.stringify(bookIDs));
  } catch(error) {
    // If any of the awaited promises was rejected, this catch block
    // would catch the rejection reason
    return null;
  }
}

// Async functions always return a promise
getAllBooks()
  .then(function(books) {
    console.log(books);
  });
```

Newer browser and node versions support `async/await`. You can also support older environments by transforming your code to ES5 with the help of regenerator (or tools that use regenerator, such as Babel).


### Let functions accept callbacks

A callback is simply a function passed to another function. That other function can call the function passed whenever it is ready. In the context of an asynchronous process, the callback will be called whenever the asynchronous process is done. Usually, the result is passed to the callback.
In the example of the question, you can make `foo` accept a callback and use it as `success` callback. So this

```javascript
var result = foo();
// Code that depends on 'result'
```

becomes

```javascript
foo(function(result) {
    // Code that depends on 'result'
});
```

Here we defined the function "inline" but you can pass any function reference:

```javascript
function myCallback(result) {
    // Code that depends on 'result'
}

foo(myCallback);
```

`foo` itself is defined as follows:

```javascript
function foo(callback) {
    $.ajax({
        // ...
        success: callback
    });
}
```

`callback` will refer to the function we pass to `foo` when we call it and we simply pass it on to `success`. I.e. once the Ajax request is successful, `$.ajax` will call `callback` and pass the response to the callback (which can be referred to with `result`, since this is how we defined the callback).
You can also process the response before passing it to the callback:

```javascript
function foo(callback) {
    $.ajax({
        // ...
        success: function(response) {
            // For example, filter the response
            callback(filtered_response);
        }
    });
}
```

It's easier to write code using callbacks than it may seem. After all, JavaScript in the browser is heavily event-driven (DOM events). Receiving the Ajax response is nothing else but an event.
Difficulties could arise when you have to work with third-party code, but most problems can be solved by just thinking through the application flow.


### ES2015+: Promises with then()

The Promise API is a new feature of ECMAScript 6 (ES2015), but it has good browser support already. There are also many libraries which implement the standard Promises API and provide additional methods to ease the use and composition of asynchronous functions (e.g. bluebird).
Promises are containers for future values. When the promise receives the value (it is resolved) or when it is cancelled (rejected), it notifies all of its "listeners" who want to access this value.
The advantage over plain callbacks is that they allow you to decouple your code and they are easier to compose.
Here is a simple example of using a promise:

```javascript
function delay() {
  // `delay` returns a promise
  return new Promise(function(resolve, reject) {
    // Only `delay` is able to resolve or reject the promise
    setTimeout(function() {
      resolve(42); // After 3 seconds, resolve the promise with value 42
    }, 3000);
  });
}

delay()
  .then(function(v) { // `delay` returns a promise
    console.log(v); // Log the value once it is resolved
  })
  .catch(function(v) {
    // Or do something else if it is rejected 
    // (it would not happen in this example, since `reject` is not called).
  });
```

Applied to our Ajax call we could use promises like this:

```javascript
function ajax(url) {
  return new Promise(function(resolve, reject) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      resolve(this.responseText);
    };
    xhr.onerror = reject;
    xhr.open('GET', url);
    xhr.send();
  });
}

ajax("/echo/json")
  .then(function(result) {
    // Code depending on result
  })
  .catch(function() {
    // An error occurred
  });
```

Describing all the advantages that promise offer is beyond the scope of this answer, but if you write new code, you should seriously consider them. They provide a great abstraction and separation of your code.
More information about promises: HTML5 rocks - JavaScript Promises
Side note: jQuery's deferred objects
Deferred objects are jQuery's custom implementation of promises (before the Promise API was standardized). They behave almost like promises but expose a slightly different API.
Every Ajax method of jQuery already returns a "deferred object" (actually a promise of a deferred object) which you can just return from your function:

```javascript
function ajax() {
    return $.ajax(...);
}

ajax().done(function(result) {
    // Code depending on result
}).fail(function() {
    // An error occurred
});
```

Side note: Promise gotchas
Keep in mind that promises and deferred objects are just containers for a future value, they are not the value itself. For example, suppose you had the following:

```javascript
function checkPassword() {
    return $.ajax({
        url: '/password',
        data: {
            username: $('#username').val(),
            password: $('#password').val()
        },
        type: 'POST',
        dataType: 'json'
    });
}

if (checkPassword()) {
    // Tell the user they're logged in
}
```

This code misunderstands the above asynchrony issues. Specifically, `$.ajax()` doesn't freeze the code while it checks the '/password' page on your server - it sends a request to the server and while it waits, immediately returns a jQuery Ajax Deferred object, not the response from the server. That means the `if` statement is going to always get this Deferred object, treat it as `true`, and proceed as though the user is logged in. Not good.
But the fix is easy:

```javascript
checkPassword()
.done(function(r) {
    if (r) {
        // Tell the user they're logged in
    } else {
        // Tell the user their password was bad
    }
})
.fail(function(x) {
    // Tell the user something bad happened
});
```




### Not recommended: Synchronous "Ajax" calls

As I mentioned, some(!) asynchronous operations have synchronous counterparts. I don't advocate their use, but for completeness' sake, here is how you would perform a synchronous call:
Without jQuery
If you directly use a `XMLHTTPRequest` object, pass `false` as third argument to `.open`.
jQuery
If you use jQuery, you can set the `async` option to `false`. Note that this option is deprecated since jQuery 1.8.
You can then either still use a `success` callback or access the `responseText` property of the jqXHR object:

```javascript
function foo() {
    var jqXHR = $.ajax({
        //...
        async: false
    });
    return jqXHR.responseText;
}
```

If you use any other jQuery Ajax method, such as `$.get`, `$.getJSON`, etc., you have to change it to `$.ajax` (since you can only pass configuration parameters to `$.ajax`).
Heads up! It is not possible to make a synchronous JSONP request. JSONP by its very nature is always asynchronous (one more reason to not even consider this option).

## [How do I include a JavaScript file in another JavaScript file?](https://stackoverflow.com/questions/950087/how-do-i-include-a-javascript-file-in-another-javascript-file)

**4019 Votes**, Alec Smart

The old versions of JavaScript had no import, include, or require, so many different approaches to this problem have been developed.
But recent versions of JavaScript have standards like ES6 modules to import modules, although this is not supported yet by most browsers.  Many people using modules with browser applications use build and/or transpilation tools to make it practical to use new syntax with features like modules.
ES6 Modules
Note that currently, browser support for ES6 Modules is not particularly great, but it is on its way. According to this StackOverflow answer, they are supported in Chrome 61, Firefox 54(behind the `dom.moduleScripts.enabled` setting in `about:config`) and MS Edge 16, with only Safari 10.1 providing support without flags.
Thus, you will currently still need to use build and/or transpilation tools to valid JavaScript that will run in without any requirement for the user to use those browser versions or enable any flags.
Once ES6 Modules are commonplace, here is how you would go about using them:

```javascript
// module.js
export function hello() {
  return "Hello";
}
```


```javascript
// main.js
import {hello} from 'module'; // or './module'
let val = hello(); // val is "Hello";
```

Node.js require
Node.js is currently using a module.exports/require system.  You can use `babel` to transpile if you want the `import` syntax.    

```javascript
// mymodule.js
module.exports = {
   hello: function() {
      return "Hello";
   }
}
```


```javascript
// server.js
const myModule = require('./mymodule');
let val = myModule.hello(); // val is "Hello"   
```

There are other ways for JavaScript to include external JavaScript contents in browsers that do not require preprocessing.
AJAX Loading
You could load an additional script with an AJAX call and then use `eval` to run it. This is the most straightforward way, but it is limited to your domain because of the JavaScript sandbox security model. Using `eval` also opens the door to bugs, hacks and security issues.
jQuery Loading
The jQuery library provides loading functionality in one line:

```javascript
$.getScript("my_lovely_script.js", function() {
   alert("Script loaded but not necessarily executed.");
});
```

Dynamic Script Loading
You could add a script tag with the script URL into the HTML. To avoid the overhead of jQuery, this is an ideal solution.
The script can even reside on a different server. Furthermore, the browser evaluates the code. The `<script>` tag can be injected into either the web page `<head>`, or inserted just before the closing `</body>` tag.
Here is an example of how this could work:

```javascript
function dynamicallyLoadScript(url) {
    var script = document.createElement("script"); // Make a script DOM node
    script.src = url; // Set it's src to the provided URL

    document.head.appendChild(script); // Add it to the end of the head section of the page (could change 'head' to 'body' to add it to the end of the body section instead)
}
```

This function will add a new `<script>` tag to end of the head section of the page, where the `src` attribute is set to the URL which is given to the function as the first parameter.
Both of these solutions are discussed and illustrated in JavaScript Madness: Dynamic Script Loading.

### Detecting when the script has been executed

Now, there is a big issue you must know about. Doing that implies that you remotely load the code. Modern web browsers will load the file and keep executing your current script because they load everything asynchronously to improve performance. (This applies to both the jQuery method and the manual dynamic script loading method.)
It means that if you use these tricks directly, you won't be able to use your newly loaded code the next line after you asked it to be loaded, because it will be still loading.
For example: `my_lovely_script.js` contains `MySuperObject`:

```javascript
var js = document.createElement("script");

js.type = "text/javascript";
js.src = jsFilePath;

document.body.appendChild(js);

var s = new MySuperObject();

Error : MySuperObject is undefined
```

Then you reload the page hitting F5. And it works! Confusing...
So what to do about it ?
Well, you can use the hack the author suggests in the link I gave you. In summary, for people in a hurry, he uses an event to run a callback function when the script is loaded. So you can put all the code using the remote library in the callback function. For example:

```javascript
function loadScript(url, callback)
{
    // Adding the script tag to the head as suggested before
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;

    // Then bind the event to the callback function.
    // There are several events for cross browser compatibility.
    script.onreadystatechange = callback;
    script.onload = callback;

    // Fire the loading
    head.appendChild(script);
}
```

Then you write the code you want to use AFTER the script is loaded in a lambda function:

```javascript
var myPrettyCode = function() {
   // Here, do whatever you want
};
```

Then you run all that:

```javascript
loadScript("my_lovely_script.js", myPrettyCode);
```

Note that the script may execute after the DOM has loaded, or before, depending on the browser and whether you included the line `script.async = false;`. There's a great article on Javascript loading in general which discusses this.
Source Code Merge/Preprocessing
As mentioned at the top of this answer, many developers now use build/transpilation tool(s) like WebPack, Babel, or Gulp in their projects, allowing them to use new syntax and support modules better, combine files, minify, etc.

## [For-each over an array in JavaScript?](https://stackoverflow.com/questions/9329446/for-each-over-an-array-in-javascript)

**3673 Votes**, Dante1986

TL;DR

Don't use `for-in` unless you use it with safeguards or are at least aware of why it might bite you.
Your best bets are usually

a `for-of` loop (ES2015+ only),
`Array#forEach` (`spec` | `MDN`) (or its relatives `some` and such) (ES5+ only),
a simple old-fashioned `for` loop,
or `for-in` with safeguards.


But there's lots more to explore, read on...

JavaScript has powerful semantics for looping through arrays and array-like objects. I've split the answer into two parts: Options for genuine arrays, and options for things that are just array-like, such as the `arguments` object, other iterable objects (ES2015+), DOM collections, and so on.
I'll quickly note that you can use the ES2015 options now, even on ES5 engines, by transpiling ES2015 to ES5. Search for "ES2015 transpiling" / "ES6 transpiling" for more...
Okay, let's look at our options:

### For Actual Arrays

You have three options in ECMAScript5 ("ES5"), the version most broadly supported at the moment, and will soon have two more in ECMAScript2015 ("ES2015", "ES6"), the latest version of JavaScript that vendors are working on supporting:

Use `forEach` and related (ES5+)
Use a simple `for` loop
Use `for-in` correctly
Use `for-of` (use an iterator implicitly) (ES2015+)
Use an iterator explicitly (ES2015+)

Details:
1. Use `forEach` and related
If you're using an environment that supports the `Array` features of ES5 (directly or using a shim), you can use the new `forEach` (`spec` | `MDN`):

```javascript
var a = ["a", "b", "c"];
a.forEach(function(entry) {
    console.log(entry);
});
```

`forEach` accepts an iterator function and, optionally, a value to use as `this` when calling that iterator function (not used above). The iterator function is called for each entry in the array, in order, skipping non-existent entries in sparse arrays. Although I only used one argument above, the iterator function is called with three: The value of each entry, the index of that entry, and a reference to the array you're iterating over (in case your function doesn't already have it handy).
Unless you're supporting obsolete browsers like IE8 (which NetApps shows at just over 4% market share as of this writing in September2016), you can happily use `forEach` in a general-purpose web page without a shim. If you do need to support obsolete browsers, shimming/polyfilling `forEach` is easily done (search for "es5 shim" for several options).
`forEach` has the benefit that you don't have to declare indexing and value variables in the containing scope, as they're supplied as arguments to the iteration function, and so nicely scoped to just that iteration.
If you're worried about the runtime cost of making a function call for each array entry, don't be; details.
Additionally, `forEach` is the "loop through them all" function, but ES5 defined several other useful "work your way through the array and do things" functions, including:

`every` (stops looping the first time the iterator returns `false` or something falsey)
`some` (stops looping the first time the iterator returns `true` or something truthy)
`filter` (creates a new array including elements where the filter function returns `true` and omitting the ones where it returns `false`)
`map` (creates a new array from the values returned by the iterator function)
`reduce` (builds up a value by repeated calling the iterator, passing in previous values; see the spec for the details; useful for summing the contents of an array and many other things)
`reduceRight` (like `reduce`, but works in descending rather than ascending order)

2. Use a simple `for` loop
Sometimes the old ways are the best:

```javascript
var index;
var a = ["a", "b", "c"];
for (index = 0; index < a.length; ++index) {
    console.log(a[index]);
}
```

If the length of the array won't change during the loop, and it's in performance-sensitive code (unlikely), a slightly more complicated version grabbing the length up front might be a tiny bit faster:

```javascript
var index, len;
var a = ["a", "b", "c"];
for (index = 0, len = a.length; index < len; ++index) {
    console.log(a[index]);
}
```

And/or counting backward:

```javascript
var index;
var a = ["a", "b", "c"];
for (index = a.length - 1; index >= 0; --index) {
    console.log(a[index]);
}
```

But with modern JavaScript engines, it's rare you need to eke out that last bit of juice.
In ES2015 and higher, you can make your index and value variables local to the `for` loop:

```javascript
let a = ["a", "b", "c"];
for (let index = 0; index < a.length; ++index) {
    let value = a[index];
}
//console.log(index); // Would cause "ReferenceError: index is not defined"
//console.log(value); // Would cause "ReferenceError: value is not defined"
```

And when you do that, not just `value` but also `index` is recreated for each loop iteration, meaning closures created in the loop body keep a reference to the `index` (and `value`) created for that specific iteration:

```javascript
let divs = document.querySelectorAll("div");
for (let index = 0; index < divs.length; ++index) {
    divs[index].addEventListener('click', e => {
        alert("Index is: " + index);
    });
}
```

If you had five divs, you'd get "Index is: 0" if you clicked the first and "Index is: 4" if you clicked the last. This does not work if you use `var` instead of `let`.
3. Use `for-in` correctly
You'll get people telling you to use `for-in`, but that's not what `for-in` is for. `for-in` loops through the enumerable properties of an object, not the indexes of an array. The order is not guaranteed, not even in ES2015 (ES6). ES2015 does define an order to object properties (via `[[OwnPropertyKeys]]`, `[[Enumerate]]`, and things that use them like `Object.getOwnPropertyKeys`), but it does not define that `for-in` will follow that order. (Details in this other answer.)
Still, it can be useful, particularly for sparse arrays, if you use appropriate safeguards:

```javascript
// `a` is a sparse array
var key;
var a = [];
a[0] = "a";
a[10] = "b";
a[10000] = "c";
for (key in a) {
    if (a.hasOwnProperty(key)  &&        // These are explained
        /^0$|^[1-9]\d*$/.test(key) &&    // and then hidden
        key <= 4294967294                // away below
        ) {
        console.log(a[key]);
    }
}
```

Note the two checks:

That the object has its own property by that name (not one it inherits from its prototype), and
That the key is a base-10 numeric string in its normal string form and its value is <= 2^32 - 2 (which is 4,294,967,294). Where does that number come from? It's part of the definition of an array index in the specification. Other numbers (non-integers, negative numbers, numbers greater than 2^32 - 2) are not array indexes. The reason it's 2^32 - 2 is that that makes the greatest index value one lower than 2^32 - 1, which is the maximum value an array's `length` can have. (E.g., an array's length fits in a 32-bit unsigned integer.) (Props to RobG for pointing out in a comment on my blog post that my previous test wasn't quite right.)

That's a tiny bit of added overhead per loop iteration on most arrays, but if you have a sparse array, it can be a more efficient way to loop because it only loops for entries that actually exist. E.g., for the array above, we loop a total of three times (for keys `"0"`, `"10"`, and `"10000"` remember, they're strings), not 10,001 times.
Now, you won't want to write that every time, so you might put this in your toolkit:

```javascript
function arrayHasOwnIndex(array, prop) {
    return array.hasOwnProperty(prop) && /^0$|^[1-9]\d*$/.test(prop) && prop <= 4294967294; // 2^32 - 2
}
```

And then we'd use it like this:

```javascript
for (key in a) {
    if (arrayHasOwnIndex(a, key)) {
        console.log(a[key]);
    }
}
```

Or if you're interested in just a "good enough for most cases" test, you could use this, but while it's close, it's not quite correct:

```javascript
for (key in a) {
    // "Good enough" for most cases
    if (String(parseInt(key, 10)) === key && a.hasOwnProperty(key)) {
        console.log(a[key]);
    }
}
```

4. Use `for-of` (use an iterator implicitly) (ES2015+)
ES2015 adds iterators to JavaScript. The easiest way to use iterators is the new `for-of` statement. It looks like this:

```javascript
var val;
var a = ["a", "b", "c"];
for (val of a) {
    console.log(val);
}
```

Output:

a
b
c

Under the covers, that gets an iterator from the array and loops through it, getting the values from it. This doesn't have the issue that using `for-in` has, because it uses an iterator defined by the object (the array), and arrays define that their iterators iterate through their entries (not their properties). Unlike `for-in` in ES5, the order in which the entries are visited is the numeric order of their indexes.
5. Use an iterator explicitly (ES2015+)
Sometimes, you might want to use an iterator explicitly. You can do that, too, although it's a lot clunkier than `for-of`. It looks like this:

```javascript
var a = ["a", "b", "c"];
var it = a.values();
var entry;
while (!(entry = it.next()).done) {
    console.log(entry.value);
}
```

The iterator is a function (specifically, a generator) that returns a new object each time you call `next`. The object returned by the iterator has a property, `done`, telling us whether it's done, and a property `value` with the value for that iteration.
The meaning of `value` varies depending on the iterator; arrays support (at least) three functions that return iterators:

`values()`: This is the one I used above. It returns an iterator where each `value` is the value for that iteration.
`keys()`: Returns an iterator where each `value` is the key for that iteration (so for our ``a above, that would be `"0"`, then `"1"`, then `"2"`).
`entries()`: Returns an iterator where each `value` is an array in the form `[key, value]` for that iteration.

(As of this writing, Firefox 29 supports `entries` and `keys` but not `values`.)

### For Array-Like Objects

Aside from true arrays, there are also array-like objects that have a `length` property and properties with numeric names: `NodeList` instances, the `arguments` object, etc. How do we loop through their contents?
Use any of the options above for arrays
At least some, and possibly most or even all, of the array approaches above frequently apply equally well to array-like objects:

Use `forEach` and related (ES5+)
The various functions on `Array.prototype` are "intentionally generic" and can usually be used on array-like objects via `Function#call` or `Function#apply`. (See the Caveat for host-provided objects at the end of this answer, but it's a rare issue.)
Suppose you wanted to use `forEach` on a `Node`'s `childNodes` property. You'd do this:

```javascript
Array.prototype.forEach.call(node.childNodes, function(child) {
    // Do something with `child`
});
```

If you're going to do that a lot, you might want to grab a copy of the function reference into a variable for reuse, e.g.:

```javascript
// (This is all presumably in some scoping function)
var forEach = Array.prototype.forEach;

// Then later...
forEach.call(node.childNodes, function(child) {
    // Do something with `child`
});
```

Use a simple `for` loop
Obviously, a simple `for` loop applies to array-like objects.
Use `for-in` correctly
`for-in` with the same safeguards as with an array should work with array-like objects as well; the caveat for host-provided objects on #1 above may apply.
Use `for-of` (use an iterator implicitly) (ES2015+)
`for-of` will use the iterator provided by the object (if any); we'll have to see how this plays with the various array-like objects, particularly host-provided ones.
Use an iterator explicitly (ES2015+)
See #4, we'll have to see how iterators play out.

Create a true array
Other times, you may want to convert an array-like object into a true array. Doing that is surprisingly easy:

Use the `slice` method of arrays
We can use the `slice` method of arrays, which like the other methods mentioned above is "intentionally generic" and so can be used with array-like objects, like this:

```javascript
var trueArray = Array.prototype.slice.call(arrayLikeObject);
```

So for instance, if we want to convert a `NodeList` into a true array, we could do this:

```javascript
var divs = Array.prototype.slice.call(document.querySelectorAll("div"));
```

See the Caveat for host-provided objects below. In particular, note that this will fail in IE8 and earlier, which don't let you use host-provided objects as `this` like that.
Use spread notation (`...`)
It's also possible to use ES2015's spread notation (MDN currently calls it an operator; it isn't one), with JavaScript engines that support this feature:

```javascript
var trueArray = [...iterableObject];
```

So for instance, if we want to convert a `NodeList` into a true array, with spread syntax this becomes quite succinct:

```javascript
var divs = [...document.querySelectorAll("div")];
```

Use `Array.from` (spec) | (MDN)
`Array.from` (ES2015, but shimmable) creates an array from an array-like object, optionally passing the entries through a mapping function first. So:

```javascript
var divs = Array.from(document.querySelectorAll("div"));
```

Or if you wanted to get an array of the tag names of the elements with a given class, you'd use the mapping function:

```javascript
// Arrow function (ES2015):
var divs = Array.from(document.querySelectorAll(".some-class"), element => element.tagName);

// Standard function (since `Array.from` can be shimmed):
var divs = Array.from(document.querySelectorAll(".some-class"), function(element) {
    return element.tagName;
});
```


Caveat for host-provided objects
If you use `Array.prototype` functions with host-provided array-like objects (DOM lists and other things provided by the browser rather than the JavaScript engine), you need to be sure to test in your target environments to make sure the host-provided object behaves properly. Most do behave properly (now), but it's important to test. The reason is that most of the `Array.prototype` methods you're likely to want to use rely on the host-provided object giving an honest answer to the abstract `[[HasProperty]]` operation. As of this writing, browsers do a very good job of this, but the ES5 spec did allow for the possibility a host-provided object may not be honest; it's in 8.6.2 (several paragraphs below the big table near the beginning of that section), where it says:

Host objects may implement these internal methods in any manner unless specified otherwise; for example, one possibility is that `[[Get]]` and `[[Put]]` for a particular host object indeed fetch and store property values but `[[HasProperty]]` always generates false.

(I couldn't find the equivalent verbiage in the ES2015 spec, but it's bound to still be the case.) Again, as of this writing the common host-provided array-like objects in modern browsers (`NodeList` instances, for instance) do handle `[[HasProperty]]` correctly, but it's important to test.

## [Which href value should I use for JavaScript links, # or javascript:void(0)?](https://stackoverflow.com/questions/134845/which-href-value-should-i-use-for-javascript-links-or-javascriptvoid0)

**3620 Votes**, community-wiki

I use `javascript:void(0)`.
Three reasons. Encouraging the use of ``# amongst a team of developers inevitably leads to some using the return value of the function called like this:

```javascript
function doSomething() {
    //Some code
    return false;
}
```

But then they forget to use `return doSomething()` in the onclick and just use `doSomething()`.
A second reason for avoiding ``# is that the final `return false;` will not execute if the called function throws an error. Hence the developers have to also remember to handle any error appropriately in the called function.
A third reason is that there are cases where the `onclick` event property is assigned dynamically.  I prefer to be able to call a function or assign it dynamically without having to code the function specifically for one method of attachment or another. Hence my `onclick` (or on anything) in HTML markup look like this:

```javascript
onclick="someFunc.call(this)"
```

OR

```javascript
onclick="someFunc.apply(this, arguments)"
```

Using `javascript:void(0)` avoids all of the above headaches, and I haven't found any examples of a downside.
So if you're a lone developer then you can clearly make your own choice, but if you work as a team you have to either state:
Use `href="#"`, make sure `onclick` always contains `return false;` at the end, that any called function does not throw an error and if you attach a function dynamically to the `onclick` property make sure that as well as not throwing an error it returns `false`.
OR
Use `href="javascript:void(0)"`
The second is clearly much easier to communicate.

## [Setting checked for a checkbox with jQuery?](https://stackoverflow.com/questions/426258/setting-checked-for-a-checkbox-with-jquery)

**3518 Votes**, tpower

### jQuery 1.6+

Use the new `.prop()` method:

```javascript
$('.myCheckbox').prop('checked', true);
$('.myCheckbox').prop('checked', false);
```


### jQuery 1.5.x and below

The `.prop()` method is not available, so you need to use `.attr()`.

```javascript
$('.myCheckbox').attr('checked', true);
$('.myCheckbox').attr('checked', false);
```

Note that this is the approach used by jQuery's unit tests prior to version 1.6 and is preferable to using

```javascript
$('.myCheckbox').removeAttr('checked');
```

since the latter will, if the box was initially checked, change the behaviour of a call to `.reset()` on any form that contains it - a subtle but probably unwelcome behaviour change.
For more context, some incomplete discussion of the changes to the handling of the `checked` attribute/property in the transition from 1.5.x to 1.6 can be found in the version 1.6 release notes and the Attributes vs. Properties section of the `.prop()` documentation.

### Any version of jQuery

If you're working with just one element, you can always just modify the `HTMLInputElement`'s `.checked` property:

```javascript
$('.myCheckbox')[0].checked = true;
$('.myCheckbox')[0].checked = false;
```

The benefit to using the `.prop()` and `.attr()` methods instead of this is that they will operate on all matched elements.

## [Why does Google prepend while(1); to their JSON responses?](https://stackoverflow.com/questions/2669690/why-does-google-prepend-while1-to-their-json-responses)

**3424 Votes**, Jess

It prevents JSON hijacking.
Contrived example: say Google has a URL like `mail.google.com/json?action=inbox` which returns the first 50 messages of your inbox in JSON format. Evil websites on other domains can't make AJAX requests to get this data due to the same-origin policy, but they can include the URL via a `<script>` tag. The URL is visited with your cookies, and by overriding the global array constructor or accessor methods they can have a method called whenever an object (array or hash) attribute is set, allowing them to read the JSON content.
The `while(1);` or `&&&BLAH&&&` prevents this: an AJAX request at `mail.google.com` will have full access to the text content, and can strip it away. But a `<script>` tag insertion blindly executes the JavaScript without any processing, resulting in either an infinite loop or a syntax error.
This does not address the issue of cross-site request forgery.

## [How do you get a timestamp in JavaScript?](https://stackoverflow.com/questions/221294/how-do-you-get-a-timestamp-in-javascript)

**3266 Votes**, pupeno

```javascript
var timeStampInMs = window.performance && window.performance.now && window.performance.timing && window.performance.timing.navigationStart ? window.performance.now() + window.performance.timing.navigationStart : Date.now();

console.log(timeStampInMs, Date.now());```




Short & Snazzy:

```javascript
+ new Date()
```

A unary operator like `plus` triggers the `valueOf` method in the `Date` object and it returns the timestamp (without any alteration).
Details:
On almost all current browsers you can use `Date.now()` to get the UTC timestamp in milliseconds; a notable exception to this is IE8 and earlier (see compatibility table).
You can easily make a shim for this, though:

```javascript
if (!Date.now) {
    Date.now = function() { return new Date().getTime(); }
}
```

To get the timestamp in seconds, you can use:

```javascript
Math.floor(Date.now() / 1000)
```

Or alternatively you could use:

```javascript
Date.now() / 1000 | 0
```

Which should be slightly faster, but also less readable (also see this answer).
I would recommend using `Date.now()` (with compatibility shim). It's slightly better because it's shorter & doesn't create a new `Date` object. However, if you don't want a shim & maximum compatibility, you could use the "old" method to get the timestamp in milliseconds:

```javascript
new Date().getTime()
```

Which you can then convert to seconds like this:

```javascript
Math.round(new Date().getTime()/1000)
```

And you can also use the `valueOf` method which we showed above:

```javascript
new Date().valueOf()
```

## [How do I check if an array includes an object in JavaScript?](https://stackoverflow.com/questions/237104/how-do-i-check-if-an-array-includes-an-object-in-javascript)

**3133 Votes**, brad

Current browsers have `Array#includes`, which does exactly that, is widely supported, and has a polyfill for older browsers.
You can also use `Array#indexOf`, which is less direct, but doesn't require Polyfills for out of date browsers.
jQuery offers `$.inArray`, which is functionally equivalent to `Array#indexOf`.
underscore.js, a JavaScript utility library, offers `_.contains(list, value)`, alias `_.include(list, value)`, both of which use indexOf internally if passed a JavaScript array.
Some other frameworks offer similar methods:

Dojo Toolkit: `dojo.indexOf(array, value, [fromIndex, findLast])`
Prototype: `array.indexOf(value)`
MooTools: `array.indexOf(value)`
MochiKit: `findValue(array, value)`
MS Ajax: `array.indexOf(value)`
Ext: `Ext.Array.contains(array, value)`
Lodash: `_.includes(array, value, [from])` (is `_.contains` prior 4.0.0)
ECMAScript 2016: `array.includes(value)`

Notice that some frameworks implement this as a function, while others add the function to the array prototype.

## [How to validate an email address in JavaScript?](https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript)

**3117 Votes**, community-wiki

Using regular expressions is probably the best way. You can see a bunch of tests here (taken from chromium)

```javascript
function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
```

Here's the example of regular expresion that accepts unicode:

```javascript
var re = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
```

But keep in mind that one should not rely only upon JavaScript validation. JavaScript can  easily be disabled. This should be validated on the server side as well.
Here's an example of the above in action:



```javascript
function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function validate() {
  var $result = $("#result");
  var email = $("#email").val();
  $result.text("");

  if (validateEmail(email)) {
    $result.text(email + " is valid :)");
    $result.css("color", "green");
  } else {
    $result.text(email + " is not valid :(");
    $result.css("color", "red");
  }
  return false;
}

$("#validate").bind("click", validate);```


```javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

<form>
  <p>Enter an email address:</p>
  <input id='email'>
  <button type='submit' id='validate'>Validate!</button>
</form>

<h2 id='result'></h2>```

## [Create GUID / UUID in JavaScript?](https://stackoverflow.com/questions/105034/create-guid-uuid-in-javascript)

**3113 Votes**, community-wiki

There have been a couple attempts at this. The question is: do you want actual GUIDs, or just random numbers that look like GUIDs? It's easy enough to generate random numbers.

```javascript
function guid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}
```

However, note that such values are not genuine GUIDs.

There's no way to generate real GUIDs in Javascript, because they depend on properties of the local computer that browsers do not expose. You'll need to use OS-specific services like ActiveX: http://p2p.wrox.com/topicindex/20339.htm

Edit: not correct - RFC4122 allows random ("version 4") GUIDs.  See other answers for specifics.
Note: the provided code snippet does not follow RFC4122 which requires that the version (``4) has to be integrated into the generated output string. Do not use this answer if you need compliant GUIDs.
Use:

```javascript
var uuid = guid();
```

Demo:



```javascript
function guid() {
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}

function s4() {
  return Math.floor((1 + Math.random()) * 0x10000)
    .toString(16)
    .substring(1);
}

document.getElementById('jsGenId').addEventListener('click', function() {
  document.getElementById('jsIdResult').value = guid();
})```


```javascript
input { font-family: monospace; }```


```javascript
<button id="jsGenId" type="button">Generate GUID</button>
<br>
<input id="jsIdResult" type="text" placeholder="Results will be placed here..." readonly size="40"/>```

## [What's the difference between using let and var to declare a variable in JavaScript?](https://stackoverflow.com/questions/762011/whats-the-difference-between-using-let-and-var-to-declare-a-variable-in-jav)

**3070 Votes**, TM.

The difference is scoping. `var` is scoped to the nearest function block and `let` is scoped to the nearest enclosing block, which can be smaller than a function block. Both are global if outside any block.
Also, variables declared with `let` are not accessible before they are declared in their enclosing block. As seen in the demo, this will throw a ReferenceError exception.
Demo: 



```javascript
var html = '';

write('#### global ####\n');
write('globalVar: ' + globalVar); //undefined, but visible

try {
  write('globalLet: ' + globalLet); //undefined, *not* visible
} catch (exception) {
  write('globalLet: exception');
}

write('\nset variables');

var globalVar = 'globalVar';
let globalLet = 'globalLet';

write('\nglobalVar: ' + globalVar);
write('globalLet: ' + globalLet);

function functionScoped() {
  write('\n#### function ####');
  write('\nfunctionVar: ' + functionVar); //undefined, but visible

  try {
    write('functionLet: ' + functionLet); //undefined, *not* visible
  } catch (exception) {
    write('functionLet: exception');
  }

  write('\nset variables');

  var functionVar = 'functionVar';
  let functionLet = 'functionLet';

  write('\nfunctionVar: ' + functionVar);
  write('functionLet: ' + functionLet);
}

function blockScoped() {
  write('\n#### block ####');
  write('\nblockVar: ' + blockVar); //undefined, but visible

  try {
    write('blockLet: ' + blockLet); //undefined, *not* visible
  } catch (exception) {
    write('blockLet: exception');
  }

  for (var blockVar = 'blockVar', blockIndex = 0; blockIndex < 1; blockIndex++) {
    write('\nblockVar: ' + blockVar); // visible here and whole function
  };

  for (let blockLet = 'blockLet', letIndex = 0; letIndex < 1; letIndex++) {
    write('blockLet: ' + blockLet); // visible only here
  };

  write('\nblockVar: ' + blockVar);

  try {
    write('blockLet: ' + blockLet); //undefined, *not* visible
  } catch (exception) {
    write('blockLet: exception');
  }
}

function write(line) {
  html += (line ? line : '') + '<br />';
}

functionScoped();
blockScoped();

document.getElementById('results').innerHTML = html;```


```javascript
<pre id="results"></pre>```




Global:
They are very similar when used like this outside a function block.

```javascript
let me = 'go';  // globally scoped
var i = 'able'; // globally scoped
```

However, global variables defined with `let` will not be added as properties on the global `window` object like those defined with `var`.

```javascript
console.log(window.me); // undefined
console.log(window.i); // 'able'
```

Function:
They are identical when used like this in a function block.

```javascript
function ingWithinEstablishedParameters() {
    let terOfRecommendation = 'awesome worker!'; //function block scoped
    var sityCheerleading = 'go!'; //function block scoped
}
```

Block:
Here is the difference. `let` is only visible in the `for()` loop and `var` is visible to the whole function.

```javascript
function allyIlliterate() {
    //tuce is *not* visible out here

    for( let tuce = 0; tuce < 5; tuce++ ) {
        //tuce is only visible in here (and in the for() parentheses)
        //and there is a separate tuce variable for each iteration of the loop
    }

    //tuce is *not* visible out here
}

function byE40() {
    //nish *is* visible out here

    for( var nish = 0; nish < 5; nish++ ) {
        //nish is visible to the whole function
    }

    //nish *is* visible out here
}
```

Redeclaration:
Assuming strict mode, `var` will let you re-declare the same variable in the same scope. On the other hand, `let` will not:

```javascript
'use strict';
let me = 'foo';
let me = 'bar'; // SyntaxError: Identifier 'me' has already been declared
```


```javascript
'use strict';
var me = 'foo';
var me = 'bar'; // No problem, `me` is replaced.
```

## [How to replace all occurrences of a string in JavaScript?](https://stackoverflow.com/questions/1144783/how-to-replace-all-occurrences-of-a-string-in-javascript)

**3033 Votes**, Click Upvote

For the sake of completeness, I got to thinking about which method I should use to do this. There are basically two ways to do this as suggested by the other answers on this page.
Note: In general, extending the built-in prototypes in JavaScript is generally not recommended. I am providing as extensions on the String prototype simply for purposes of illustration, showing different implementations of a hypothetical standard method on the `String` built-in prototype.

Regular Expression Based Implementation

```javascript
String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};
```

Split and Join (Functional) Implementation

```javascript
String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};
```


Not knowing too much about how regular expressions work behind the scenes in terms of efficiency, I tended to lean toward the split and join implementation in the past without thinking about performance. When I did wonder which was more efficient, and by what margin, I used it as an excuse to find out.
On my Chrome Windows8 machine, the regular expression based implementation is the fastest, with the split and join implementation being 53% slower. Meaning the regular expressions are twice as fast for the lorem ipsum input I used.
Check out this benchmark running these two implementations against each other.

As noted in the comment below by @ThomasLeduc and others, there could be an issue with the regular expression-based implementation if `search` contains certain characters which are reserved as special characters in regular expressions. The implementation assumes that the caller will escape the string beforehand or will only pass strings that are without the characters in the table in Regular Expressions (MDN).
MDN also provides an implementation to escape our strings. It would be nice if this was also standardized as `RegExp.escape(str)`, but alas, it does not exist:

```javascript
function escapeRegExp(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); // $& means the whole matched string
}
```

We could call `escapeRegExp` within our `String.prototype.replaceAll` implementation, however, I'm not sure how much this will affect the performance (potentially even for strings for which the escape is not needed, like all alphanumeric strings).

## [How do I make the first letter of a string uppercase in JavaScript?](https://stackoverflow.com/questions/1026069/how-do-i-make-the-first-letter-of-a-string-uppercase-in-javascript)

**2859 Votes**, Robert Wills

```javascript
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}
```

Some other answers modify `String.prototype` (this answer used to as well), but I would advise against this now due to maintainability (hard to find out where the function is being added to the `prototype` and could cause conflicts if other code uses the same name / a browser adds a native function with that same name in future).

## [How to append something to an array?](https://stackoverflow.com/questions/351409/how-to-append-something-to-an-array)

**2798 Votes**, community-wiki

Use the `push()` function to append to an array:



```javascript
// initialize array
var arr = [
    "Hi",
    "Hello",
    "Bonjour"
];

// append new value to the array
arr.push("Hola");

console.log(arr);```




Will print

```javascript
["Hi", "Hello", "Bonjour", "Hola"]
```


You can use the `push()` function to append more than one value to an array in a single call:



```javascript
// initialize array
var arr = [ "Hi", "Hello", "Bonjour", "Hola" ];

// append multiple values to the array
arr.push("Salut", "Hey");

// display all values
for (var i = 0; i < arr.length; i++) {
    console.log(arr[i]);
}```




Will print

```javascript
Hi
Hello
Bonjour
Hola 
Salut
Hey
```


Update
If you want to add the items of one array to another array, you can use `firstArray.concat(secondArray)`:



```javascript
var arr = [
    "apple",
    "banana",
    "cherry"
];

arr = arr.concat([
    "dragonfruit",
    "elderberry",
    "fig"
]);

console.log(arr);```




Will print

```javascript
["apple", "banana", "cherry", "dragonfruit", "elderberry", "fig"]
```

## [How can I get query string values in JavaScript?](https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript)

**2703 Votes**, community-wiki

You don't need jQuery for that purpose. You can use just some pure JavaScript:

```javascript
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
```

Usage:

```javascript
// query string: ?foo=lorem&bar=&baz
var foo = getParameterByName('foo'); // "lorem"
var bar = getParameterByName('bar'); // "" (present with empty value)
var baz = getParameterByName('baz'); // "" (present with no value)
var qux = getParameterByName('qux'); // null (absent)
```


Note: If a parameter is present several times (`?foo=lorem&foo=ipsum`), you will get the first value (`lorem`). There is no standard about this and usages vary, see for example this question: Authoritative position of duplicate HTTP GET query keys.
NOTE: The function is case-sensitive. If you prefer case-insensitive parameter name, add 'i' modifier to RegExp

This is an update based on the new URLSearchParams specs to achieve the same result more succinctly. See answer titled "URLSearchParams" below.

## [What is the difference between call and apply?](https://stackoverflow.com/questions/1986896/what-is-the-difference-between-call-and-apply)

**2696 Votes**, John Duff

The difference is that `apply` lets you invoke the function with `arguments` as an array; `call` requires the parameters be listed explicitly. A useful mnemonic is "A for array and C for comma."
See MDN's documentation on apply and call.
Pseudo syntax:
`theFunction.apply(valueForThis, arrayOfArgs)`
`theFunction.call(valueForThis, arg1, arg2, ...)`
There is also, as of ES6, the possibility to `spread` the array for use with the `call` function, you can see the compatibilities here.
Sample code:



```javascript
function theFunction(name, profession) {
    console.log("My name is " + name + " and I am a " + profession +".");
}
theFunction("John", "fireman");
theFunction.apply(undefined, ["Susan", "school teacher"]);
theFunction.call(undefined, "Claude", "mathematician");
theFunction.call(undefined, ...["Matthew", "physicist"]); // used with the spread operator```

## [How do I copy to the clipboard in JavaScript?](https://stackoverflow.com/questions/400212/how-do-i-copy-to-the-clipboard-in-javascript)

**2608 Votes**, Santiago Corredoira

Overview
There are 3 primary browser APIs for copying to the clipboard:

Async Clipboard API `[navigator.clipboard.writeText]`

Text-focused portion available in Chrome 66 (March 2018)
Access is asynchronous and uses JavaScript Promises, can be written so security user prompts (if displayed) don't interrupt the JavaScript in page.
Text can be copied to the clipboard directly from a variable.
Only supported on pages served over HTTPS.
In Chrome 66 pages in active tabs can write to the clipboard without a permissions prompt.

`document.execCommand('copy')`

Most browsers support this as of ~April 2015 (see Browser Support below).
Access is synchronous, i.e. stops JavaScript in the page until complete including displaying and user interacting with any security prompts.
Text is read from the DOM and placed on the clipboard.
During testing ~April 2015 only Internet Explorer was noted as displaying permissions prompts whilst writing to the clipboard.

Overriding the copy event


See Clipboard API documentation on Overriding the copy event.
Allows you to modify what appear on the clipboard from any copy event, can include other formats of data other than plain text.
Not covered here as it doesn't directly answer the question.


General development notes
Don't expect clipboard related commands to work whilst you testing code in the console. Generally the page is required to be active (Async Clipboard API) or requires user interaction (e.g. a user click) to allow (`document.execCommand('copy')`) to access the clipboard see below for more detail.
Async + Fallback
Due to the level of browser support for the new Async Clipboard API you will likely want to fallback to the `document.execCommand('copy')` method to get good browser coverage.
Here is a simple example:



```javascript
function fallbackCopyTextToClipboard(text) {
  var textArea = document.createElement("textarea");
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Fallback: Copying text command was ' + msg);
  } catch (err) {
    console.error('Fallback: Oops, unable to copy', err);
  }

  document.body.removeChild(textArea);
}
function copyTextToClipboard(text) {
  if (!navigator.clipboard) {
    fallbackCopyTextToClipboard(text);
    return;
  }
  navigator.clipboard.writeText(text).then(function() {
    console.log('Async: Copying to clipboard was successful!');
  }, function(err) {
    console.error('Async: Could not copy text: ', err);
  });
}

var copyBobBtn = document.querySelector('.js-copy-bob-btn'),
  copyJaneBtn = document.querySelector('.js-copy-jane-btn');

copyBobBtn.addEventListener('click', function(event) {
  copyTextToClipboard('Bob');
});


copyJaneBtn.addEventListener('click', function(event) {
  copyTextToClipboard('Jane');
});```


```javascript
<div style="display:inline-block; vertical-align:top;">
  <button class="js-copy-bob-btn">Set clipboard to BOB</button><br /><br />
  <button class="js-copy-jane-btn">Set clipboard to JANE</button>
</div>
<div style="display:inline-block;">
  <textarea class="js-test-textarea" cols="35" rows="4">Try pasting into here to see what you have on your clipboard:
  
  </textarea>
</div>```




Note that this snippet is not working well in StackOverflow's embedded preview you can try it here:
https://codepen.io/DeanMarkTaylor/pen/RMRaJX?editors=1011
Async Clipboard API

Chrome 66 announcement post (March 2018)
Reference Async Clipboard API draft documentation

Note that there is an ability to "request permission" and test for access to the clipboard via the permissions API in Chrome 66.

```javascript
var text = "Example text to appear on clipboard";
navigator.clipboard.writeText(text).then(function() {
  console.log('Async: Copying to clipboard was successful!');
}, function(err) {
  console.error('Async: Could not copy text: ', err);
});
```

document.execCommand('copy')
The rest of this post goes into the nuances and detail of the `document.execCommand('copy')` API.

### Browser Support

The JavaScript `document.execCommand('copy')` support has grown, see the links below for browser updates:

IE10+ (although this document indicates some support was there from IE5.5+).
Google Chrome 43+ (~April 2015)
Mozilla Firefox 41+ (shipping ~September 2015)
Opera 29+ (based on Chromium 42, ~April 2015) 


### Simple Example




```javascript
var copyTextareaBtn = document.querySelector('.js-textareacopybtn');

copyTextareaBtn.addEventListener('click', function(event) {
  var copyTextarea = document.querySelector('.js-copytextarea');
  copyTextarea.focus();
  copyTextarea.select();

  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Copying text command was ' + msg);
  } catch (err) {
    console.log('Oops, unable to copy');
  }
});```


```javascript
<p>
  <button class="js-textareacopybtn" style="vertical-align:top;">Copy Textarea</button>
  <textarea class="js-copytextarea">Hello I'm some text</textarea>
</p>```





### Complex Example: Copy to clipboard without displaying input

The above simple example works great if there is a `textarea` or `input` element  visible on screen. 
In some cases you might wish to copy text to the clipboard without displaying an `input` / `textarea` element. This is one example of a way to work around this (basically insert element, copy to clipboard, remove element):
Tested with Google Chrome 44, Firefox 42.0a1 and IE 11.0.8600.17814.



```javascript
function copyTextToClipboard(text) {
  var textArea = document.createElement("textarea");

  //
  // *** This styling is an extra step which is likely not required. ***
  //
  // Why is it here? To ensure:
  // 1. the element is able to have focus and selection.
  // 2. if element was to flash render it has minimal visual impact.
  // 3. less flakyness with selection and copying which **might** occur if
  //    the textarea element is not visible.
  //
  // The likelihood is the element won't even render, not even a flash,
  // so some of these are just precautions. However in IE the element
  // is visible whilst the popup box asking the user for permission for
  // the web page to copy to the clipboard.
  //

  // Place in top-left corner of screen regardless of scroll position.
  textArea.style.position = 'fixed';
  textArea.style.top = 0;
  textArea.style.left = 0;

  // Ensure it has a small width and height. Setting to 1px / 1em
  // doesn't work as this gives a negative w/h on some browsers.
  textArea.style.width = '2em';
  textArea.style.height = '2em';

  // We don't need padding, reducing the size if it does flash render.
  textArea.style.padding = 0;

  // Clean up any borders.
  textArea.style.border = 'none';
  textArea.style.outline = 'none';
  textArea.style.boxShadow = 'none';

  // Avoid flash of white box if rendered for any reason.
  textArea.style.background = 'transparent';


  textArea.value = text;

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Copying text command was ' + msg);
  } catch (err) {
    console.log('Oops, unable to copy');
  }

  document.body.removeChild(textArea);
}


var copyBobBtn = document.querySelector('.js-copy-bob-btn'),
  copyJaneBtn = document.querySelector('.js-copy-jane-btn');

copyBobBtn.addEventListener('click', function(event) {
  copyTextToClipboard('Bob');
});


copyJaneBtn.addEventListener('click', function(event) {
  copyTextToClipboard('Jane');
});```


```javascript
<div style="display:inline-block; vertical-align:top;">
  <button class="js-copy-bob-btn">Set clipboard to BOB</button><br /><br />
  <button class="js-copy-jane-btn">Set clipboard to JANE</button>
</div>
<div style="display:inline-block;">
  <textarea class="js-test-textarea" cols="35" rows="4">Try pasting into here to see what you have on your clipboard:
  
  </textarea>
</div>```





### Additional notes

Only works if the user takes an action
All `document.execCommand('copy')` calls must take place as a direct result of a user action, e.g. click event handler. This is a measure to prevent messing with the users clipboard when they don't expect it.
See the Google Developers post here for more info.
Clipboard API
Note the full Clipboard API draft specification can be found here:
https://w3c.github.io/clipboard-apis/
Is it supported?

`document.queryCommandSupported('copy')` should return `true` if the command "is supported by the browser".
and `document.queryCommandEnabled('copy')` return `true` if the `document.execCommand('copy')` will succeed if called now. Checking to ensure the command was called from a user-initiated thread and other requirements are met.

However as an example of browser compatibility issues, Google Chrome from ~April to ~October 2015 only returned `true` from `document.queryCommandSupported('copy')` if the command was called from a user-initiated thread.
Note compatibility detail below.
Browser Compatibility Detail
Whilst a simple call to `document.execCommand('copy')` wrapped in a `try`/`catch` block called as a result of a user click will get you the most compatibility use the following has some provisos:
Any call to `document.execCommand`, `document.queryCommandSupported` or `document.queryCommandEnabled` should be wrapped in a `try`/`catch` block.
Different browser implementations and browser versions throw differing types of exceptions when called instead of returning `false`.
Different browser implementations are still in flux and the Clipboard API is still in draft, so remember to do your testing.

## [event.preventDefault() vs. return false](https://stackoverflow.com/questions/1357118/event-preventdefault-vs-return-false)

**2605 Votes**, RaYell

`return false` from within a jQuery event handler is effectively the same as calling both  `e.preventDefault` and `e.stopPropagation` on the passed jQuery.Event object.
`e.preventDefault()` will prevent the default event from occuring, `e.stopPropagation()` will prevent the event from bubbling up and `return false` will do both. Note that this behaviour differs from normal (non-jQuery) event handlers, in which, notably, `return false` does not stop the event from bubbling up.
Source: John Resig
Any benefit to using event.preventDefault() over "return false" to cancel out an href click?

## [How can I upload files asynchronously?](https://stackoverflow.com/questions/166221/how-can-i-upload-files-asynchronously)

**2568 Votes**, Sergio del Amo

With HTML5 you can make file uploads with Ajax and jQuery. Not only that, you can do file validations (name, size, and MIME type) or handle the progress event with the HTML5 progress tag (or a div). Recently I had to make a file uploader, but I didn't want to use Flash nor Iframes or plugins and after some research I came up with the solution.
The HTML:

```javascript
<form enctype="multipart/form-data">
    <input name="file" type="file" />
    <input type="button" value="Upload" />
</form>
<progress></progress>
```

First, you can do some validation if you want. For example, in the onChange event of the file:

```javascript
$(':file').on('change', function() {
    var file = this.files[0];
    if (file.size > 1024) {
        alert('max upload size is 1k')
    }

    // Also see .name, .type
});
```

Now the Ajax submit with the button's click:

```javascript
$(':button').on('click', function() {
    $.ajax({
        // Your server script to process the upload
        url: 'upload.php',
        type: 'POST',

        // Form data
        data: new FormData($('form')[0]),

        // Tell jQuery not to process data or worry about content-type
        // You *must* include these options!
        cache: false,
        contentType: false,
        processData: false,

        // Custom XMLHttpRequest
        xhr: function() {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                // For handling the progress of the upload
                myXhr.upload.addEventListener('progress', function(e) {
                    if (e.lengthComputable) {
                        $('progress').attr({
                            value: e.loaded,
                            max: e.total,
                        });
                    }
                } , false);
            }
            return myXhr;
        }
    });
});
```

As you can see, with HTML5 (and some research) file uploading not only becomes possible but super easy. Try it with Google Chrome as some of the HTML5 components of the examples aren't available in every browser.

## [Get the current URL with JavaScript?](https://stackoverflow.com/questions/1034621/get-the-current-url-with-javascript)

**2470 Votes**, 
        dougoftheabaci
        



Use:

```javascript
window.location.href 
```

As noted in the comments, the line below works, but it is bugged for Firefox.

```javascript
document.URL;
```

See URL of type DOMString, readonly.

## [Detecting an undefined object property](https://stackoverflow.com/questions/27509/detecting-an-undefined-object-property)

**2396 Votes**, Matt Sheppard

Use:

```javascript
if (typeof something === "undefined") {
    alert("something is undefined");
}
```

If an object variable which have some properties you can use same thing like this:

```javascript
if (typeof my_obj.someproperties === "undefined"){
    console.log('the property is not available...'); // print into console
}
```

## [Is it possible to apply CSS to half of a character?](https://stackoverflow.com/questions/23569441/is-it-possible-to-apply-css-to-half-of-a-character)

**2385 Votes**, Mathew MacLean

Now on GitHub as a Plugin!
 Feel free to fork and improve.
Demo | Download Zip | Half-Style.com (Redirects to GitHub)


Pure CSS for a Single Character
JavaScript used for automation across text or multiple characters
Preserves Text Accessibility for screen readers for the blind or visually
impaired

Part 1: Basic Solution

Demo: http://jsfiddle.net/arbel/pd9yB/1694/

This works on any dynamic text, or a single character, and is all automated. All you need to do is add a class on the target text and the rest is taken care of.
Also, the accessibility of the original text is preserved for screen readers for the blind or visually impaired.
Explanation for a single character:
Pure CSS. All you need to do is to apply `.halfStyle` class to each element that contains the character you want to be half-styled.
For each span element containing the character, you can create a data attribute, for example here `data-content="X"`, and on the pseudo element use `content: attr(data-content);` so the `.halfStyle:before` class will be dynamic and you won't need to hard code it for every instance.
Explanation for any text:
Simply add `textToHalfStyle` class to the element containing the text.




```javascript
// jQuery for automated mode
jQuery(function($) {
    var text, chars, $el, i, output;

    // Iterate over all class occurences
    $('.textToHalfStyle').each(function(idx, el) {
    $el = $(el);
    text = $el.text();
    chars = text.split('');

    // Set the screen-reader text
    $el.html('<span style="position: absolute !important;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);">' + text + '</span>');

    // Reset output for appending
    output = '';

    // Iterate over all chars in the text
    for (i = 0; i < chars.length; i++) {
        // Create a styled element for each character and append to container
        output += '<span aria-hidden="true" class="halfStyle" data-content="' + chars[i] + '">' + chars[i] + '</span>';
    }

    // Write to DOM only once
    $el.append(output);
  });
});```


```javascript
.halfStyle {
    position: relative;
    display: inline-block;
    font-size: 80px; /* or any font size will work */
    color: black; /* or transparent, any color */
    overflow: hidden;
    white-space: pre; /* to preserve the spaces from collapsing */
}

.halfStyle:before {
    display: block;
    z-index: 1;
    position: absolute;
    top: 0;
    left: 0;
    width: 50%;
    content: attr(data-content); /* dynamic content for the pseudo element */
    overflow: hidden;
    color: #f00;
}```


```javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

<p>Single Characters:</p>
<span class="halfStyle" data-content="X">X</span>
<span class="halfStyle" data-content="Y">Y</span>
<span class="halfStyle" data-content="Z">Z</span>
<span class="halfStyle" data-content="A">A</span>

<hr/>
<p>Automated:</p>

<span class="textToHalfStyle">Half-style, please.</span>```




(JSFiddle demo)

Part 2: Advanced solution - Independent left and right parts

With this solution you can style left and right parts, individually and independently.
Everything is the same, only more advanced CSS does the magic.



```javascript
jQuery(function($) {
    var text, chars, $el, i, output;

    // Iterate over all class occurences
    $('.textToHalfStyle').each(function(idx, el) {
        $el = $(el);
        text = $el.text();
        chars = text.split('');

        // Set the screen-reader text
        $el.html('<span style="position: absolute !important;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);">' + text + '</span>');

        // Reset output for appending
        output = '';

        // Iterate over all chars in the text
        for (i = 0; i < chars.length; i++) {
            // Create a styled element for each character and append to container
            output += '<span aria-hidden="true" class="halfStyle" data-content="' + chars[i] + '">' + chars[i] + '</span>';
        }

        // Write to DOM only once
        $el.append(output);
    });
});```


```javascript
.halfStyle {
    position: relative;
    display: inline-block;
    font-size: 80px; /* or any font size will work */
    color: transparent; /* hide the base character */
    overflow: hidden;
    white-space: pre; /* to preserve the spaces from collapsing */
}

.halfStyle:before { /* creates the left part */
    display: block;
    z-index: 1;
    position: absolute;
    top: 0;
    width: 50%;
    content: attr(data-content); /* dynamic content for the pseudo element */
    overflow: hidden;
    pointer-events: none; /* so the base char is selectable by mouse */
    color: #f00; /* for demo purposes */
    text-shadow: 2px -2px 0px #af0; /* for demo purposes */
}

.halfStyle:after { /* creates the right part */
    display: block;
    direction: rtl; /* very important, will make the width to start from right */
    position: absolute;
    z-index: 2;
    top: 0;
    left: 50%;
    width: 50%;
    content: attr(data-content); /* dynamic content for the pseudo element */
    overflow: hidden;
    pointer-events: none; /* so the base char is selectable by mouse */
    color: #000; /* for demo purposes */
    text-shadow: 2px 2px 0px #0af; /* for demo purposes */
}```


```javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<p>Single Characters:</p>
<span class="halfStyle" data-content="X">X</span>
<span class="halfStyle" data-content="Y">Y</span>
<span class="halfStyle" data-content="Z">Z</span>
<span class="halfStyle" data-content="A">A</span>

<hr/>
<p>Automated:</p>

<span class="textToHalfStyle">Half-style, please.</span>```




(JSFiddle demo)


Part 3: Mix-Match and Improve
Now that we know what is possible, let's create some variations.


### -Horizontal Half Parts





```javascript
// jQuery for automated mode
jQuery(function($) {
    var text, chars, $el, i, output;

    // Iterate over all class occurences
    $('.textToHalfStyle').each(function(idx, el) {
        $el = $(el);
        text = $el.text();
        chars = text.split('');

        // Set the screen-reader text
        $el.html('<span style="position: absolute !important;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);">' + text + '</span>');

        // Reset output for appending
        output = '';

        // Iterate over all chars in the text
        for (i = 0; i < chars.length; i++) {
            // Create a styled element for each character and append to container
            output += '<span aria-hidden="true" class="halfStyle" data-content="' + chars[i] + '">' + chars[i] + '</span>';
        }

        // Write to DOM only once
        $el.append(output);
    });
});```


```javascript
.halfStyle {
  position: relative;
  display: inline-block;
  font-size: 80px; /* or any font size will work */
  color: transparent; /* hide the base character */
  overflow: hidden;
  white-space: pre; /* to preserve the spaces from collapsing */
}

.halfStyle:before { /* creates the top part */
  display: block;
  z-index: 2;
  position: absolute;
  top: 0;
  height: 50%;
  content: attr(data-content); /* dynamic content for the pseudo element */
  overflow: hidden;
  pointer-events: none; /* so the base char is selectable by mouse */
  color: #f00; /* for demo purposes */
  text-shadow: 2px -2px 0px #af0; /* for demo purposes */
}

.halfStyle:after { /* creates the bottom part */
  display: block;
  position: absolute;
  z-index: 1;
  top: 0;
  height: 100%;
  content: attr(data-content); /* dynamic content for the pseudo element */
  overflow: hidden;
  pointer-events: none; /* so the base char is selectable by mouse */
  color: #000; /* for demo purposes */
  text-shadow: 2px 2px 0px #0af; /* for demo purposes */
}```


```javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<p>Single Characters:</p>
<span class="halfStyle" data-content="X">X</span>
<span class="halfStyle" data-content="Y">Y</span>
<span class="halfStyle" data-content="Z">Z</span>
<span class="halfStyle" data-content="A">A</span>

<hr/>
<p>Automated:</p>

<span class="textToHalfStyle">Half-style, please.</span>```




(JSFiddle demo)



### -Vertical 1/3 Parts





```javascript
// jQuery for automated mode
jQuery(function($) {
    var text, chars, $el, i, output;

    // Iterate over all class occurences
    $('.textToHalfStyle').each(function(idx, el) {
    $el = $(el);
    text = $el.text();
    chars = text.split('');

    // Set the screen-reader text
    $el.html('<span style="position: absolute !important;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);">' + text + '</span>');

    // Reset output for appending
    output = '';

    // Iterate over all chars in the text
    for (i = 0; i < chars.length; i++) {
        // Create a styled element for each character and append to container
        output += '<span aria-hidden="true" class="halfStyle" data-content="' + chars[i] + '">' + chars[i] + '</span>';
    }

    // Write to DOM only once
    $el.append(output);
  });
});```


```javascript
.halfStyle { /* base char and also the right 1/3 */
    position: relative;
    display: inline-block;
    font-size: 80px; /* or any font size will work */
    color: transparent; /* hide the base character */
    overflow: hidden;
    white-space: pre; /* to preserve the spaces from collapsing */
    color: #f0f; /* for demo purposes */
    text-shadow: 2px 2px 0px #0af; /* for demo purposes */
}

.halfStyle:before { /* creates the left 1/3 */
    display: block;
    z-index: 2;
    position: absolute;
    top: 0;
    width: 33.33%;
    content: attr(data-content); /* dynamic content for the pseudo element */
    overflow: hidden;
    pointer-events: none; /* so the base char is selectable by mouse */
    color: #f00; /* for demo purposes */
    text-shadow: 2px -2px 0px #af0; /* for demo purposes */
}

.halfStyle:after { /* creates the middle 1/3 */
    display: block;
    z-index: 1;
    position: absolute;
    top: 0;
    width: 66.66%;
    content: attr(data-content); /* dynamic content for the pseudo element */
    overflow: hidden;
    pointer-events: none; /* so the base char is selectable by mouse */
    color: #000; /* for demo purposes */
    text-shadow: 2px 2px 0px #af0; /* for demo purposes */
}```


```javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

<p>Single Characters:</p>
<span class="halfStyle" data-content="X">X</span>
<span class="halfStyle" data-content="Y">Y</span>
<span class="halfStyle" data-content="Z">Z</span>
<span class="halfStyle" data-content="A">A</span>

<hr/>
<p>Automated:</p>

<span class="textToHalfStyle">Half-style, please.</span>```




(JSFiddle demo)



### -Horizontal 1/3 Parts





```javascript
// jQuery for automated mode
jQuery(function($) {
    var text, chars, $el, i, output;

    // Iterate over all class occurences
    $('.textToHalfStyle').each(function(idx, el) {
    $el = $(el);
    text = $el.text();
    chars = text.split('');

    // Set the screen-reader text
    $el.html('<span style="position: absolute !important;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);">' + text + '</span>');

    // Reset output for appending
    output = '';

    // Iterate over all chars in the text
    for (i = 0; i < chars.length; i++) {
        // Create a styled element for each character and append to container
        output += '<span aria-hidden="true" class="halfStyle" data-content="' + chars[i] + '">' + chars[i] + '</span>';
    }

    // Write to DOM only once
    $el.append(output);
  });
});```


```javascript
.halfStyle { /* base char and also the bottom 1/3 */
  position: relative;
  display: inline-block;
  font-size: 80px; /* or any font size will work */
  color: transparent;
  overflow: hidden;
  white-space: pre; /* to preserve the spaces from collapsing */
  color: #f0f;
  text-shadow: 2px 2px 0px #0af; /* for demo purposes */
}

.halfStyle:before { /* creates the top 1/3 */
  display: block;
  z-index: 2;
  position: absolute;
  top: 0;
  height: 33.33%;
  content: attr(data-content); /* dynamic content for the pseudo element */
  overflow: hidden;
  pointer-events: none; /* so the base char is selectable by mouse */
  color: #f00; /* for demo purposes */
  text-shadow: 2px -2px 0px #fa0; /* for demo purposes */
}

.halfStyle:after { /* creates the middle 1/3 */
  display: block;
  position: absolute;
  z-index: 1;
  top: 0;
  height: 66.66%;
  content: attr(data-content); /* dynamic content for the pseudo element */
  overflow: hidden;
  pointer-events: none; /* so the base char is selectable by mouse */
  color: #000; /* for demo purposes */
  text-shadow: 2px 2px 0px #af0; /* for demo purposes */
}```


```javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<p>Single Characters:</p>
<span class="halfStyle" data-content="X">X</span>
<span class="halfStyle" data-content="Y">Y</span>
<span class="halfStyle" data-content="Z">Z</span>
<span class="halfStyle" data-content="A">A</span>

<hr/>
<p>Automated:</p>

<span class="textToHalfStyle">Half-style, please.</span>```




(JSFiddle demo)



### -HalfStyle Improvement By @KevinGranger





```javascript
// jQuery for automated mode
jQuery(function($) {
    var text, chars, $el, i, output;

    // Iterate over all class occurences
    $('.textToHalfStyle').each(function(idx, el) {
    $el = $(el);
    text = $el.text();
    chars = text.split('');

    // Set the screen-reader text
    $el.html('<span style="position: absolute !important;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);">' + text + '</span>');

    // Reset output for appending
    output = '';

    // Iterate over all chars in the text
    for (i = 0; i < chars.length; i++) {
        // Create a styled element for each character and append to container
        output += '<span aria-hidden="true" class="halfStyle" data-content="' + chars[i] + '">' + chars[i] + '</span>';
    }

    // Write to DOM only once
    $el.append(output);
  });
});```


```javascript
body {
    background-color: black;
}

.textToHalfStyle {
    display: block;
    margin: 200px 0 0 0;
    text-align: center;
}

.halfStyle {
    font-family: 'Libre Baskerville', serif;
    position: relative;
    display: inline-block;
    width: 1;
    font-size: 70px;
    color: black;
    overflow: hidden;
    white-space: pre;
    text-shadow: 1px 2px 0 white;
}

.halfStyle:before {
    display: block;
    z-index: 1;
    position: absolute;
    top: 0;
    width: 50%;
    content: attr(data-content); /* dynamic content for the pseudo element */
    overflow: hidden;
    color: white;
}```


```javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<p>Single Characters:</p>
<span class="halfStyle" data-content="X">X</span>
<span class="halfStyle" data-content="Y">Y</span>
<span class="halfStyle" data-content="Z">Z</span>
<span class="halfStyle" data-content="A">A</span>

<hr/>
<p>Automated:</p>

<span class="textToHalfStyle">Half-style, please.</span>```




(JSFiddle demo)



### -PeelingStyle improvement of HalfStyle by @SamTremaine





```javascript
// jQuery for automated mode
jQuery(function($) {
    var text, chars, $el, i, output;

    // Iterate over all class occurences
    $('.textToHalfStyle').each(function(idx, el) {
    $el = $(el);
    text = $el.text();
    chars = text.split('');

    // Set the screen-reader text
    $el.html('<span style="position: absolute !important;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);">' + text + '</span>');

    // Reset output for appending
    output = '';

    // Iterate over all chars in the text
    for (i = 0; i < chars.length; i++) {
        // Create a styled element for each character and append to container
        output += '<span aria-hidden="true" class="halfStyle" data-content="' + chars[i] + '">' + chars[i] + '</span>';
    }

    // Write to DOM only once
    $el.append(output);
  });
});```


```javascript
.halfStyle {
    position: relative;
    display: inline-block;
    font-size: 68px;
    color: rgba(0, 0, 0, 0.8);
    overflow: hidden;
    white-space: pre;
    transform: rotate(4deg);
    text-shadow: 2px 1px 3px rgba(0, 0, 0, 0.3);
}

.halfStyle:before { /* creates the left part */
    display: block;
    z-index: 1;
    position: absolute;
    top: -0.5px;
    left: -3px;
    width: 100%;
    content: attr(data-content);
    overflow: hidden;
    pointer-events: none;
    color: #FFF;
    transform: rotate(-4deg);
    text-shadow: 0px 0px 1px #000;
}```


```javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<p>Single Characters:</p>
<span class="halfStyle" data-content="X">X</span>
<span class="halfStyle" data-content="Y">Y</span>
<span class="halfStyle" data-content="Z">Z</span>
<span class="halfStyle" data-content="A">A</span>

<hr/>
<p>Automated:</p>

<span class="textToHalfStyle">Half-style, please.</span>```




(JSFiddle demo and on samtremaine.co.uk)


Part 4: Ready for Production
Customized different Half-Style style-sets can be used on desired elements on the same page.
You can define multiple style-sets and tell the plugin which one to use.
The plugin uses data attribute `data-halfstyle="[-CustomClassName-]"` on the target `.textToHalfStyle` elements and makes all the necessary changes automatically.
So, simply on the element containing the text add `textToHalfStyle` class and data attribute `data-halfstyle="[-CustomClassName-]"`. The plugin will do the rest of the job.

Also the CSS style-sets' class definitions match the `[-CustomClassName-]` part mentioned above and is chained to `.halfStyle`, so we will have `.halfStyle.[-CustomClassName-]`



```javascript
jQuery(function($) {
    var halfstyle_text, halfstyle_chars, $halfstyle_el, halfstyle_i, halfstyle_output, halfstyle_style;

    // Iterate over all class occurrences
    $('.textToHalfStyle').each(function(idx, halfstyle_el) {
        $halfstyle_el = $(halfstyle_el);
        halfstyle_style = $halfstyle_el.data('halfstyle') || 'hs-base';
        halfstyle_text = $halfstyle_el.text();
        halfstyle_chars = halfstyle_text.split('');

        // Set the screen-reader text
        $halfstyle_el.html('<span style="position: absolute !important;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);">' + halfstyle_text + '</span>');

        // Reset output for appending
        halfstyle_output = '';

        // Iterate over all chars in the text
        for (halfstyle_i = 0; halfstyle_i < halfstyle_chars.length; halfstyle_i++) {
            // Create a styled element for each character and append to container
            halfstyle_output += '<span aria-hidden="true" class="halfStyle ' + halfstyle_style + '" data-content="' + halfstyle_chars[halfstyle_i] + '">' + halfstyle_chars[halfstyle_i] + '</span>';
        }

        // Write to DOM only once
        $halfstyle_el.append(halfstyle_output);
    });
});```


```javascript
/* start half-style hs-base */

.halfStyle.hs-base {
    position: relative;
    display: inline-block;
    font-size: 80px; /* or any font size will work */
    overflow: hidden;
    white-space: pre; /* to preserve the spaces from collapsing */
    color: #000; /* for demo purposes */
}

.halfStyle.hs-base:before {
    display: block;
    z-index: 1;
    position: absolute;
    top: 0;
    width: 50%;
    content: attr(data-content); /* dynamic content for the pseudo element */
    pointer-events: none; /* so the base char is selectable by mouse */
    overflow: hidden;
    color: #f00; /* for demo purposes */
}

/* end half-style hs-base */


/* start half-style hs-horizontal-third */

.halfStyle.hs-horizontal-third { /* base char and also the bottom 1/3 */
    position: relative;
    display: inline-block;
    font-size: 80px; /* or any font size will work */
    color: transparent;
    overflow: hidden;
    white-space: pre; /* to preserve the spaces from collapsing */
    color: #f0f;
    text-shadow: 2px 2px 0px #0af; /* for demo purposes */
}

.halfStyle.hs-horizontal-third:before { /* creates the top 1/3 */
    display: block;
    z-index: 2;
    position: absolute;
    top: 0;
    height: 33.33%;
    content: attr(data-content); /* dynamic content for the pseudo element */
    overflow: hidden;
    pointer-events: none; /* so the base char is selectable by mouse */
    color: #f00; /* for demo purposes */
    text-shadow: 2px -2px 0px #fa0; /* for demo purposes */
}

.halfStyle.hs-horizontal-third:after { /* creates the middle 1/3 */
    display: block;
    position: absolute;
    z-index: 1;
    top: 0;
    height: 66.66%;
    content: attr(data-content); /* dynamic content for the pseudo element */
    overflow: hidden;
    pointer-events: none; /* so the base char is selectable by mouse */
    color: #000; /* for demo purposes */
    text-shadow: 2px 2px 0px #af0; /* for demo purposes */
}

/* end half-style hs-horizontal-third */


/* start half-style hs-PeelingStyle, by user SamTremaine on Stackoverflow.com */

.halfStyle.hs-PeelingStyle {
  position: relative;
  display: inline-block;
  font-size: 68px;
  color: rgba(0, 0, 0, 0.8);
  overflow: hidden;
  white-space: pre;
  transform: rotate(4deg);
  text-shadow: 2px 1px 3px rgba(0, 0, 0, 0.3);
}

.halfStyle.hs-PeelingStyle:before { /* creates the left part */
  display: block;
  z-index: 1;
  position: absolute;
  top: -0.5px;
  left: -3px;
  width: 100%;
  content: attr(data-content);
  overflow: hidden;
  pointer-events: none;
  color: #FFF;
  transform: rotate(-4deg);
  text-shadow: 0px 0px 1px #000;
}

/* end half-style hs-PeelingStyle */


/* start half-style hs-KevinGranger, by user KevinGranger on StackOverflow.com*/

.textToHalfStyle.hs-KevinGranger {
  display: block;
  margin: 200px 0 0 0;
  text-align: center;
}

.halfStyle.hs-KevinGranger {
  font-family: 'Libre Baskerville', serif;
  position: relative;
  display: inline-block;
  width: 1;
  font-size: 70px;
  color: black;
  overflow: hidden;
  white-space: pre;
  text-shadow: 1px 2px 0 white;
}

.halfStyle.hs-KevinGranger:before {
  display: block;
  z-index: 1;
  position: absolute;
  top: 0;
  width: 50%;
  content: attr(data-content); /* dynamic content for the pseudo element */
  overflow: hidden;
  color: white;
}

/* end half-style hs-KevinGranger```


```javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<p>
    <span class="textToHalfStyle" data-halfstyle="hs-base">Half-style, please.</span>
</p>
<p>
    <span class="textToHalfStyle" data-halfstyle="hs-horizontal-third">Half-style, please.</span>
</p>
<p>
    <span class="textToHalfStyle" data-halfstyle="hs-PeelingStyle">Half-style, please.</span>
</p>
<p style="background-color:#000;">
    <span class="textToHalfStyle" data-halfstyle="hs-KevinGranger">Half-style, please.</span>
</p>```




(JSFiddle demo)

## [Loop through an array in JavaScript](https://stackoverflow.com/questions/3010840/loop-through-an-array-in-javascript)

**2337 Votes**, Mark Szymanski

Use a sequential `for` loop:

```javascript
var myStringArray = ["Hello","World"];
var arrayLength = myStringArray.length;
for (var i = 0; i < arrayLength; i++) {
    alert(myStringArray[i]);
    //Do something
}
```

@zipcodeman suggests the use of the `for...in` statement, but for iterating arrays `for-in` should be avoided, that statement is meant to enumerate object properties.
It shouldn't be used for array-like objects because:

The order of iteration is not guaranteed, the array indexes may not be visited in numeric order.
Inherited properties are also enumerated.

The second point is that it can give you a lot of problems, for example, if you extend the `Array.prototype` object to include a method there, that property will be also enumerated.
For example:

```javascript
Array.prototype.foo = "foo!";
var array = ['a', 'b', 'c'];

for (var i in array) {
  alert(array[i]);
}
```

The above code will alert, "a", "b", "c" and "foo!".
That be particularly a problem if you use some library that relies heavily on native prototypes augmention (such as MooTools for example).
The `for-in` statement as I said before is there to enumerate object properties, for example:

```javascript
var obj = {
  "a": 1,
  "b": 2,
  "c": 3
};

for (var prop in obj) {
  if (obj.hasOwnProperty(prop)) { 
  // or if (Object.prototype.hasOwnProperty.call(obj,prop)) for safety...
    alert("prop: " + prop + " value: " + obj[prop])
  }
}
```

In the above example the `hasOwnProperty` method allows you to enumerate only own properties, that's it, only the properties that the object physically has, no inherited properties.
I would recommend you to read the following article:

Enumeration VS Iteration

## [How do I correctly clone a JavaScript object?](https://stackoverflow.com/questions/728360/how-do-i-correctly-clone-a-javascript-object)

**2312 Votes**, community-wiki

Updated answer
Just use Object.assign() as suggested here

Outdated answer
To do this for any object in JavaScript will not be simple or straightforward. You will run into the problem of erroneously picking up attributes from the object's prototype that should be left in the prototype and not copied to the new instance. If, for instance, you are adding a `clone` method to `Object.prototype`, as some answers depict, you will need to explicitly skip that attribute. But what if there are other additional methods added to `Object.prototype`, or other intermediate prototypes, that you don't know about? In that case, you will copy attributes you shouldn't, so you need to detect unforeseen, non-local attributes with the `hasOwnProperty` method.
In addition to non-enumerable attributes, you'll encounter a tougher problem when you try to copy objects that have hidden properties. For example, `prototype` is a hidden property of a function. Also, an object's prototype is referenced with the attribute `__proto__`, which is also hidden, and will not be copied by a for/in loop iterating over the source object's attributes. I think `__proto__` might be specific to Firefox's JavaScript interpreter and it may be something different in other browsers, but you get the picture. Not everything is enumerable. You can copy a hidden attribute if you know its name, but I don't know of any way to discover it automatically.
Yet another snag in the quest for an elegant solution is the problem of setting up the prototype inheritance correctly. If your source object's prototype is `Object`, then simply creating a new general object with `{}` will work, but if the source's prototype is some descendant of `Object`, then you are going to be missing the additional members from that prototype which you skipped using the `hasOwnProperty` filter, or which were in the prototype, but weren't enumerable in the first place. One solution might be to call the source object's `constructor` property to get the initial copy object and then copy over the attributes, but then you still will not get non-enumerable attributes. For example, a `Date` object stores its data as a hidden member:

```javascript
function clone(obj) {
    if (null == obj || "object" != typeof obj) return obj;
    var copy = obj.constructor();
    for (var attr in obj) {
        if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
    }
    return copy;
}

var d1 = new Date();

/* Executes function after 5 seconds. */
setTimeout(function(){
    var d2 = clone(d1);
    alert("d1 = " + d1.toString() + "\nd2 = " + d2.toString());
}, 5000);
```

The date string for `d1` will be 5 seconds behind that of `d2`. A way to make one `Date` the same as another is by calling the `setTime` method, but that is specific to the `Date` class. I don't think there is a bullet-proof general solution to this problem, though I would be happy to be wrong!
When I had to implement general deep copying I ended up compromising by assuming that I would only need to copy a plain `Object`, `Array`, `Date`, `String`, `Number`, or `Boolean`. The last 3 types are immutable, so I could perform a shallow copy and not worry about it changing. I further assumed that any elements contained in `Object` or `Array` would also be one of the 6 simple types in that list. This can be accomplished with code like the following:

```javascript
function clone(obj) {
    var copy;

    // Handle the 3 simple types, and null or undefined
    if (null == obj || "object" != typeof obj) return obj;

    // Handle Date
    if (obj instanceof Date) {
        copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
        copy = [];
        for (var i = 0, len = obj.length; i < len; i++) {
            copy[i] = clone(obj[i]);
        }
        return copy;
    }

    // Handle Object
    if (obj instanceof Object) {
        copy = {};
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy[attr] = clone(obj[attr]);
        }
        return copy;
    }

    throw new Error("Unable to copy obj! Its type isn't supported.");
}
```

The above function will work adequately for the 6 simple types I mentioned, as long as the data in the objects and arrays form a tree structure. That is, there isn't more than one reference to the same data in the object. For example:

```javascript
// This would be cloneable:
var tree = {
    "left"  : { "left" : null, "right" : null, "data" : 3 },
    "right" : null,
    "data"  : 8
};

// This would kind-of work, but you would get 2 copies of the 
// inner node instead of 2 references to the same copy
var directedAcylicGraph = {
    "left"  : { "left" : null, "right" : null, "data" : 3 },
    "data"  : 8
};
directedAcyclicGraph["right"] = directedAcyclicGraph["left"];

// Cloning this would cause a stack overflow due to infinite recursion:
var cyclicGraph = {
    "left"  : { "left" : null, "right" : null, "data" : 3 },
    "data"  : 8
};
cyclicGraph["right"] = cyclicGraph;
```

It will not be able to handle any JavaScript object, but it may be sufficient for many purposes as long as you don't assume that it will just work for anything you throw at it.

## [Is there an exists function for jQuery?](https://stackoverflow.com/questions/31044/is-there-an-exists-function-for-jquery)

**2270 Votes**, Jake McGraw

In JavaScript, everything is 'truthy' or 'falsy', and for numbers ``0 (and NaN) means `false`, everything else `true`. So you could write:

```javascript
if ($(selector).length)
```

You don't need that `>0` part.

## [JavaScript closure inside loops  simple practical example](https://stackoverflow.com/questions/750486/javascript-closure-inside-loops-simple-practical-example)

**2247 Votes**, nickf

Well, the problem is that the variable ``i, within each of your anonymous functions, is bound to the same variable outside of the function.
What you want to do is bind the variable within each function to a separate, unchanging value outside of the function:



```javascript
var funcs = [];

function createfunc(i) {
    return function() { console.log("My value: " + i); };
}

for (var i = 0; i < 3; i++) {
    funcs[i] = createfunc(i);
}

for (var j = 0; j < 3; j++) {
    funcs[j]();                        // and now let's run each one to see
}```




Since there is no block scope in JavaScript - only function scope - by wrapping the function creation in a new function, you ensure that the value of "i" remains as you intended.

Update: with the relatively widespread availability of the `Array.prototype.forEach` function (in 2015), it's worth noting that in those situations involving iteration primarily over an array of values, `.forEach()` provides a clean, natural way to get a distinct closure for every iteration. That is, assuming you've got some sort of array containing values (DOM references, objects, whatever), and the problem arises of setting up callbacks specific to each element, you can do this:

```javascript
var someArray = [ /* whatever */ ];
// ...
someArray.forEach(function(arrayElement) {
  // ... code code code for this one element
  someAsynchronousFunction(arrayElement, function() {
    arrayElement.doSomething();
  });
});
```

The idea is that each invocation of the callback function used with the `.forEach` loop will be its own closure. The parameter passed in to that handler is the array element specific to that particular step of the iteration. If it's used in an asynchronous callback, it won't collide with any of the other callbacks established at other steps of the iteration.
If you happen to be working in jQuery, the `$.each()` function gives you a similar capability.
Update 2:
ECMAScript 6 (ES6), the newest version of JavaScript, is now starting to be implemented in many evergreen browsers and backend systems. There are also transpilers like Babel that will convert ES6 to ES5 to allow usage of new features on older systems.
ES6 introduces new `let` and `const` keywords that are scoped differently than `var`-based variables. For example, in a loop with a `let`-based index, each iteration through the loop will have a new value of ``i where each value is scoped inside the loop, so your code would work as you expect. There are many resources, but I'd recommend 2ality's block-scoping post as a great source of information.

```javascript
for (let i = 0; i < 3; i++) {
    funcs[i] = function() {
        console.log("My value: " + i);
    };
}
```

Beware, though, that IE9-IE11 and Edge prior to Edge 14 support `let` but get the above wrong (they don't create a new ``i each time, so all the functions above would log 3 like they would if we used `var`). Edge 14 finally gets it right.

## [How can I know which radio button is selected via jQuery?](https://stackoverflow.com/questions/596351/how-can-i-know-which-radio-button-is-selected-via-jquery)

**2244 Votes**, juan

To get the value of the selected `radioName` item of a form with id `myForm`:

```javascript
$('input[name=radioName]:checked', '#myForm').val()
```

Here's an example:



```javascript
$('#myForm input').on('change', function() {
   alert($('input[name=radioName]:checked', '#myForm').val()); 
});```


```javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<form id="myForm">
  <input type="radio" name="radioName" value="1" /> 1 <br />
  <input type="radio" name="radioName" value="2" /> 2 <br />
  <input type="radio" name="radioName" value="3" /> 3 <br />
</form>```

## [Change an element's class with JavaScript](https://stackoverflow.com/questions/195951/change-an-elements-class-with-javascript)

**2232 Votes**, Nathan Smith

### Modern HTML5 Techniques for changing classes

Modern browsers have added classList which provides methods to make it easier to manipulate classes without needing a library:

```javascript
document.getElementById("MyElement").classList.add('MyClass');

document.getElementById("MyElement").classList.remove('MyClass');

if ( document.getElementById("MyElement").classList.contains('MyClass') )

document.getElementById("MyElement").classList.toggle('MyClass');
```

Unfortunately, these do not work in Internet Explorer prior to v10, though there is a shim to add support for it to IE8 and IE9, available from this page. It is, though, getting more and more supported.

### Simple cross-browser solution

The standard JavaScript way to select an element is using `document.getElementById("Id")`, which is what the following examples use - you can of course obtain elements in other ways, and in the right situation may simply use `this` instead - however, going into detail on this is beyond the scope of the answer.
To change all classes for an element:
To replace all existing classes with one or more new classes, set the className attribute:

```javascript
document.getElementById("MyElement").className = "MyClass";
```

(You can use a space-delimited list to apply multiple classes.)
To add an additional class to an element:
To add a class to an element, without removing/affecting existing values, append a space and the new classname, like so:

```javascript
document.getElementById("MyElement").className += " MyClass";
```

To remove a class from an element:
To remove a single class to an element, without affecting other potential classes, a simple regex replace is required:

```javascript
document.getElementById("MyElement").className =
   document.getElementById("MyElement").className.replace
      ( /(?:^|\s)MyClass(?!\S)/g , '' )
/* Code wrapped for readability - above is all one statement */
```

An explanation of this regex is as follows:

```javascript
(?:^|\s) # Match the start of the string, or any single whitespace character

MyClass  # The literal text for the classname to remove

(?!\S)   # Negative lookahead to verify the above is the whole classname
         # Ensures there is no non-space character following
         # (i.e. must be end of string or a space)
```

The ``g flag tells the replace to repeat as required, in case the class name has been added multiple times.
To check if a class is already applied to an element:
The same regex used above for removing a class can also be used as a check as to whether a particular class exists:

```javascript
if ( document.getElementById("MyElement").className.match(/(?:^|\s)MyClass(?!\S)/) )
```


Assigning these actions to onclick events:
Whilst it is possible to write JavaScript directly inside the HTML event attributes (such as `onclick="this.className+=' MyClass'"`) this is not recommended behaviour. Especially on larger applications, more maintainable code is achieved by separating HTML markup from JavaScript interaction logic.
The first step to achieving this is by creating a function, and calling the function in the onclick attribute, for example:

```javascript
<script type="text/javascript">
    function changeClass(){
        // Code examples from above
    }
</script>
...
<button onclick="changeClass()">My Button</button>
```

(It is not required to have this code in script tags, this is simply for brevity of example, and including the JavaScript in a distinct file may be more appropriate.)
The second step is to move the onclick event out of the HTML and into JavaScript, for example using addEventListener

```javascript
<script type="text/javascript">
    function changeClass(){
        // Code examples from above
    }

    window.onload = function(){
        document.getElementById("MyElement").addEventListener( 'click', changeClass);
    }
</script>
...
<button id="MyElement">My Button</button>
```

(Note that the window.onload part is required so that the contents of that function are executed after the HTML has finished loading - without this, the MyElement might not exist when the JavaScript code is called, so that line would fail.)


### JavaScript Frameworks and Libraries

The above code is all in standard JavaScript, however it is common practise to use either a framework or a library to simplify common tasks, as well as benefit from fixed bugs and edge cases that you might not think of when writing your code.
Whilst some people consider it overkill to add a ~50KB framework for simply changing a class, if you are doing any substantial amount of JavaScript work, or anything that might have unusual cross-browser behaviour, it is well worth considering.
(Very roughly, a library is a set of tools designed for a specific task, whilst a framework generally contains multiple libraries and performs a complete set of duties.)
The examples above have been reproduced below using jQuery, probably the most commonly used JavaScript library (though there are others worth investigating too).
(Note that ``$ here is the jQuery object.)
Changing Classes with jQuery:

```javascript
$('#MyElement').addClass('MyClass');

$('#MyElement').removeClass('MyClass');

if ( $('#MyElement').hasClass('MyClass') )
```

In addition, jQuery provides a shortcut for adding a class if it doesn't apply, or removing a class that does:

```javascript
$('#MyElement').toggleClass('MyClass');
```


Assigning a function to a click event with jQuery:

```javascript
$('#MyElement').click(changeClass);
```

or, without needing an id:

```javascript
$(':button:contains(My Button)').click(changeClass);
```

## [What is the !! (not not) operator in JavaScript?](https://stackoverflow.com/questions/784929/what-is-the-not-not-operator-in-javascript)

**2220 Votes**, Hexagon Theory

Coerces `oObject` to boolean. If it was falsey (e.g. 0, `null`, `undefined`, etc.), it will be `false`, otherwise, `true`.

```javascript
!oObject  //Inverted boolean
!!oObject //Non inverted boolean so true boolean representation
```

So `!!` is not an operator, it's just the ``! operator twice.
Real World Example "Test IE version":  

```javascript
let isIE8 = false;  
isIE8 = !! navigator.userAgent.match(/MSIE 8.0/);  
console.log(isIE8); // returns true or false 
```

If you 

```javascript
console.log(navigator.userAgent.match(/MSIE 8.0/));  
// returns null  
```

but if you 

```javascript
console.log(!!navigator.userAgent.match(/MSIE 8.0/));  
// returns true or false
```

## [Can (a== 1 && a ==2 && a==3) ever evaluate to true?](https://stackoverflow.com/questions/48270127/can-a-1-a-2-a-3-ever-evaluate-to-true)

**2204 Votes**, Dimpu Aravind Buddha

If you take advantage of how `==` works, you could simply create an object with a custom `toString` (or `valueOf`) function that changes what it returns each time it is used such that it satisfies all three conditions.



```javascript
const a = {
  i: 1,
  toString: function () {
    return a.i++;
  }
}

if(a == 1 && a == 2 && a == 3) {
  console.log('Hello World!');
}```





The reason this works is due to the use of the loose equality operator. When using loose equality, if one of the operands is of a different type than the other, the engine will attempt to convert one to the other. In the case of an object on the left and a number on the right, it will attempt to convert the object to a number by first calling `valueOf` if it is callable, and failing that, it will call `toString`. I used `toString` in this case simply because it's what came to mind, `valueOf` would make more sense. If I instead returned a string from `toString`, the engine would have then attempted to convert the string to a number giving us the same end result, though with a slightly longer path.

## [How to decide when to use Node.js?](https://stackoverflow.com/questions/5062614/how-to-decide-when-to-use-node-js)

**2200 Votes**, Legend

You did a great job of summarizing what's awesome about Node.js. My feeling is that Node.js is especially suited for applications where you'd like to maintain a persistent connection from the browser back to the server. Using a technique known as "long-polling", you can write an application that sends updates to the user in real time. Doing long polling on many of the web's giants, like Ruby on Rails or Django, would create immense load on the server, because each active client eats up one server process. This situation amounts to a tarpit attack. When you use something like Node.js, the server has no need of maintaining separate threads for each open connection.  
This means you can create a browser-based chat application in Node.js that takes almost no system resources to serve a great many clients. Any time you want to do this sort of long-polling, Node.js is a great option.  
It's worth mentioning that Ruby and Python both have tools to do this sort of thing (eventmachine and twisted, respectively), but that Node.js does it exceptionally well, and from the ground up. JavaScript is exceptionally well situated to a callback-based concurrency model, and it excels here. Also, being able to serialize and deserialize with JSON native to both the client and the server is pretty nifty. 
I look forward to reading other answers here, this is a fantastic question. 
It's worth pointing out that Node.js is also great for situations in which you'll be reusing a lot of code across the client/server gap. The Meteor framework makes this really easy, and a lot of folks are suggesting this might be the future of web development. I can say from experience that it's a whole lot of fun to write code in Meteor, and a big part of this is spending less time thinking about how you're going to restructure your data, so the code that runs in the browser can easily manipulate it and pass it back. 
Here's an article on Pyramid and long-polling, which turns out to be very easy to set up with a little help from gevent: TicTacToe and Long Polling with Pyramid.

## [How do I empty an array in JavaScript?](https://stackoverflow.com/questions/1232040/how-do-i-empty-an-array-in-javascript)

**2199 Votes**, amir

Ways to clear an existing array ``A:
Method 1
(this was my original answer to the question)

```javascript
A = [];
```

This code will set the variable ``A to a new empty array. This is perfect if you don't have references to the original array ``A anywhere else because this actually creates a brand new (empty) array. You should be careful with this method because if you have referenced this array from another variable or property, the original array will remain unchanged. Only use this if you only reference the array by its original variable ``A.
This is also the fastest solution.
This code sample shows the issue you can encounter when using this method:

```javascript
var arr1 = ['a','b','c','d','e','f'];
var arr2 = arr1;  // Reference arr1 by another variable 
arr1 = [];
console.log(arr2); // Output ['a','b','c','d','e','f']
```

Method 2 (as suggested by Matthew Crumley)

```javascript
A.length = 0
```

This will clear the existing array by setting its length to 0. Some have argued that this may not work in all implementations of JavaScript, but it turns out that this is not the case. It also works when using "strict mode" in ECMAScript 5 because the length property of an array is a read/write property.
Method 3 (as suggested by Anthony)

```javascript
A.splice(0,A.length)
```

Using `.splice()` will work perfectly, but since the `.splice()` function will return an array with all the removed items, it will actually return a copy of the original array. Benchmarks suggest that this has no effect on performance whatsoever.
Method 4 (as suggested by tanguy_k)

```javascript
while(A.length > 0) {
    A.pop();
}
```

This solution is not very succinct, and it is also the slowest solution, contrary to earlier benchmarks referenced in the original answer.
Performance
Of all the methods of clearing an existing array, methods 2 and 3 are very similar in performance and are a lot faster than method 4. See this benchmark.
As pointed out by Diadistis in their answer below, the original benchmarks that were used to determine the performance of the four methods described above were flawed. The original benchmark reused the cleared array so the second iteration was clearing an array that was already empty.
The following benchmark fixes this flaw: http://jsben.ch/#/hyj65. It clearly shows that methods #2 (length property) and #3 (splice) are the fastest (not counting method #1 which doesn't change the original array).

This has been a hot topic and the cause of a lot of controversy. There are actually many correct answers and because this answer has been marked as the accepted answer for a very long time, I will include all of the methods here. If you vote for this answer, please upvote the other answers that I have referenced as well.

## [Checking if a key exists in a JavaScript object?](https://stackoverflow.com/questions/1098040/checking-if-a-key-exists-in-a-javascript-object)

**2164 Votes**, Adam Ernst

Checking for undefined-ness is not an accurate way of testing whether a key exists. What if the key exists but the value is actually `undefined`?

```javascript
var obj = { key: undefined };
obj["key"] != undefined // false, but the key exists!
```

You should instead use the `in` operator:

```javascript
"key" in obj // true, regardless of the actual value
```

If you want to check if a key doesn't exist, remember to use parenthesis:

```javascript
!("key" in obj) // true if "key" doesn't exist in object
!"key" in obj   // ERROR!  Equivalent to "false in obj"
```

Or, if you want to particularly test for properties of the object instance (and not inherited properties), use `hasOwnProperty`:

```javascript
obj.hasOwnProperty("key") // true
```

For performance comparison between the methods that are `in`, `hasOwnProperty` and key is `undefined`, see this benchmark

## [What's the difference between tilde(~) and caret(^) in package.json?](https://stackoverflow.com/questions/22343224/whats-the-difference-between-tilde-and-caret-in-package-json)

**2141 Votes**, Fizer Khan

In the simplest terms, the tilde matches the most recent minor version
  (the middle number). ~1.2.3 will match all 1.2.x versions but will
  miss 1.3.0.
The caret, on the other hand, is more relaxed. It will update you to
  the most recent major version (the first number). ^1.2.3 will match
  any 1.x.x release including 1.3.0, but will hold off on 2.0.0.

http://fredkschott.com/post/2014/02/npm-no-longer-defaults-to-tildes/

## [Validate decimal numbers in JavaScript - IsNumeric()](https://stackoverflow.com/questions/18082/validate-decimal-numbers-in-javascript-isnumeric)

**2117 Votes**, community-wiki

@Joel's answer is pretty close, but it will fail in the following cases:

```javascript
// Whitespace strings:
IsNumeric(' ') == true;
IsNumeric('\t\t') == true;
IsNumeric('\n\r') == true;

// Number literals:
IsNumeric(-1) == false;
IsNumeric(0) == false;
IsNumeric(1.1) == false;
IsNumeric(8e5) == false;
```

Some time ago I had to implement an `IsNumeric` function, to find out if a variable contained a numeric value, regardless of its type, it could be a `String` containing a numeric value (I had to consider also exponential notation, etc.), a `Number` object, virtually anything could be passed to that function, I couldn't make any type assumptions,  taking care of type coercion (eg. `+true == 1;` but `true` shouldn't be considered as `"numeric"`).
I think is worth sharing this set of +30 unit tests (old link) made to numerous function implementations, and also share the one that passes all my tests:

```javascript
function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}
```

P.S. isNaN & isFinite have a confusing behavior due to forced conversion to number. In ES6, Number.isNaN & Number.isFinite would fix these issues. Keep that in mind when using them. 

Update : 
Here's how jQuery does it now (2.2-stable) : 

```javascript
isNumeric: function( obj ) {
    var realStringObj = obj && obj.toString();
    return !jQuery.isArray( obj ) && ( realStringObj - parseFloat( realStringObj ) + 1 ) >= 0;
}
```

Update :
Angular 4.3 :

```javascript
export function isNumeric(value: any): boolean {
  return !isNaN(value - parseFloat(value));
}
```

## [Encode URL in JavaScript?](https://stackoverflow.com/questions/332872/encode-url-in-javascript)

**2084 Votes**, nickf

Check out the built-in function `encodeURIComponent(str)` and `encodeURI(str)`.
In your case, this should work:

```javascript
var myOtherUrl = 
       "http://example.com/index.html?url=" + encodeURIComponent(myUrl);
```

## [How do you check for an empty string in JavaScript?](https://stackoverflow.com/questions/154059/how-do-you-check-for-an-empty-string-in-javascript)

**2080 Votes**, casademora

If you just want to check whether there's any value, you can do 

```javascript
if (strValue) {
    //do something
}
```

If you need to check specifically for an empty string over null, I would think checking against `""` is your best bet, using the `===` operator (so that you know that it is, in fact, a string you're comparing against).

## [Check if object is array?](https://stackoverflow.com/questions/4775722/check-if-object-is-array)

**2076 Votes**, mpen

In modern browsers you can do

```javascript
Array.isArray(obj)
```

(Supported by Chrome 5, Firefox 4.0, IE 9, Opera 10.5 and Safari 5)
For backward compatibility you can add the following

```javascript
# only implement if no native implementation is available
if (typeof Array.isArray === 'undefined') {
  Array.isArray = function(obj) {
    return Object.prototype.toString.call(obj) === '[object Array]';
  }
};
```

If you use jQuery you can use `jQuery.isArray(obj)` or `$.isArray(obj)`. If you use underscore you can use `_.isArray(obj)`
If you don't need to detect arrays created in different frames you can also just use `instanceof`

```javascript
obj instanceof Array
```

## [How do I loop through or enumerate a JavaScript object?](https://stackoverflow.com/questions/684672/how-do-i-loop-through-or-enumerate-a-javascript-object)

**2051 Votes**, Tanmoy

You can use the `for-in` loop as shown by others. However, you also have to make sure that the key you get is an actual property of an object, and doesn't come from the prototype.
Here is the snippet:



```javascript
var p = {
    "p1": "value1",
    "p2": "value2",
    "p3": "value3"
};

for (var key in p) {
    if (p.hasOwnProperty(key)) {
        console.log(key + " -> " + p[key]);
    }
}```
