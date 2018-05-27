# StackOverflow Top ReactJS Questions


## [Why use Redux over Facebook Flux?](https://stackoverflow.com/questions/32461229/why-use-redux-over-facebook-flux)

**961 Votes**, Volodymyr Bakhmatiuk

Redux author here!  
Redux is not that different from Flux. Overall it has same architecture, but Redux is able to cut some complexity corners by using functional composition where Flux uses callback registration.
There is not a fundamental difference in Redux, but I find it makes certain abstractions easier, or at least possible to implement, that would be hard or impossible to implement in Flux.

### Reducer Composition

Take, for example, pagination. My Flux + React Router example handles pagination, but the code for that is awful. One of the reasons it's awful is that Flux makes it unnatural to reuse functionality across stores. If two stores need to handle pagination in response to different actions, they either need to inherit from a common base store (bad! you're locking yourself into a particular design when you use inheritance), or call a function from the handler, which will need to somehow operate on the Flux store's private state. The whole thing is messy (although definitely in the realm of possible).
On the other hand, with Redux pagination is natural thanks to reducer composition. It's reducers all the way down, so you can write a reducer factory that generates pagination reducers and then use it in your reducer tree. The key to why it's so easy is because in Flux, stores are flat, but in Redux, reducers can be nested via functional composition, just like React components can be nested.
This pattern also enables wonderful features like no-user-code undo/redo. Can you imagine plugging Undo/Redo into a Flux app being two lines of code? Hardly. With Redux, it isagain, thanks to reducer composition pattern. I need to highlight there's nothing new about itthis is the pattern pioneered and described in detail in Elm Architecture which was itself influenced by Flux.

### Server Rendering

People have been rendering on the server fine with Flux, but seeing that we have 20 Flux libraries each attempting to make server rendering easier, perhaps Flux has some rough edges on the server. The truth is Facebook doesn't do much server rendering, so they haven't been very concerned about it, and rely on the ecosystem to make it easier.
In traditional Flux, stores are singletons. This means it's hard to separate the data for different requests on the server. Not impossible, but hard. This is why most Flux libraries (as well as the new Flux Utils) now suggest you use classes instead of singletons, so you can instantiate stores per request.
There are still the following problems that you need to solve in Flux (either yourself or with the help of your favorite Flux library such as Flummox or Alt):

If stores are classes, how do I create and destroy them with dispatcher per request? When do I register stores?
How do I hydrate the data from the stores and later rehydrate it on the client? Do I need to implement special methods for this?

Admittedly Flux frameworks (not vanilla Flux) have solutions to these problems, but I find them overcomplicated. For example, Flummox asks you to implement `serialize()` and `deserialize()` in your stores. Alt solves this nicer by providing `takeSnapshot()` that automatically serializes your state in a JSON tree.
Redux just goes further: since there is just a single store (managed by many reducers), you don't need any special API to manage the (re)hydration. You don't need to flush or hydrate storesthere's just a single store, and you can read its current state, or create a new store with a new state. Each request gets a separate store instance. Read more about server rendering with Redux.
Again, this is a case of something possible both in Flux and Redux, but Flux libraries solve this problem by introducing a ton of API and conventions, and Redux doesn't even have to solve it because it doesn't have that problem in the first place thanks to conceptual simplicity.

### Developer Experience

I didn't actually intend Redux to become a popular Flux libraryI wrote it as I was working on my ReactEurope talk on hot reloading with time travel. I had one main objective: make it possible to change reducer code on the fly or even change the past by crossing out actions, and see the state being recalculated.

I haven't seen a single Flux library that is able to do this. React Hot Loader also doesn't let you do thisin fact it breaks if you edit Flux stores because it doesn't know what to do with them.
When Redux needs to reload the reducer code, it calls `replaceReducer()`, and the app runs with the new code. In Flux, data and functions are entangled in Flux stores, so you can't just replace the functions. Moreover, you'd have to somehow re-register the new versions with the Dispatchersomething Redux doesn't even have.

### Ecosystem

Redux has a rich and fast-growing ecosystem. This is because it provides a few extension points such as middleware. It was designed with use cases such as logging, support for Promises, Observables, routing, immutability dev checks, persistence, etc, in mind. Not all of these will turn out to be useful, but it's nice to have access to a set of tools that can be easily combined to work together.

### Simplicity

Redux preserves all the benefits of Flux (recording and replaying of actions, unidirectional data flow, dependent mutations) and adds new benefits (easy undo-redo, hot reloading) without introducing Dispatcher and store registration.
Keeping it simple is important because it keeps you sane while you implement higher-level abstractions.
Unlike most Flux libraries, Redux API surface is tiny. If you remove the developer warnings, comments, and sanity checks, it's 99 lines. There is no tricky async code to debug.
You can actually read it and understand all of Redux.

See also my answer on downsides of using Redux compared to Flux.

## [Programmatically navigate using react router](https://stackoverflow.com/questions/31079081/programmatically-navigate-using-react-router)

**710 Votes**, George Mauer

React Router v4

With v4 of React Router, there are three approaches that you can take to programmatic routing within components.

Use the `withRouter` higher-order component.
Use composition and render a `<Route>`
Use the `context`.

React Router is mostly a wrapper around the `history` library. `history` handles interaction with the browser's `window.history` for you with its browser and hash histories. It also provides a memory history which is useful for environments that don't have a global history. This is particularly useful in mobile app development (`react-native`) and unit testing with Node.
A `history` instance has two methods for navigating: `push` and `replace`. If you think of the `history` as an array of visited locations, `push` will add a new location to the array and `replace` will replace the current location in the array with the new one. Typically you will want to use the `push` method when you are navigating.
In earlier versions of React Router, you had to create your own `history` instance, but in v4 the `<BrowserRouter>`, `<HashRouter>`, and `<MemoryRouter>` components will created browser, hash, and memory instances for you. React Router makes the properties and methods of the `history` instance associated with your router available through the context, under the `router` object.
1. Use the `withRouter` higher-order component
The `withRouter` higher-order component will inject the `history` object as a prop of the component. This allows you to access the `push` and `replace` methods without having to deal with the `context`.

```reactjs
import { withRouter } from 'react-router-dom'
// this also works with react-router-native

const Button = withRouter(({ history }) => (
  <button
    type='button'
    onClick={() => { history.push('/new-location') }}
  >
    Click Me!
  </button>
))
```

2. Use composition and render a `<Route>`
The `<Route>` component isn't just for matching locations. You can render a pathless route and it will always match the current location. The `<Route>` component passes the same props as `withRouter`, so you will be able to access the `history` methods through the `history` prop.

```reactjs
import { Route } from 'react-router-dom'

const Button = () => (
  <Route render={({ history}) => (
    <button
      type='button'
      onClick={() => { history.push('/new-location') }}
    >
      Click Me!
    </button>
  )} />
)
```

3. Use the context*
*But you probably should not
The last option is one that you should only use if you feel comfortable working with React's context model. Although context is an option, it should be stressed that context is an unstable API and React has a section Why Not To Use Context in their documentation. So use at your own risk!

```reactjs
const Button = (props, context) => (
  <button
    type='button'
    onClick={() => {
      // context.history.push === history.push
      context.history.push('/new-location')
    }}
  >
    Click Me!
  </button>
)

// you need to specify the context type so that it
// is available within the component
Button.contextTypes = {
  history: React.PropTypes.shape({
    push: React.PropTypes.func.isRequired
  })
}
```

1 and 2 are the simplest choices to implement, so for most use cases they are your best bets.

## [Loop inside React JSX](https://stackoverflow.com/questions/22876978/loop-inside-react-jsx)

**677 Votes**, Ben Roberts

Think of it like you're just calling JavaScript functions. You can't put a `for` loop inside a function call:

```reactjs
return tbody(
    for (var i = 0; i < numrows; i++) {
        ObjectRow()
    } 
)
```

But you can make an array, and then pass that in:

```reactjs
var rows = [];
for (var i = 0; i < numrows; i++) {
    rows.push(ObjectRow());
}
return tbody(rows);
```


You can use basically the same structure when working with JSX:

```reactjs
var rows = [];
for (var i = 0; i < numrows; i++) {
    // note: we add a key prop here to allow react to uniquely identify each
    // element in this array. see: https://reactjs.org/docs/lists-and-keys.html
    rows.push(<ObjectRow key={i} />);
}
return <tbody>{rows}</tbody>;
```

Incidentally, my JavaScript example is almost exactly what that example of JSX transforms into. Play around with Babel REPL to get a feel for how JSX works.

## [How to pass props to {this.props.children}](https://stackoverflow.com/questions/32370994/how-to-pass-props-to-this-props-children)

**518 Votes**, plus-

You can use React.Children to iterate over the children, and then clone each element with new props (shallow merged) using React.cloneElement e.g:

```reactjs
const Child = ({ doSomething, value }) => (
  <div onClick={() => doSomething(value)}>Click Me</div>
);

class Parent extends React.PureComponent {
  doSomething = (value) => {
    console.log('doSomething called by child with value:', value);
  }

  render() {
    const { children } = this.props;

    const childrenWithProps = React.Children.map(children, child =>
      React.cloneElement(child, { doSomething: this.doSomething }));

    return <div>{childrenWithProps}</div>
  }
};

ReactDOM.render(
  <Parent>
    <Child value="1" />
    <Child value="2" />
  </Parent>,
  document.getElementById('container')
);
```

Fiddle: https://jsfiddle.net/2q294y43/2/

## [What is the difference between using constructor vs getInitialState in React / React Native?](https://stackoverflow.com/questions/30668326/what-is-the-difference-between-using-constructor-vs-getinitialstate-in-react-r)

**406 Votes**, Nader Dabit

The two approaches are not interchangeable. You should initialize state in the constructor when using ES6 classes, and define the `getInitialState` method when using `React.createClass`.
See the official React doc on the subject of ES6 classes.

```reactjs
class MyComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { /* initial state */ };
  }
}
```

is equivalent to 

```reactjs
var MyComponent = React.createClass({
  getInitialState() {
    return { /* initial state */ };
  },
});
```

## [What do these three dots in React do?](https://stackoverflow.com/questions/31048953/what-do-these-three-dots-in-react-do)

**392 Votes**, Thomas Johansen

Updated Answer (April 2018)
That's property spread notation, being added in ES2018 (proposal here, in the draft specification here), but long-supported in React projects via transpilation (as "JSX spread attributes" even though you could do it elsewhere, too, not just attributes).
`{...this.props}` spreads out the properties in props as discrete properties (attributes) on the `Modal` element you're creating. For instance, if `this.props` contained `a: 1` and `b: 2`, then

```reactjs
<Modal {...this.props} title='Modal heading' animation={false}>
```

would be the same as

```reactjs
<Modal a={this.props.a} b={this.props.b} title='Modal heading' animation={false}>
```

But it's dynamic, so whatever properties are in `props` are included.
Spread notation is handy not only for that use case, but for creating a new object with most (or all) of the properties of an existing object which comes up a lot when you're updating state, since you can't modify state directly:

```reactjs
this.setState(prevState => {
    return {foo: {...prevState.foo, a: "updated"}};
});
```

That replaces `this.state.foo` with a new object with all the same properties as `foo` except the ``a property, which becomes `"updated"`:



```reactjs
const obj = {
  foo: {
    a: 1,
    b: 2,
    c: 3
  }
};
console.log("original", obj.foo);
// Creates a NEW object and assigns it to `obj.foo`
obj.foo = {...obj.foo, a: "updated"};
console.log("updated", obj.foo);```


```reactjs
.as-console-wrapper {
  max-height: 100% !important;
}```




Original Answer (July 2015)
Those are JSX spread attributes:

Spread Attributes
If you already have props as an object, and you want to pass it in JSX, you can use `...` as a "spread" operator to pass the whole props object. These two components are equivalent:

```reactjs
function App1() {
  return <Greeting firstName="Ben" lastName="Hector" />;
}

function App2() {
  const props = {firstName: 'Ben', lastName: 'Hector'};
  return <Greeting {...props} />;
}
```

Spread attributes can be useful when you are building generic containers. However, they can also make your code messy by making it easy to pass a lot of irrelevant props to components that don't care about them. We recommend that you use this syntax sparingly.

That documentation used to mention that although this is (for now) a JSX thing, there's a proposal to add Object Rest and Spread Properties to JavaScript itself. (JavaScript has had rest and spread for arrays since ES2015, but not for object properties.) As of November 2017, that proposal is at Stage3 and has been for some time. Both Chrome's V8 and Firefox's SpiderMonkey now support it, so presumably if the specification language is worked out in time it'll be Stage4 soon and part of the ES2018 snapshot specification. (More about stages here.) Transpilers have supported it for some time (even separately from JSX).

Side note: Although the JSX quote above talks about a "spread operator," `...` isn't an operator, and can't be. Operators have a single result value. `...` is primary syntax (kind of like the `()` used with `for` aren't the grouping operator, even though they look like it).

## [Why do we need middleware for async flow in Redux?](https://stackoverflow.com/questions/34570758/why-do-we-need-middleware-for-async-flow-in-redux)

**370 Votes**, sbichenko

What is wrong with this approach? Why would I want to use Redux Thunk or Redux Promise, as the documentation suggests?

There is nothing wrong with this approach. Its just inconvenient in a large application because youll have different components performing the same actions, you might want to debounce some actions, or keep some local state like auto-incrementing IDs close to action creators, etc. So it is just easier from the maintenance point of view to extract action creators into separate functions.
You can read my answer to How to dispatch a Redux action with a timeout for a more detailed walkthrough.
Middleware like Redux Thunk or Redux Promise just gives you syntax sugar for dispatching thunks or promises, but you dont have to use it.
So, without any middleware, your action creator might look like

```reactjs
// action creator
function loadData(dispatch, userId) { // needs to dispatch, so it is first argument
  return fetch(`http://data.com/${userId}`)
    .then(res => res.json())
    .then(
      data => dispatch({ type: 'LOAD_DATA_SUCCESS', data }),
      err => dispatch({ type: 'LOAD_DATA_FAILURE', err })
    );
}

// component
componentWillMount() {
  loadData(this.props.dispatch, this.props.userId); // don't forget to pass dispatch
}
```

But with Thunk Middleware you can write it like this:

```reactjs
// action creator
function loadData(userId) {
  return dispatch => fetch(`http://data.com/${userId}`) // Redux Thunk handles these
    .then(res => res.json())
    .then(
      data => dispatch({ type: 'LOAD_DATA_SUCCESS', data }),
      err => dispatch({ type: 'LOAD_DATA_FAILURE', err })
    );
}

// component
componentWillMount() {
  this.props.dispatch(loadData(this.props.userId)); // dispatch like you usually do
}
```

So there is no huge difference. One thing I like about the latter approach is that the component doesnt care that the action creator is async. It just calls `dispatch` normally, it can also use `mapDispatchToProps` to bind such action creator with a short syntax, etc. The components dont know how action creators are implemented, and you can switch between different async approaches (Redux Thunk, Redux Promise, Redux Saga) without changing the components. On the other hand, with the former, explicit approach, your components know exactly that a specific call is async, and needs `dispatch` to be passed by some convention (for example, as a sync parameter).
Also think about how this code will change. Say we want to have a second data loading function, and to combine them in a single action creator.
With the first approach we need to be mindful of what kind of action creator we are calling:

```reactjs
// action creators
function loadSomeData(dispatch, userId) {
  return fetch(`http://data.com/${userId}`)
    .then(res => res.json())
    .then(
      data => dispatch({ type: 'LOAD_SOME_DATA_SUCCESS', data }),
      err => dispatch({ type: 'LOAD_SOME_DATA_FAILURE', err })
    );
}
function loadOtherData(dispatch, userId) {
  return fetch(`http://data.com/${userId}`)
    .then(res => res.json())
    .then(
      data => dispatch({ type: 'LOAD_OTHER_DATA_SUCCESS', data }),
      err => dispatch({ type: 'LOAD_OTHER_DATA_FAILURE', err })
    );
}
function loadAllData(dispatch, userId) {
  return Promise.all(
    loadSomeData(dispatch, userId), // pass dispatch first: it's async
    loadOtherData(dispatch, userId) // pass dispatch first: it's async
  );
}


// component
componentWillMount() {
  loadAllData(this.props.dispatch, this.props.userId); // pass dispatch first
}
```

With Redux Thunk action creators can `dispatch` the result of other action creators and not even think whether those are synchronous or asynchronous:

```reactjs
// action creators
function loadSomeData(userId) {
  return dispatch => fetch(`http://data.com/${userId}`)
    .then(res => res.json())
    .then(
      data => dispatch({ type: 'LOAD_SOME_DATA_SUCCESS', data }),
      err => dispatch({ type: 'LOAD_SOME_DATA_FAILURE', err })
    );
}
function loadOtherData(userId) {
  return dispatch => fetch(`http://data.com/${userId}`)
    .then(res => res.json())
    .then(
      data => dispatch({ type: 'LOAD_OTHER_DATA_SUCCESS', data }),
      err => dispatch({ type: 'LOAD_OTHER_DATA_FAILURE', err })
    );
}
function loadAllData(userId) {
  return dispatch => Promise.all(
    dispatch(loadSomeData(userId)), // just dispatch normally!
    dispatch(loadOtherData(userId)) // just dispatch normally!
  );
}


// component
componentWillMount() {
  this.props.dispatch(loadAllData(this.props.userId)); // just dispatch normally!
}
```

With this approach, if you later want your action creators to look into current Redux state, you can just use the second `getState` argument passed to the thunks without modifying the calling code at all:

```reactjs
function loadSomeData(userId) {
  // Thanks to Redux Thunk I can use getState() here without changing callers
  return (dispatch, getState) => {
    if (getState().data[userId].isLoaded) {
      return Promise.resolve();
    }

    fetch(`http://data.com/${userId}`)
      .then(res => res.json())
      .then(
        data => dispatch({ type: 'LOAD_SOME_DATA_SUCCESS', data }),
        err => dispatch({ type: 'LOAD_SOME_DATA_FAILURE', err })
      );
  }
}
```

If you need to change it to be synchronous, you can also do this without changing any calling code:

```reactjs
// I can change it to be a regular action creator without touching callers
function loadSomeData(userId) {
  return {
    type: 'LOAD_SOME_DATA_SUCCESS',
    data: localStorage.getItem('my-data')
  }
}
```

So the benefit of using middleware like Redux Thunk or Redux Promise is that components arent aware of how action creators are implemented, and whether they care about Redux state, whether they are synchronous or asynchronous, and whether or not they call other action creators. The downside is a little bit of indirection, but we believe its worth it in real applications.
Finally, Redux Thunk and friends is just one possible approach to asynchronous requests in Redux apps. Another interesting approach is Redux Saga which lets you define long-running daemons (sagas) that take actions as they come, and transform or perform requests before outputting actions. This moves the logic from action creators into sagas. You might want to check it out, and later pick what suits you the most.

I searched the Redux repo for clues, and found that Action Creators were required to be pure functions in the past. 

This is incorrect. The docs said this, but the docs were wrong.
Action creators were never required to be pure functions.
We fixed the docs to reflect that.

## [React.js inline style best practices](https://stackoverflow.com/questions/26882177/react-js-inline-style-best-practices)

**359 Votes**, eye_mew

There aren't a lot of "Best Practices" yet. Those of us that are using inline-styles, for React components, are still very much experimenting.
There are a number of approaches that vary wildly: React inline-style lib comparison chart

### All or nothing?

What we refer to as "style" actually includes quite a few concepts:

Layout  how an element/component looks in relationship to others
Appearance  the characteristics of an element/component
Behavior and state  how an element/component looks in a given state


### Start with state-styles

React is already managing the state of your components, this makes styles of state and behavior a natural fit for colocation with your component logic.
Instead of building components to render with conditional state-classes, consider adding state-styles directly:

```reactjs
// Typical component with state-classes
<li 
 className={classnames({ 'todo-list__item': true, 'is-complete': item.complete })} />


// Using inline-styles for state
<li className='todo-list__item'
 style={(item.complete) ? styles.complete : {}} />
```

Note that we're using a class to style appearance but no longer using any `.is-` prefixed class for state and behavior.
We can use `Object.assign` (ES6) or `_.extend` (underscore/lodash) to add support for multiple states:

```reactjs
// Supporting multiple-states with inline-styles
<li 'todo-list__item'
 style={Object.assign({}, item.complete && styles.complete, item.due && styles.due )}>
```


### Customization and reusability

Now that we're using `Object.assign` it becomes very simple to make our component reusable with different styles. If we want to override the default styles, we can do so at the call-site with props, like so: `<TodoItem dueStyle={ fontWeight: "bold" } />`. Implemented like this:

```reactjs
<li 'todo-list__item'
 style={Object.assign({},
         item.due && styles.due,
         item.due && this.props.dueStyles)}>
```

Layout
Personally, I don't see compelling reason to inline layout styles. There are a number of great CSS layout systems out there. I'd just use one.
That said, don't add layout styles directly to your component. Wrap your components with layout components. Here's an example.

```reactjs
// This couples your component to the layout system
// It reduces the reusability of your component
<UserBadge
 className="col-xs-12 col-sm-6 col-md-8"
 firstName="Michael"
 lastName="Chan" />

// This is much easier to maintain and change
<div class="col-xs-12 col-sm-6 col-md-8">
  <UserBadge
   firstName="Michael"
   lastName="Chan" />
</div>
```

For layout support, I often try to design components to be `100%` `width` and `height`.
Appearance
This is the most contentious area of the "inline-style" debate. Ultimately, it's up to the component your designing and the comfort of your team with JavaScript.
One thing is certain, you'll need the assistance of a library. Browser-states (`:hover`, `:focus`), and media-queries are painful in raw React.
I like Radium because the syntax for those hard parts is designed to model that of SASS.

### Code organization

Often you'll see a style object outside of the module. For a todo-list component, it might look something like this:

```reactjs
var styles = {
  root: {
    display: "block"
  },
  item: {
    color: "black"

    complete: {
      textDecoration: "line-through"
    },

    due: {
      color: "red"
    }
  },
}
```


### getter functions

Adding a bunch of style logic to your template can get a little messy (as seen above). I like to create getter functions to compute styles:

```reactjs
React.createClass({
  getStyles: function () {
    return Object.assign(
      {},
      item.props.complete && styles.complete,
      item.props.due && styles.due,
      item.props.due && this.props.dueStyles
    );
  },

  render: function () {
    return <li style={this.getStyles()}>{this.props.item}</li>
  }
});
```


### Further watching

I discussed all of these in more detail at React Europe earlier this year: Inline Styles and when it's best to 'just use CSS'.
I'm happy to help as you make new discoveries along the way :) Hit me up -> @chantastic

## [Pros/cons of using redux-saga with ES6 generators vs redux-thunk with ES2017 async/await](https://stackoverflow.com/questions/34930735/pros-cons-of-using-redux-saga-with-es6-generators-vs-redux-thunk-with-es2017-asy)

**342 Votes**, hampusohlsson

In redux-saga, the equivalent of the above example would be

```reactjs
export function* loginSaga() {
  while(true) {
    const { user, pass } = yield take(LOGIN_REQUEST)
    try {
      let { data } = yield call(request.post, '/login', { user, pass });
      yield fork(loadUserData, data.uid);
      yield put({ type: LOGIN_SUCCESS, data });
    } catch(error) {
      yield put({ type: LOGIN_ERROR, error });
    }  
  }
}

export function* loadUserData(uid) {
  try {
    yield put({ type: USERDATA_REQUEST });
    let { data } = yield call(request.get, `/users/${uid}`);
    yield put({ type: USERDATA_SUCCESS, data });
  } catch(error) {
    yield put({ type: USERDATA_ERROR, error });
  }
}
```

The first thing to notice is that we're calling the api functions using the form `yield call(func, ...args)`. `call` doesn't execute the effect, it just creates a plain object like `{type: 'CALL', func, args}`. The execution is delegated to the redux-saga middleware which takes care of executing the function and resuming the generator with its result.
The main advantage is that you can test the generator outside of Redux using simple equality checks

```reactjs
const iterator = loginSaga()

assert.deepEqual(iterator.next().value, take(LOGIN_REQUEST))

// resume the generator with some dummy action
const mockAction = {user: '...', pass: '...'}
assert.deepEqual(
  iterator.next(mockAction).value, 
  call(request.post, '/login', mockAction)
)

// simulate an error result
const mockError = 'invalid user/password'
assert.deepEqual(
  iterator.throw(mockError).value, 
  put({ type: LOGIN_ERROR, error: mockError })
)
```

Note we're mocking the api call result by simply injecting the mocked data into the `next` method of the iterator. Mocking data is way simpler than mocking functions.
The second thing to notice is the call to `yield take(ACTION)`. Thunks are called by the action creator on each new action (e.g. `LOGIN_REQUEST`). i.e. actions are continually pushed to thunks, and thunks have no control on when to stop handling those actions. 
In redux-saga, generators pull the next action. i.e. they have control when to listen for some action, and when to not. In the above example the flow instructions are placed inside a `while(true)` loop, so it'll listen for each incoming action, which somewhat mimics the thunk pushing behavior.
The pull approach allows implementing complex control flows. Suppose for example we want to add the following requirements 

Handle LOGOUT user action
upon the first successful login, the server returns a token which expires in some delay stored in a `expires_in` field. We'll have to refresh the authorization in the background on each `expires_in` milliseconds
Take into account that when waiting for the result of api calls (either initial login or refresh) the user may logout in-between.

How would you implement that with thunks; while also providing full test coverage for the entire flow? Here is how it may look with Sagas:

```reactjs
function* authorize(credentials) {
  const token = yield call(api.authorize, credentials)
  yield put( login.success(token) )
  return token
}

function* authAndRefreshTokenOnExpiry(name, password) {
  let token = yield call(authorize, {name, password})
  while(true) {
    yield call(delay, token.expires_in)
    token = yield call(authorize, {token})
  }
}

function* watchAuth() {
  while(true) {
    try {
      const {name, password} = yield take(LOGIN_REQUEST)

      yield race([
        take(LOGOUT),
        call(authAndRefreshTokenOnExpiry, name, password)
      ])

      // user logged out, next while iteration will wait for the
      // next LOGIN_REQUEST action

    } catch(error) {
      yield put( login.error(error) )
    }
  }
}
```

In the above example, we're expressing our concurrency requirement using `race`. If `take(LOGOUT)` wins the race (i.e. user clicked on a Logout Button). The race will automatically cancel the `authAndRefreshTokenOnExpiry` background task. And if the `authAndRefreshTokenOnExpiry` was blocked in middle of a `call(authorize, {token})` call it'll also be cancelled. Cancellation propagates downward automatically.
You can find a runnable demo of the above flow

## [Can you force a React component to rerender without calling setState?](https://stackoverflow.com/questions/30626030/can-you-force-a-react-component-to-rerender-without-calling-setstate)

**322 Votes**, Philip Walton

In your component, you can call `this.forceUpdate()` to force a rerender.  
Documentation: https://facebook.github.io/react/docs/component-api.html

## [Why is React's concept of Virtual DOM said to be more performant than dirty model checking?](https://stackoverflow.com/questions/21109361/why-is-reacts-concept-of-virtual-dom-said-to-be-more-performant-than-dirty-mode)

**315 Votes**, Daniil

I'm the primary author of a virtual-dom module, so I might be able to answer your questions. There are in fact 2 problems that need to be solved here

When do I re-render?  Answer: When I observe that the data is dirty.  
How do I re-render efficiently? Answer:  Using a virtual DOM to generate a real DOM patch

In React, each of your components have a state. This state is like an observable you might find in knockout or other MVVM style libraries. Essentially, React knows when to re-render the scene because it is able to observe when this data changes. Dirty checking is slower than observables because you must poll the data at a regular interval and check all of the values in the data structure recursively. By comparison, setting a value on the state will signal to a listener that some state has changed, so React can simply listen for change events on the state and queue up re-rendering.
The virtual DOM is used for efficient re-rendering of the DOM. This isn't really related to dirty checking your data. You could re-render using a virtual DOM with or without dirty checking. You're right in that there is some overhead in computing the diff between two virtual trees, but the virtual DOM diff is about understanding what needs updating in the DOM and not whether or not your data has changed. In fact, the diff algorithm is a dirty checker itself but it is used to see if the DOM is dirty instead.
We aim to re-render the virtual tree only when the state changes. So using an observable to check if the state has changed is an efficient way to prevent unnecessary re-renders, which would cause lots of unnecessary tree diffs. If nothing has changed, we do nothing.
A virtual DOM is nice because it lets us write our code as if we were re-rendering the entire scene. Behind the scenes we want to compute a patch operation that updates the DOM to look how we expect. So while the virtual DOM diff/patch algorithm is probably not the optimal solution, it gives us a very nice way to express our applications. We just declare exactly what we want and React/virtual-dom will work out how to make your scene look like this. We don't have to do manual DOM manipulation or get confused about previous DOM state. We don't have to re-render the entire scene either, which could be much less efficient than patching it.

## [React set focus on input after render](https://stackoverflow.com/questions/28889826/react-set-focus-on-input-after-render)

**313 Votes**, Dave

You should do it in `componentDidMount` and `refs callback` instead. Something like this

```reactjs
componentDidMount(){
   this.nameInput.focus(); 
}
```




```reactjs
class App extends React.Component{
  componentDidMount(){
    this.nameInput.focus();
  }
  render() {
    return(
      <div>
        <input 
          defaultValue="Won't focus" 
        />
        <input 
          ref={(input) => { this.nameInput = input; }} 
          defaultValue="will focus"
        />
      </div>
    );
  }
}
    
ReactDOM.render(<App />, document.getElementById('app'));```


```reactjs
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/15.3.1/react.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/15.3.1/react-dom.js"></script>
<div id="app"></div>```

## [Invariant Violation: _registerComponent(): Target container is not a DOM element](https://stackoverflow.com/questions/26566317/invariant-violation-registercomponent-target-container-is-not-a-dom-elem)

**307 Votes**, Dan Abramov

By the time script is executed, `document` element is not available yet, because `script` itself is in the `head`. While it's a valid solution to keep `script` in `head` and render on `DOMContentLoaded` event, it's even better to put your `script` at the very bottom of the `body` and render root component to a `div` before it like this:

```reactjs
<html>
<head>
</head>
<body>
  <div id="root"></div>
  <script src="/bundle.js"></script>
</body>
</html>
```

and in your code, call

```reactjs
React.render(<App />, document.getElementById('root'));
```

You should always render to a nested `div` instead of `body`. Otherwise all sorts of third-party code (Google Font Loader, browser plugins, whatever) can modify the `body` DOM node when React doesn't expect it, and cause weird errors that are very hard to trace and debug. Read more about this issue.
The nice thing about putting `script` at the bottom is that it won't block rendering until script load in case you add React server rendering to your project.

## [React js onClick can't pass value to method](https://stackoverflow.com/questions/29810914/react-js-onclick-cant-pass-value-to-method)

**304 Votes**, user1924375

### Easy Way

Use an arrow function:

```reactjs
return (
  <th value={column} onClick={() => this.handleSort(column)}>{column}</th>
);
```

This will create a new function that calls `handleSort` with the right params.

### Better Way

Extract it into a sub-component.
The problem with using an arrow function in the render call is it will create a new function every time, which ends up causing unneeded re-renders.
If you create a sub-component, you can pass handler and use props as the arguments, which will then re-render only when the props change (because the handler reference now never changes):
Sub-component

```reactjs
class TableHeader extends Component {
  handleClick = () => {
    this.props.onHeaderClick(this.props.value);
  }

  render() {
    return (
      <th onClick={this.handleClick}>
        {this.props.column}
      </th>
    );
  }
}
```

Main component

```reactjs
{this.props.defaultColumns.map((column) => (
  <TableHeader
    value={column}
    onHeaderClick={this.handleSort}
  />
))}
```


Old Easy Way (ES5)
Use `.bind` to pass the parameter you want:

```reactjs
return (
  <th value={column} onClick={that.handleSort.bind(that, column)}>{column}</th>
);
```

## [Uncaught Error: Invariant Violation: Element type is invalid: expected a string (for built-in components) or a class/function but got: object](https://stackoverflow.com/questions/34130539/uncaught-error-invariant-violation-element-type-is-invalid-expected-a-string)

**301 Votes**, Pankaj Thakur

In my case (using Webpack) it was the difference between:

```reactjs
import {MyComponent} from '../components/xyz.js';
```

vs

```reactjs
import MyComponent from '../components/xyz.js';
```

The second one works while the first caused the error.

## [What's the difference between super() and super(props) in React when using es6 classes?](https://stackoverflow.com/questions/30571875/whats-the-difference-between-super-and-superprops-in-react-when-using-e)

**298 Votes**, Misha Moroshko

There is only one reason when one needs to pass `props` to `super()`:
When you want to access `this.props` in constructor.
Passing:

```reactjs
class MyComponent extends React.Component {    
    constructor(props) {
        super(props)

        console.log(this.props)
        // -> { icon: 'home',  }
    }
}
```

Not passing:

```reactjs
class MyComponent extends React.Component {    
    constructor(props) {
        super()

        console.log(this.props)
        // -> undefined

        // Props parameter is still available
        console.log(props)
        // -> { icon: 'home',  }
    }

    render() {
        // No difference outside constructor
        console.log(this.props)
        // -> { icon: 'home',  }
    }
}
```

Note that passing or not passing `props` to `super` has no effect on later uses of `this.props` outside `constructor`. That is `render`, `shouldComponentUpdate`, or event handlers always have access to it.
This is explicitly said in one Sophie Alpert's answer to a similar question.

The documentationState and Lifecycle, Adding Local State to a Class, point 2recommends:

Class components should always call the base constructor with `props`.

However, no reason is provided. We can speculate it is either because of subclassing or for future compatibility.
(Thanks @MattBrowne for the link)

## [What is the difference between React Native and React?](https://stackoverflow.com/questions/34641582/what-is-the-difference-between-react-native-and-react)

**288 Votes**, shiva kumar

ReactJS is a JavaScript library, supporting both front end web and being run on the server, for building user interfaces and web applications.
React Native is a mobile framework that compiles to native app components, allowing you to build native mobile applications (iOS, Android, and Windows) in JavaScript that allows you to use ReactJS to build your components, and implements ReactJS under the hood.
Both are open sourced by Facebook.

## [React-router urls don't work when refreshing or writting manually](https://stackoverflow.com/questions/27928372/react-router-urls-dont-work-when-refreshing-or-writting-manually)

**278 Votes**, DavidDev

Looking at the comments on the accepted answer and the generic nature of this question ('don't work'), I thought this might be a good place for some general explanations about the issues involved here. So this answer is intended as background info / elaboration on the specific use case of the OP. Please bear with me.
Server-side vs Client-side
The first big thing to understand about this is that there are now 2 places where the URL is interpreted, whereas there used to be only 1 in 'the old days'. In the past, when life was simple, some user sent a request for `http://example.com/about` to the server, which inspected the path part of the URL, determined the user was requesting the about page and then sent back that page.
With client-side routing, which is what React-Router provides, things are less simple. At first, the client does not have any JS code loaded yet. So the very first request will always be to the server. That will then return a page that contains the needed script tags to load React and React Router etc. Only when those scripts have loaded does phase 2 start. In phase 2, when the user clicks on the 'About us' navigation link for example, the URL is changed locally only to `http://example.com/about` (made possible by the History API), but no request to the server is made.  Instead, React Router does it's thing on the client side, determines which React view to render and renders it. Assuming your about page does not need to make any REST calls, it's done already. You have transitioned from Home to About Us without any server request having fired.
So basically when you click a link, some Javascript runs that manipulates the URL in the address bar, without causing a page refresh, which in turn causes React Router to perform a page transition on the client side.
But now consider what happens if you copy-paste the URL in the address bar and e-mail it to a friend. Your friend has not loaded your website yet. In other words, she is still in phase 1. No React Router is running on her machine yet. So her browser will make a server request to `http://example.com/about`. 
And this is where your trouble starts. Until now, you could get away with just placing a static HTML at the webroot of your server. But that would give `404` errors for all other URLs when requested from the server. Those same URLs work fine on the client side, because there React Router is doing the routing for you, but they fail on the server side unless you make your server understand them.
Combining server- and client-side routing
If you want the `http://example.com/about` URL to work on both the server- and the client-side, you need to set up routes for it on both the server- and the client side. Makes sense right?
And this is where your choices begin. Solutions range from bypassing the problem altogether, via a catch-all route that returns the bootstrap HTML, to the full-on isomorphic approach where both the server and the client run the same JS code.
.

### Bypassing the problem altogether: Hash History

With Hash History instead of Browser History, your URL for the about page would look something like this:
`http://example.com/#/about`
The part after the hash (``#) symbol is not sent to the server. So the server only sees `http://example.com/` and sends the index page as expected. React-Router will pick up the `#/about` part and show the correct page.
Downsides: 

'ugly' URLs
Server-side rendering is not possible with this approach. As far as Search Engine Optimization (SEO) is concerned, your website consists of a single page with hardly any content on it.

.

### Catch-all

With this approach you do use Browser History, but just set up a catch-all on the server that sends `/*` to `index.html`, effectively giving you much the same situation as with Hash History. You do have clean URLs however and you could improve upon this scheme later without having to invalidate all your user's favorites.
Downsides: 

More complex to set up
Still no good SEO

.

### Hybrid

In the hybrid approach you expand upon the catch-all scenario by adding specific scripts for specific routes. You could make some simple PHP scripts to return the most important pages of your site with content included, so Googlebot can at least see what's on your page.
Downsides:

Even more complex to set up
Only good SEO for those routes you give the special treatment
Duplicating code for rendering content on server and client

.

### Isomorphic

What if we use Node JS as our server so we can run the same JS code on both ends? Now, we have all our routes defined in a single react-router config and we don't need to duplicate our rendering code. This is 'the holy grail' so to speak. The server sends the exact same markup as we would end up with if the page transition had happened on the client. This solution is optimal in terms of SEO.
Downsides:

Server must (be able to) run JS. I've experimented with Java i.c.w. Nashorn but it's not working for me. In practice it mostly means you must use a Node JS based server.
Many tricky environmental issues (using `window` on server-side etc)
Steep learning curve

.
Which should I use?
Choose the one that you can get away with. Personally I think the catch-all is simple enough to set up that that would be my minimum. This setup allows you to improve on things over time. If you are already using Node JS as your server platform, I'd definitely investigate doing an isomorphic app. Yes it's tough at first but once you get the hang of it it's actually a very elegant solution to the problem. 
So basically, for me, that would be the deciding factor. If my server runs on Node JS, I'd go isomorphic, otherwise I would go for the Catch-all solution and just expand on it (Hybrid solution) as time progresses and SEO requirements demand it.
If you'd like to learn more on isomorphic (also called 'universal') rendering with React, there are some good tutorials on the subject:

React to the future with isomorphic apps
The Pain and the Joy of creating isomorphic apps in ReactJS
How to Implement Node + React Isomorphic JavaScript & Why it Matters

Also, to get you started, I recommend looking at some starter kits. Pick one that matches your choices for the technology stack (remember, React is just the V in MVC, you need more stuff to build a full app). Start with looking at the one published by Facebook itself:

Create React App 

Or pick one of the many by the community. There is a nice site now that tries to index all of them:

Pick your perfect React starter project

I started with these:

React Isomorphic Starterkit
React Redux Universal Hot Example

Currently I am using a home-brew version of universal rendering that was inspired by the two starter kits above, but they are out of date now. 
Good luck with your quest!

## [ReactJS - Does render get called any time setState is called?](https://stackoverflow.com/questions/24718709/reactjs-does-render-get-called-any-time-setstate-is-called)

**270 Votes**, Brad Parks

Does React re-render all components and sub components every time setState is called?

By default - yes.
There is a method boolean shouldComponentUpdate(object nextProps, object nextState), each component has this method and it's responsible to determine "should component update (run render function)?" every time you change state or pass new props from parent component.
You can write your own implementation of shouldComponentUpdate method for your component, but default implementation always returns true - meaning always re-run render function.
Quote from official docs http://facebook.github.io/react/docs/component-specs.html#updating-shouldcomponentupdate

By default, shouldComponentUpdate always returns true to prevent
  subtle bugs when state is mutated in place, but if you are careful to
  always treat state as immutable and to read only from props and state
  in render() then you can override shouldComponentUpdate with an
  implementation that compares the old props and state to their
  replacements.

Next part of your question:

If so, why? I thought the idea was that React only rendered as little as needed - when state changed. 

There are two steps of what we may call "render":

Virtual DOM render: when render method is called it returns a new virtual dom structure of the component. As I mentioned before, this render method is called always when you call setState(), because shouldComponentUpdate always returns true by default. So, by default, there is no optimization here in React.
Native DOM render: React changes real DOM nodes in your browser only if they were changed in the Virtual DOM and as little as needed - this is that great React's feature which optimizes real DOM mutation and makes React fast.

## [What is the difference between state and props in React?](https://stackoverflow.com/questions/27991366/what-is-the-difference-between-state-and-props-in-react)

**267 Votes**, skaterdav85

Props and state are related. The state of one component will often become the props of a child component. Props are passed to the child within the render method of the parent as the second argument to `React.createElement()` or, if you're using JSX, the more familiar tag attributes.

```reactjs
<MyChild name={this.state.childsName} />
```

The parent's state value of `childsName` becomes the child's `this.props.name`. From the child's perspective, the name prop is immutable. If it needs to be changed, the parent should just change its internal state:

```reactjs
this.setState({ childsName: 'New name' });
```

and React will propagate it to the child for you. A natural follow-on question is: what if the child needs to change its name prop? This is usually done through child events and parent callbacks. The child might expose an event called, for example, `onNameChanged`. The parent would then subscribe to the event by passing a callback handler.

```reactjs
<MyChild name={this.state.childsName} onNameChanged={this.handleName} />
```

The child would pass its requested new name as an argument to the event callback by calling, e.g., `this.props.onNameChanged('New name')`, and the parent would use the name in the event handler to update its state.

```reactjs
handleName: function(newName) {
   this.setState({ childsName: newName });
}
```

## [Understanding unique keys for array children in React.js](https://stackoverflow.com/questions/28329382/understanding-unique-keys-for-array-children-in-react-js)

**267 Votes**, Brett DeWoody

You should add a key to each child as well as each element inside children.
This way React can handle the minimal DOM change. 
In your code, each `<TableRowItem key={item.id} data={item} columns={columnNames}/>` is trying to render some children inside them without a key.
Check this example.
Try removing the `key={i}` from the `<b></b>` element inside the div's (and check the console).
In the sample, if we don't give a key to the `<b>` element and we want to update only the `object.city`, React needs to re-render the whole row vs just the  element. 
Here is the code:

```reactjs
var data = [{name:'Jhon', age:28, city:'HO'},
            {name:'Onhj', age:82, city:'HN'},
            {name:'Nohj', age:41, city:'IT'}
           ];

var Hello = React.createClass({

    render: function() {

      var _data = this.props.info;
      console.log(_data);
      return(
        <div>
            {_data.map(function(object, i){
               return <div className={"row"} key={i}> 
                          {[ object.name ,
                             // remove the key
                             <b className="fosfo" key={i}> {object.city} </b> , 
                             object.age
                          ]}
                      </div>; 
             })}
        </div>
       );
    }
});

React.render(<Hello info={data} />, document.body);
```

React documentation on the importance of keys in reconciliation: Keys

## [Perform debounce in React.js](https://stackoverflow.com/questions/23123138/perform-debounce-in-react-js)

**261 Votes**, Chetan Ankola

The important part here is to create a single debounced (or throttled) function per component instance. You don't want to recreate the debounce (or throttle) function everytime, and you don't want either multiple instances to share the same debounced function.
I'm not defining debouncing function in this answer as it's not really relevant, but this answer will work perfectly fine with `_.debounce` of underscore or lodash, as well as user-provided debouncing function.


### NOT a good idea:


```reactjs
var SearchBox = React.createClass({
  method: function() {...},
  debouncedMethod: debounce(this.method,100);
});
```

It won't work, because during class description object creation, `this` is not the object created itself. `this.method` does not return what you expect because the `this` context is not the object itself (which actually does not really exist yet BTW as it is just being created).


### NOT a good idea:


```reactjs
var SearchBox = React.createClass({
  method: function() {...},
  debouncedMethod: function() {
      var debounced = debounce(this.method,100);
      debounced();
  },
});
```

This time you are effectively creating a debounced function that calls your `this.method`. The problem is that you are recreating it on every `debouncedMethod` call, so the newly created debounce function does not know anything about former calls! You must reuse the same debounced function over time or the debouncing will not happen.


### NOT a good idea:


```reactjs
var SearchBox = React.createClass({
  debouncedMethod: debounce(function () {...},100),
});
```

This is a little bit tricky here. 
All the mounted instances of the class will share the same debounced function, and most often this is not what you want!. See JsFiddle: 3 instances are producting only 1 log entry globally.
You have to create a debounced function for each component instance, and not a singe debounced function at the class level, shared by each component instance.

GOOD IDEA:
Because debounced functions are stateful, we have to create one debounced function per component instance.
ES6 (class property): recommended

```reactjs
class SearchBox extends React.Component {
    method = debounce(() => { 
      ...
    });
}
```

ES6 (class constructor)

```reactjs
class SearchBox extends React.Component {
    constructor(props) {
        super(props);
        this.method = debounce(this.method,1000);
    }
    method() { ... }
}
```

ES5

```reactjs
var SearchBox = React.createClass({
    method: function() {...},
    componentWillMount: function() {
       this.method = debounce(this.method,100);
    },
});
```

See JsFiddle: 3 instances are producting 1 log entry per instance (that makes 3 globally).

Take care of React's event pooling
This is related because we often want to debounce or throttle DOM events.
In React, the event objects (ie, `SyntheticEvent`) that you receive in callbacks are pooled (this is now documented). This means that after the event callback has be called, the SyntheticEvent you receive will be put back in the pool with empty attributes to reduce the GC pressure.
So if you access SyntheticEvent properties async to the original callback (as it may be the case if you throttle/debounce), the properties you access may be erased. If you want the event to never be put back in the pool, you can use the `persist()` method.
Without persist (default behavior: pooled event)

```reactjs
onClick = e => {
  alert(`sync -> hasNativeEvent=${!!e.nativeEvent}`);
  setTimeout(() => {
    alert(`async -> hasNativeEvent=${!!e.nativeEvent}`);
  }, 0);
};
```

The 2nd (async) will print `hasNativeEvent=false` because the event properties have been cleaned up.
With persist

```reactjs
onClick = e => {
  e.persist();
  alert(`sync -> hasNativeEvent=${!!e.nativeEvent}`);
  setTimeout(() => {
    alert(`async -> hasNativeEvent=${!!e.nativeEvent}`);
  }, 0);
};
```

The 2nd (async) will print `hasNativeEvent=true` because persist() permits to avoid putting back the event in the pool.
You can test these 2 behaviors here JsFiddle
Read Julen's answer for an example of using `persist()` with a throttle/debounce function.

## [Show or hide element in React](https://stackoverflow.com/questions/24502898/show-or-hide-element-in-react)

**257 Votes**, user1725382

The key is to update the state of the component in the click handler using `setState`. When the state changes get applied, the `render` method gets called again with the new state:

```reactjs
var Search = React.createClass({
    getInitialState: function() {
        return { showResults: false };
    },
    onClick: function() {
        this.setState({ showResults: true });
    },
    render: function() {
        return (
            <div>
                <input type="submit" value="Search" onClick={this.onClick} />
                { this.state.showResults ? <Results /> : null }
            </div>
        );
    }
});

var Results = React.createClass({
    render: function() {
        return (
            <div id="results" className="search-results">
                Some Results
            </div>
        );
    }
});

ReactDOM.render(<Search />, document.getElementById('container'));
```

http://jsfiddle.net/kb3gN/15084/

## [Parse Error: Adjacent JSX elements must be wrapped in an enclosing tag](https://stackoverflow.com/questions/31284169/parse-error-adjacent-jsx-elements-must-be-wrapped-in-an-enclosing-tag)

**245 Votes**, user1072337

You should put your component between an enclosing tag, Which mean:

```reactjs
//WRONG!

return (  
    <Comp1 />
    <Comp2 />
)
```

Instead:

```reactjs
//Correct

return (
    <div>
       <Comp1 />
       <Comp2 />
    </div>
)
```

## [react-router - pass props to handler component](https://stackoverflow.com/questions/27864720/react-router-pass-props-to-handler-component)

**243 Votes**, Kosmetika

UPDATE since new release, it's possible to pass props directly via the `Route` component, without using a Wrapper 
For example, by using `render` prop. Link to react router: https://reacttraining.com/react-router/web/api/Route/render-func
Code example at codesandbox: https://codesandbox.io/s/z3ovqpmp44
Component

```reactjs
    class Greeting extends React.Component {
        render() {
            const { text, match: { params } } = this.props;

            const { name } = params;

            return (
                <React.Fragment>
                    <h1>Greeting page</h1>
                    <p>
                        {text} {name}
                    </p>
                </React.Fragment>
            );
        }
    }
```

And usage

```reactjs
<Route path="/greeting/:name" render={(props) => <Greeting text="Hello, " {...props} />} />
```


OLD VERSION
My preferred way is wrap the `Comments` component and pass the wrapper as a route handler.
This is your example with changes applied:

```reactjs
var Dashboard = require('./Dashboard');
var Comments = require('./Comments');

var CommentsWrapper = React.createClass({
  render: function () {
    return (
        <Comments myprop="myvalue" />
    );
  }
});

var Index = React.createClass({
  render: function () {
    return (
        <div>
            <header>Some header</header>
            <RouteHandler />
        </div>
    );
  }
});

var routes = (
  <Route path="/" handler={Index}>
    <Route path="comments" handler={CommentsWrapper}/>
    <DefaultRoute handler={Dashboard}/>
  </Route>
);

ReactRouter.run(routes, function (Handler) {
  React.render(<Handler/>, document.body);
});
```

## [ReactJS Two components communicating](https://stackoverflow.com/questions/21285923/reactjs-two-components-communicating)

**242 Votes**, woutr_be

The best approach would depend on how you plan to arrange those components. A few example scenarios that come to mind right now:

`<Filters />` is a child component of `<List />`
Both `<Filters />` and `<List />` are children of a parent component
`<Filters />` and `<List />` live in separate root components entirely.

There may be other scenarios that I'm not thinking of. If yours doesn't fit within these, then let me know. Here are some very rough examples of how I've been handling the first two scenarios:

### Scenario #1

You could pass a handler from `<List />` to `<Filters />`, which could then be called on the `onChange` event to filter the list with the current value.
JSFiddle for #1 

```reactjs
/** @jsx React.DOM */

var Filters = React.createClass({
  handleFilterChange: function() {
    var value = this.refs.filterInput.getDOMNode().value;
    this.props.updateFilter(value);
  },
  render: function() {
    return <input type="text" ref="filterInput" onChange={this.handleFilterChange} placeholder="Filter" />;
  }
});

var List = React.createClass({
  getInitialState: function() {
    return {
      listItems: ['Chicago', 'New York', 'Tokyo', 'London', 'San Francisco', 'Amsterdam', 'Hong Kong'],
      nameFilter: ''
    };
  },
  handleFilterUpdate: function(filterValue) {
    this.setState({
      nameFilter: filterValue
    });
  },
  render: function() {
    var displayedItems = this.state.listItems.filter(function(item) {
      var match = item.toLowerCase().indexOf(this.state.nameFilter.toLowerCase());
      return (match !== -1);
    }.bind(this));

    var content;
    if (displayedItems.length > 0) {
      var items = displayedItems.map(function(item) {
        return <li>{item}</li>;
      });
      content = <ul>{items}</ul>
    } else {
      content = <p>No items matching this filter</p>;
    }

    return (
      <div>
        <Filters updateFilter={this.handleFilterUpdate} />
        <h4>Results</h4>
        {content}
      </div>
    );
  }
});

React.renderComponent(<List />, document.body);
```



### Scenario #2

Similar to scenario #1, but the parent component will be the one passing down the handler function to `<Filters />`, and will pass the filtered list to `<List />`. I like this method better since it decouples the `<List />` from the `<Filters />`.
JSFiddle for #2 

```reactjs
/** @jsx React.DOM */

var Filters = React.createClass({
  handleFilterChange: function() {
    var value = this.refs.filterInput.getDOMNode().value;
    this.props.updateFilter(value);
  },
  render: function() {
    return <input type="text" ref="filterInput" onChange={this.handleFilterChange} placeholder="Filter" />;
  }
});

var List = React.createClass({
  render: function() {
    var content;
    if (this.props.items.length > 0) {
      var items = this.props.items.map(function(item) {
        return <li>{item}</li>;
      });
      content = <ul>{items}</ul>
    } else {
      content = <p>No items matching this filter</p>;
    }
    return (
      <div className="results">
        <h4>Results</h4>
        {content}
      </div>
    );
  }
});

var ListContainer = React.createClass({
  getInitialState: function() {
    return {
      listItems: ['Chicago', 'New York', 'Tokyo', 'London', 'San Francisco', 'Amsterdam', 'Hong Kong'],
      nameFilter: ''
    };
  },
  handleFilterUpdate: function(filterValue) {
    this.setState({
      nameFilter: filterValue
    });
  },
  render: function() {
    var displayedItems = this.state.listItems.filter(function(item) {
      var match = item.toLowerCase().indexOf(this.state.nameFilter.toLowerCase());
      return (match !== -1);
    }.bind(this));

    return (
      <div>
        <Filters updateFilter={this.handleFilterUpdate} />
        <List items={displayedItems} />
      </div>
    );
  }
});

React.renderComponent(<ListContainer />, document.body);
```



### Scenario #3

When the components can't communicate between any sort of parent-child relationship, the documentation recommends setting up a global event system.

## [babel-loader jsx SyntaxError: Unexpected token [duplicate]](https://stackoverflow.com/questions/33460420/babel-loader-jsx-syntaxerror-unexpected-token)

**235 Votes**, Keyu Lin

Add "babel-preset-react"

```reactjs
npm install babel-preset-react
```

and add "presets" option to babel-loader in your webpack.config.js
(or you can add it to your .babelrc or package.js: http://babeljs.io/docs/usage/babelrc/)
Here is an example webpack.config.js:

```reactjs
{ 
    test: /\.jsx?$/,         // Match both .js and .jsx files
    exclude: /node_modules/, 
    loader: "babel", 
    query:
      {
        presets:['react']
      }
}
```

Recently Babel 6 was released and there was a major change:
https://babeljs.io/blog/2015/10/29/6.0.0
If you are using react 0.14, you should use `ReactDOM.render()` (from `require('react-dom')`) instead of `React.render()`: https://facebook.github.io/react/blog/#changelog
UPDATE 2018
Rule.query has already been deprecated in favour of Rule.options. Usage in webpack 4 is as follows:

```reactjs
npm install babel-loader babel-preset-react
```

Then in your webpack configuration (as an entry in the module.rules array in the module.exports object)

```reactjs
{
    test: /\.jsx?$/,
    exclude: /node_modules/,
    use: [
      {
        loader: 'babel-loader',
        options: {
          presets: ['react']
        }
      }
    ],
  }
```

## [How to conditionally add attributes to React components?](https://stackoverflow.com/questions/31163693/how-to-conditionally-add-attributes-to-react-components)

**232 Votes**, Remi Sture

Apparently, for certain attributes, React is intelligent enough to omit the attribute if the value you pass to it is not truthy. For example:

```reactjs
var InputComponent = React.createClass({
    render: function() {
        var required = true;
        var disabled = false;

        return (
            <input type="text" disabled={disabled} required={required} />
        );
    }
});
```

will result in:

```reactjs
<input type="text" required data-reactid=".0.0">
```

## [React after render code?](https://stackoverflow.com/questions/26556436/react-after-render-code)

**221 Votes**, Oscar Godson

https://facebook.github.io/react/docs/react-component.html#componentdidmount
This method is called once after your component is rendered. So your code would look like so.

```reactjs
var AppBase = React.createClass({
  componentDidMount: function() {
    var $this = $(ReactDOM.findDOMNode(this));
    // set el height and width etc.
  },

  render: function () {
    return (
      <div className="wrapper">
        <Sidebar />
          <div className="inner-wrapper">
            <ActionBar title="Title Here" />
            <BalanceBar balance={balance} />
            <div className="app-content">
              <List items={items} />
          </div>
        </div>
      </div>
    );
  }
});
```

## [React JSX: selecting selected on selected <select> option](https://stackoverflow.com/questions/21733847/react-jsx-selecting-selected-on-selected-select-option)

**219 Votes**, cantera

React automatically understands booleans for this purpose, so you can simply write (note: not recommended)

```reactjs
<option value={option.value} selected={optionsState == option.value}>{option.label}</option>
```

and it will output 'selected' appropriately.
However, React makes this even easier for you. Instead of defining `selected` on each option, you can (and should) simply write `value={optionsState}` on the select tag itself:

```reactjs
<select value={optionsState}>
  <option value="A">Apple</option>
  <option value="B">Banana</option>
  <option value="C">Cranberry</option>
</select>
```

More info at http://facebook.github.io/react/docs/forms.html#why-select-value.

## [Pass props to parent component in React.js](https://stackoverflow.com/questions/22639534/pass-props-to-parent-component-in-react-js)

**218 Votes**, KendallB

Edit: see the end examples for ES6 updated examples.
This answer simply handle the case of direct parent-child relationship. When parent and child have potentially a lot of intermediaries, check this answer.
Other solutions are missing the point
While they still work fine, other answers are missing something very important.

Is there not a simple way to pass a child's props to its parent using events, in React.js?

The parent already has that child prop!: if the child has a prop, then it is because its parent provided that prop to the child! Why do you want the child to pass back the prop to the parent, while the parent obviously already has that prop?
Better implementation
Child: it really does not have to be more complicated than that.

```reactjs
var Child = React.createClass({
  render: function () {
    return <button onClick={this.props.onClick}>{this.props.text}</button>;
  },
});
```

Parent with single child: using the value it passes to the child

```reactjs
var Parent = React.createClass({
  getInitialState: function() {
     return {childText: "Click me! (parent prop)"};
  },
  render: function () {
    return (
      <Child onClick={this.handleChildClick} text={this.state.childText}/>
    );
  },
  handleChildClick: function(event) {
     // You can access the prop you pass to the children 
     // because you already have it! 
     // Here you have it in state but it could also be
     //  in props, coming from another parent.
     alert("The Child button text is: " + this.state.childText);
     // You can also access the target of the click here 
     // if you want to do some magic stuff
     alert("The Child HTML is: " + event.target.outerHTML);
  }
});
```

JsFiddle
Parent with list of children: you still have everything you need on the parent and don't need to make the child more complicated.

```reactjs
var Parent = React.createClass({
  getInitialState: function() {
     return {childrenData: [
         {childText: "Click me 1!", childNumber: 1},
         {childText: "Click me 2!", childNumber: 2}
     ]};
  },
  render: function () {
    var children = this.state.childrenData.map(function(childData,childIndex) {
        return <Child onClick={this.handleChildClick.bind(null,childData)} text={childData.childText}/>;
    }.bind(this));
    return <div>{children}</div>;
  },

  handleChildClick: function(childData,event) {
     alert("The Child button data is: " + childData.childText + " - " + childData.childNumber);
     alert("The Child HTML is: " + event.target.outerHTML);
  }
});
```

JsFiddle
It is also possible to use `this.handleChildClick.bind(null,childIndex)` and then use `this.state.childrenData[childIndex]`
Note we are binding with a `null` context because otherwise React issues a warning related to its autobinding system. Using null means you don't want to change the function context. See also.
About encapsulation and coupling in other answers
This is for me a bad idea in term of coupling and encapsulation:

```reactjs
var Parent = React.createClass({
  handleClick: function(childComponent) {
     // using childComponent.props
     // using childComponent.refs.button
     // or anything else using childComponent
  },
  render: function() {
    <Child onClick={this.handleClick} />
  }
});
```

Using props:
As I explained above, you already have the props in the parent so it's useless to pass the whole child component to access props.
Using refs: 
You already have the click target in the event, and in most case this is enough. 
Additionnally, you could have used a ref directly on the child:

```reactjs
<Child ref="theChild" .../>
```

And access the DOM node in the parent with

```reactjs
React.findDOMNode(this.refs.theChild)
```

For more advanced cases where you want to access multiple refs of the child in the parent, the child could pass all the dom nodes directly in the callback.
The component has an interface (props) and the parent should not assume anything about the inner working of the child, including its inner DOM structure or which DOM nodes it declares refs for. A parent using a ref of a child means that you tightly couple the 2 components.
To illustrate the issue, I'll take this quote about the Shadow DOM, that is used inside browsers to render things like sliders, scrollbars, video players...:

They created a boundary between what you, the Web developer can reach
  and whats considered implementation details, thus inaccessible to
  you. The browser however, can traipse across this boundary at will.
  With this boundary in place, they were able to build all HTML elements
  using the same good-old Web technologies, out of the divs and spans
  just like you would.

The problem is that if you let the child implementation details leak into the parent, you make it very hard to refactor the child without affecting the parent. This means as a library author (or as a browser editor with Shadow DOM) this is very dangerous because you let the client access too much, making it very hard to upgrade code without breaking retrocompatibility.
If Chrome had implemented its scrollbar letting the client access the inner dom nodes of that scrollbar, this means that the client may have the possibility to simply break that scrollbar, and that apps would break more easily when Chrome perform its auto-update after refactoring the scrollbar... Instead, they only give access to some safe things like customizing some parts of the scrollbar with CSS.
About using anything else
Passing the whole component in the callback is dangerous and may lead novice developers to do very weird things like calling `childComponent.setState(...)` or `childComponent.forceUpdate()`, or assigning it new variables, inside the parent, making the whole app much harder to reason about.

Edit: ES6 examples
As many people now use ES6, here are the same examples for ES6 syntax
The child can be very simple:

```reactjs
const Child = ({
  onClick, 
  text
}) => (
  <button onClick={onClick}>
    {text}
  </button>
)
```

The parent can be either a class (and it can eventually manage the state itself, but I'm passing it as props here:

```reactjs
class Parent1 extends React.Component {
  handleChildClick(childData,event) {
     alert("The Child button data is: " + childData.childText + " - " + childData.childNumber);
     alert("The Child HTML is: " + event.target.outerHTML);
  }
  render() {
    return (
      <div>
        {this.props.childrenData.map(child => (
          <Child
            key={child.childNumber}
            text={child.childText} 
            onClick={e => this.handleChildClick(child,e)}
          />
        ))}
      </div>
    );
  }
}
```

But it can also be simplified if it does not need to manage state:

```reactjs
const Parent2 = ({childrenData}) => (
  <div>
     {childrenData.map(child => (
       <Child
         key={child.childNumber}
         text={child.childText} 
         onClick={e => {
            alert("The Child button data is: " + child.childText + " - " + child.childNumber);
                    alert("The Child HTML is: " + e.target.outerHTML);
         }}
       />
     ))}
  </div>
)
```

JsFiddle

PERF WARNING (apply to ES5/ES6): if you are using `PureComponent` or `shouldComponentUpdate`, the above implementations will not be optimized by default because using `onClick={e => doSomething()}`, or binding directly during the render phase, because it will create a new function everytime the parent renders. If this is a perf bottleneck in your app, you can pass the data to the children, and reinject it inside "stable" callback (set on the parent class, and binded to `this` in class constructor) so that `PureComponent` optimization can kick in, or you can implement your own `shouldComponentUpdate` and ignore the callback in the props comparison check.
You can also use Recompose library, which provide higher order components to achieve fine-tuned optimisations:

```reactjs
// A component that is expensive to render
const ExpensiveComponent = ({ propA, propB }) => {...}

// Optimized version of same component, using shallow comparison of props
// Same effect as React's PureRenderMixin
const OptimizedComponent = pure(ExpensiveComponent)

// Even more optimized: only updates if specific prop keys have changed
const HyperOptimizedComponent = onlyUpdateForKeys(['propA', 'propB'])(ExpensiveComponent)
```

In this case you could optimize the Child component by using:

```reactjs
const OptimizedChild = onlyUpdateForKeys(['text'])(Child)
```

## [How to have conditional elements and keep DRY with Facebook React's JSX?](https://stackoverflow.com/questions/22538638/how-to-have-conditional-elements-and-keep-dry-with-facebook-reacts-jsx)

**214 Votes**, Jack Allan

Just leave banner as being undefined and it does not get included.

## [What could be the downsides of using Redux instead of Flux](https://stackoverflow.com/questions/32021763/what-could-be-the-downsides-of-using-redux-instead-of-flux)

**214 Votes**, Ivan Wang

Redux author here!
I'd like to say you're going to make the following compromises using it:

You'll need to learn to avoid mutations. Flux is unopinionated about mutating data, but Redux doesn't like mutations and many packages complementary to Redux assume you never mutate the state. You can enforce this with dev-only packages like redux-immutable-state-invariant, use Immutable.js, or trust yourself and your team to write non-mutative code, but it's something you need to be aware of, and this needs to be a conscious decision accepted by your team.
You're going to have to carefully pick your packages. While Flux explicitly doesn't try to solve nearby problems such as undo/redo, persistence, or forms, Redux has extension points such as middleware and store enhancers, and it has spawned a young but rich ecosystem. This means most packages are new ideas and haven't received the critical mass of usage yet. You might depend on something that will be clearly a bad idea a few months later on, but it's hard to tell just yet.
You won't have a nice Flow integration yet. Flux currently lets you do very impressive static type checks which Redux doesn't support yet. We'll get there, but it will take some time.

I think the first is the biggest hurdle for the beginners, the second can be a problem for over-enthusiastic early adopters, and the third is my personal pet peeve. Other than that, I don't think using Redux brings any particular downsides that Flux avoids, and some people say it even has some upsides compared to Flux.

See also my answer on upsides of using Redux.

## [React JSX: Access Props in Quotes](https://stackoverflow.com/questions/21668025/react-jsx-access-props-in-quotes)

**207 Votes**, cantera

React (or JSX) doesn't support variable interpolation inside an attribute value, but you can put any JS expression inside curly braces as the entire attribute value, so this works:

```reactjs
<img className="image" src={"images/" + this.props.image} />
```

## [Correct modification of state arrays in ReactJS](https://stackoverflow.com/questions/26253351/correct-modification-of-state-arrays-in-reactjs)

**205 Votes**, fadedbee

The React docs says:

Treat this.state as if it were immutable.

Your `push` will mutate the state directly and that could potentially lead to error prone code, even if you are "resetting" the state again afterwards. F.ex, it could lead to that some lifecycle methods like `componentDidUpdate` wont trigger.
The recommended approach in later React versions is to use an updater function when modifying states to prevent race conditions:

```reactjs
this.setState(prevState => ({
  arrayvar: [...prevState.arrayvar, newelement]
}))
```

The memory "waste" is not an issue compared to the errors you might face using non-standard state modifications.
Alternative syntax for earlier React versions
You can use `concat` to get a clean syntax since it returns a new array:

```reactjs
this.setState({ 
  arrayvar: this.state.arrayvar.concat([newelement])
})
```

In ES6 you can use the Spread Operator:

```reactjs
this.setState({
  arrayvar: [...this.state.arrayvar, newelement]
})
```

## [Hide keyboard in react-native](https://stackoverflow.com/questions/29685421/hide-keyboard-in-react-native)

**196 Votes**, MrMuetze

The problem with keyboard not dismissing gets more severe if you have `keyboardType='numeric'`, as there is no way to dismiss it.
Replacing View with ScrollView is not a correct solution, as if you have multiple `textInput`s or `button`s, tapping on them while the keyboard is up will only dismiss the keyboard.
Correct way is to encapsulate View with `TouchableWithoutFeedback` and calling `Keyboard.dismiss()`
If you have

```reactjs
<View style={styles.container}>
    <TextInput keyboardType='numeric'/>
</View>
```

Change it to

```reactjs
import {Keyboard} from 'react-native'

<TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
    <View style={styles.container}>
        <TextInput keyboardType='numeric'/>
    </View>
</TouchableWithoutFeedback>
```

EDIT: You can also create a Higher Order Component to dismiss the keyboard.

```reactjs
import React from 'react';
import { TouchableWithoutFeedback, Keyboard } from 'react-native';

const DismissKeyboardHOC (Comp) => {
  return ({ children, ...props }) => (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
      <Comp {...props}>
        {children}
      </Comp>
    </TouchableWithoutFeedback>
  );
};
```

Simply use it like this

```reactjs
const DismissKeyboardView = DismissKeyboardHOC(View)
...
render() {
    <DismissKeyboardView>
        ...
    </DismissKeyboardView>
}
```

NOTE: the `accessible={false}` is required to make the input form continue to be accessible through VoiceOver. Visually impaired people will thank you!

## [What is mapDispatchToProps?](https://stackoverflow.com/questions/39419237/what-is-mapdispatchtoprops)

**191 Votes**, Code Whisperer

I feel like none of the answers have crystallized why `mapDispatchToProps` is useful.
This can really only be answered in the context of the `container-component` pattern, which I found best understood by first reading:
https://medium.com/@learnreact/container-components-c0e67432e005#.1a9j3w1jl
then
http://redux.js.org/docs/basics/UsageWithReact.html
In a nutshell, your `components` are supposed to be concerned only with displaying stuff.   The only place they are supposed to get information from is their props.
Separated out from this is the concern about:

how you get the stuff to display, 
and how you handle events.  

That is what `containers` are for.
Therefore, a "well designed" `component` in the pattern look like this:

```reactjs
class FancyAlerter extends Component {
    sendAlert = () => {
        this.props.sendTheAlert()
    }

    render() {
        <div>
          <h1>Today's Fancy Alert is {this.props.fancyInfo}</h1>
          <Button onClick={sendAlert}/>
        </div>
     }}
```

See how this component gets the info it displays from props (which came from the redux store via `mapStateToProps`) and it also gets its action function from its props: `sendTheAlert()`.
That's where `mapDispatchToProps` comes in: in the corresponding `container`
`FancyButtonContainer.js`

```reactjs
function mapDispatchToProps(dispatch) {
    return({
        sendTheAlert: () => {dispatch(ALERT_ACTION)}
    })
}

function mapStateToProps(state} {
    return({fancyInfo: "Fancy this:" + state.currentFunnyString})
}

export const FancyButtonContainer = connect(
    mapStateToProps, mapDispatchToProps)(
    FancyAlerter
)
```

I wonder if you can see, now that it's the `container` [1] that knows about redux and dispatch and store and state and ... stuff.
The `component` in the pattern, `FancyAlerter`, which does the rendering doesn't need to know about any of that stuff: it gets its method to call at `onClick` of the button, via its props.
And ... `mapDispatchToProps` was the useful means that redux provides to let the container easily pass that function into the wrapped component on its props.
All this looks very like the todo example in docs, and another answer here, but I have tried to cast it in the light of the pattern to emphasize why.
(Note: you can't use `mapStateToProps` for the same purpose as `mapDispatchToProps` for the basic reason that you don't have access to `dispatch` inside `mapStateToProp`.  So you couldn't use `mapStateToProps` to give the wrapped component a method that uses `dispatch`.   
I don't know why they chose to break it into two mapping functions - it might have been tidier to have `mapToProps(state, dispatch, props)`   IE one function to do both!

[1]  Note that I deliberately explicitly named the container `FancyButtonContainer`,  to highlight that it is a "thing" - the identity (and hence existence!) of the container as "a thing" is sometimes lost in the shorthand 
`export default connect(...)` 
syntax that is shown in most examples

## [Where should ajax request be made in Flux app?](https://stackoverflow.com/questions/26632415/where-should-ajax-request-be-made-in-flux-app)

**188 Votes**, Eniz Glek

I'm a big proponent of putting async write operations in the action creators and async read operations in the store. The goal is to keep the store state modification code in fully synchronous action handlers; this makes them simple to reason about and simple to unit test. In order to prevent multiple simultaneous requests to the same endpoint (for example, double-reading), I'll move the actual request processing into a separate module that uses promises to prevent the multiple requests; for example:

```reactjs
class MyResourceDAO {
  get(id) {
    if (!this.promises[id]) {
      this.promises[id] = new Promise((resolve, reject) => {
        // ajax handling here...
      });
    } 
    return this.promises[id];
  }
}
```

While reads in the store involve asynchronous functions, there is an important caveat that the stores don't update themselves in the async handlers, but instead fire an action and only fire an action when the response arrives. Handlers for this action end up doing the actual state modification.
For example, a component might do:

```reactjs
getInitialState() {
  return { data: myStore.getSomeData(this.props.id) };
}
```

The store would have a method implemented, perhaps, something like this:

```reactjs
class Store {
  getSomeData(id) {
    if (!this.cache[id]) {
      MyResurceDAO.get(id).then(this.updateFromServer);
      this.cache[id] = LOADING_TOKEN;
      // LOADING_TOKEN is a unique value of some kind
      // that the component can use to know that the
      // value is not yet available.
    }

    return this.cache[id];
  }

  updateFromServer(response) {
    fluxDispatcher.dispatch({
      type: "DATA_FROM_SERVER",
      payload: {id: response.id, data: response}
    });
  }

  // this handles the "DATA_FROM_SERVER" action
  handleDataFromServer(action) {
    this.cache[action.payload.id] = action.payload.data;
    this.emit("change"); // or whatever you do to re-render your app
  }
}
```

## [Programmatically navigate using react router V4](https://stackoverflow.com/questions/42123261/programmatically-navigate-using-react-router-v4)

**187 Votes**, Colin Witkamp

If you are targeting browser environments, you need to use `react-router-dom` package, instead of `react-router`. They are following the same approach as React did, in order to separate the core, (`react`) and the platform specific code, (`react-dom`, `react-native` ) with the subtle difference that you don't need to install two separate packages, so the environment packages contain everything you need. You can add it to your project as:
`yarn add react-router-dom`
or
`npm i -S react-router-dom`
The first thing you need to do is to provide a `<BrowserRouter>` as the top most parent component in your application. `<BrowserRouter>` uses the HTML5 `history` API and manages it for you, so you don't have to worry about instantiating it yourself and passing it down to the `<BrowserRouter>` component as a prop (as you needed to do in previous versions). 
In V4, for navigating programatically you need to access the `history` object, which is available through React `context`, as long as you have a `<BrowserRouter>` provider component as the top most parent in your application. The library exposes through context the `router` object, that itself contains `history` as a property. The `history` interface offers several navigation methods, such as `push`, `replace` and `goBack`, among others. You can check the whole list of properties and methods here.

### Important Note to Redux/Mobx users

If you are using redux or mobx as your state management library in your application, you may have come across issues with components location-aware that are not re-rendered after triggering an URL update
That's happening because `react-router` passes `location` to components using the context model.

Both connect and observer create components whose shouldComponentUpdate methods do a shallow comparison of their current props and their next props. Those components will only re-render when at least one prop has changed. This means that in order to ensure they update when the location changes, they will need to be given a prop that changes when the location changes.

The 2 approaches for solving this are:

Wrap your connected component in a pathless `<Route />`. The current `location` object is one of the props that a `<Route>` passes to the component it renders
Wrap your connected component with the `withRouter` higher-order component, that in fact has the same effect and injects `location` as a prop  

Setting that aside, there are four ways to navigate programatically, ordered by recommendation:
1.- Using a `<Route>` Component It promotes a declarative style. Prior to v4, `<Route />` components were placed at the top of your component hierarchy, having to think of your routes structure beforehand. However, now you can have `<Route>` components anywhere in your tree, allowing you to have a finer control for conditionally rendering depending on the URL. `Route` injects `match`, `location` and `history` as props into your component. The navigation methods (such as `push`, `replace`, `goBack`...) are available as properties of the `history` object.
There are 3 ways to render something with a `Route`, by using either `component`, `render` or `children` props, but don't use more than one in the same `Route`. The choice depends on the use case, but basically the first two options will only render your component if the `path` matches the url location, whereas with `children` the component will be rendered whether the path matches the location or not (useful for adjusting the UI based on URL matching).
If you want to customise your component rendering output, you need to wrap your component in a function and use the `render` option, in order to pass to your component any other props you desire, apart from `match`, `location` and `history`. An example to illustrate:

```reactjs
import { BrowserRouter as Router } from 'react-router-dom'

const ButtonToNavigate = ({ title, history }) => (
  <button
    type="button"
    onClick={() => history.push('/my-new-location')}
  >
    {title}
  </button>
);

const SomeComponent = () => (
  <Route path="/" render={(props) => <ButtonToNavigate {...props} title="Navigate elsewhere" />} />
)    

const App = () => (
  <Router>
    <SomeComponent /> // Notice how in v4 we can have any other component interleaved
    <AnotherComponent />
  </Router>
);
```

2.- Using `withRouter` HoC
This higher order component will inject the same props as `Route`. However, it carries along the limitation that you can have only 1 HoC per file.

```reactjs
import { withRouter } from 'react-router-dom'

const ButtonToNavigate = ({ history }) => (
  <button
    type="button"
    onClick={() => history.push('/my-new-location')}
  >
    Navigate
  </button>
);


ButtonToNavigate.propTypes = {
  history: React.PropTypes.shape({
    push: React.PropTypes.func.isRequired,
  }),
};

export default withRouter(ButtonToNavigate);
```

3.- Using a `Redirect` component Rendering a `<Redirect>` will navigate to a new location. But keep in mind that, by default, the current location is replaced by the new one, like server-side redirects (HTTP 3xx). The new location is provided by `to` prop, that can be a string (URL to redirect to) or a `location` object. If you want to push a new entry onto the history instead, pass a `push` prop as well and set it to `true`

```reactjs
<Redirect to="/your-new-location" push />
```

4.- Accessing `router` manually through context A bit discouraged because context is still an experimental API and it is likely to break/change in future releases of React

```reactjs
const ButtonToNavigate = (props, context) => (
  <button
    type="button"
    onClick={() => context.router.history.push('/my-new-location')}
  >
    Navigate to a new location
  </button>
);

ButtonToNavigate.contextTypes = {
  router: React.PropTypes.shape({
    history: React.PropTypes.object.isRequired,
  }),
};
```

Needless to say there are also other Router components that are meant to be for non browser ecosystems, such as `<NativeRouter>` that replicates a navigation stack in memory and targets React Native platform, available through `react-router-native` package.
For any further reference, don't hesitate to take a look at the official docs. There is also a video made by one of the co-authors of the library that provides a pretty cool introduction to react-router v4, highlighting some of the major changes.

## [Why calling react setState method doesn't mutate the state immediately?](https://stackoverflow.com/questions/30782948/why-calling-react-setstate-method-doesnt-mutate-the-state-immediately)

**184 Votes**, tarrsalah

From React's documentation:

`setState()` does not immediately mutate `this.state` but creates a
  pending state transition. Accessing `this.state` after calling this
  method can potentially return the existing value. There is no
  guarantee of synchronous operation of calls to `setState` and calls may
  be batched for performance gains.

If you want a function to be executed after the state change occurs, pass it in as a callback.

```reactjs
this.setState({value: event.target.value}, function () {
    console.log(this.state.value);
});
```

## [What's the '@' (at symbol) in the Redux @connect decorator?](https://stackoverflow.com/questions/32646920/whats-the-at-symbol-in-the-redux-connect-decorator)

**174 Votes**, 

The ``@ symbol is in fact a JavaScript expression currently proposed to signify decorators:

Decorators make it possible to annotate and modify classes and properties at design time.

Here's an example of setting up Redux without and with a decorator:
Without a decorator

```reactjs
import React from 'react';
import * as actionCreators from './actionCreators';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

function mapStateToProps(state) {
  return { todos: state.todos };
}

function mapDispatchToProps(dispatch) {
  return { actions: bindActionCreators(actionCreators, dispatch) };
}

class MyApp extends React.Component {
  // ...define your main app here
}

export default connect(mapStateToProps, mapDispatchToProps)(MyApp);
```

Using a decorator

```reactjs
import React from 'react';
import * as actionCreators from './actionCreators';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

function mapStateToProps(state) {
  return { todos: state.todos };
}

function mapDispatchToProps(dispatch) {
  return { actions: bindActionCreators(actionCreators, dispatch) };
}

@connect(mapStateToProps, mapDispatchToProps)
export default class MyApp extends React.Component {
  // ...define your main app here
}
```

Both examples above are equivalent, it's just a matter of preference. Also, the decorator syntax isn't built into any Javascript runtimes yet, and is still experimental and subject to change. If you want to use it, it is available using Babel.

## [What do multiple arrow functions mean in javascript?](https://stackoverflow.com/questions/32782922/what-do-multiple-arrow-functions-mean-in-javascript)

**171 Votes**, jhamm

That is a curried function
First, examine this function with two parameters 

```reactjs
let add = (x,y) => x + y;
add(2,3); //=> 5
```

Here it is again in curried form 

```reactjs
let add = x => y => x + y;
```

Here is the same code1 without arrow functions 

```reactjs
let add = function (x) {
  return function (y) {
    return x + y;
  };
};
```


Focus on `return`
It might help to visualize it another way. We know that arrow functions work like this  let's pay particular attention to the return value.

```reactjs
let f = someParam => returnValue```

So our `add` function returns a function  we can use parentheses for added clarity. The bolded text is the return value of our function `add`

```reactjs
let add = x => (y => x + y)```

In other words `add` of some number ``x returns a function

```reactjs
let x = 2;
add (2) // returns (y => 2 + y)
```


Calling curried functions
So in order to use our curried function, we have to call it a bit differently 

```reactjs
add(2)(3); // returns 5
```

This is because the first (outer) function call returns a second (inner) function. Only after we call the second function do we actually get the result. This is more evident if we separate the calls on two lines 

```reactjs
let add2 = add(2); // returns function(y) { return 2 + y }
add2(3);           // returns 5
```


Applying our new understanding to your code

related: Whats the difference between binding, partial application, and currying?

OK, now that we understand how that works, let's look at your code

```reactjs
handleChange = field => e => {
  e.preventDefault();
  /// Do something here
}
```

We'll start by representing it without using arrow functions 

```reactjs
handleChange = function(field) {
  return function(e) {
    e.preventDefault();
    // Do something here
    // return ...
  };
};
```

However, because arrow functions lexically bind `this`, it would actually look more like this 

```reactjs
handleChange = function(field) {
  return function(e) {
    e.preventDefault();
    // Do something here
    // return ...
  }.bind(this);
}.bind(this);
```

Maybe now we can see what this is doing more clearly. The `handleChange` function is creating a function for a specified `field`. This is a handy React technique because you're required to setup your own listeners on each input in order to update your applications state. By using the `handleChange` function, we can eliminate all the duplicated code that would result in setting up `change` listeners for each field.
Cool !

1 Here I did not have to lexically bind `this` because the original `add` function does not use any context, so it is not important to preserve it in this case.

## [Rerender view on browser resize with React](https://stackoverflow.com/questions/19014250/rerender-view-on-browser-resize-with-react)

**156 Votes**, digibake

You can listen in componentDidMount, something like this component which just displays the window dimensions (like `<span>1024 x 768</span>`):

```reactjs
var WindowDimensions = React.createClass({
    render: function() {
        return <span>{this.state.width} x {this.state.height}</span>;
    },
    updateDimensions: function() {
        this.setState({width: $(window).width(), height: $(window).height()});
    },
    componentWillMount: function() {
        this.updateDimensions();
    },
    componentDidMount: function() {
        window.addEventListener("resize", this.updateDimensions);
    },
    componentWillUnmount: function() {
        window.removeEventListener("resize", this.updateDimensions);
    }
});
```
