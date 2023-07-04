今天我们来学习JavaScript新的原始类型`Symbol`，我们可以使用Symbol来创建唯一值作为对象属性或者值，也可以通过`Symbol`的`well-known`来修改JS语言内部的逻辑。

## 创建Symbol

ES6新增了`Symbol`作为原始数据类型，和其他原始数据类型，像number、boolean、null、undefined、string，symbol类型没有文字形式。

创建一个symbol，我们要使用全局函数`Symbol()`

```javascript
let s = Symbol('foo');

```

`Symbol()` 函数每次调用会创建一个新的唯一值

```javascript
console.log(Symbol() === Symbol()); // false

```

`Symbol()` 函数接受一个可选参数作为描述，这样使Symbol更具有语义性。

下面创建两个symbol分别为: `firstName` and `lastName`.

```javascript
let firstName = Symbol('first name'),
    lastName = Symbol('last name');

```

当我们使用console.log()去打印symbol的时候会隐式调用symbol的toString()方法。

```javascript
console.log(firstName); // Symbol(first name)
console.log(lastName); // Symbol(last name)

```

由于symbol为原始值，我们可以使用`typeof`去检查它的类型，同样ES6拓展了typeof关键字，在遇到symbol类型时会返回symbol

```javascript
console.log(typeof firstName); 
// symbol

```

由于是原始类型，也不能使用new去创建

```javascript
let s = new Symbol(); // error

```

## 共享 symbol

要创建一个共享的symbol，要使用`Symbol.for()`函数，而不是`Symbol()`。

`Symbol.for()` 也接受一个可选参数作为描述

```javascript
let ssn = Symbol.for('ssn');

```

`Symbol.for()` 会首先在全局中查找是否有已经创建的`ssn`的symbol，如果有就会返回已经创建的symbol，如果没有就会创建一个新的symbol。

接下来，我们创建一个相同的symbol，然后看看不是同一个symbol

```javascript
let nz = Symbol.for('ssn');
console.log(ssn === nz); // true

```

因为上面已经创建`ssn`的symbol，所以nz变量的symbol和上面创建的将是同一个。

如果想要获取symbol的键，使用Symbol.keyFor()方法

```javascript
console.log(Symbol.keyFor(nz)); // 'ssn'

```

注意，如果symbol是通过`Symbol()`创建的，使用`Symbol.keyFor()`会返回undefined

```javascript
let systemID = Symbol('sys');
console.log(Symbol.keyFor(systemID)); // undefined

```

## Symbol 有啥用

### 一) 使用Symbol作唯一值

我们在代码中经常会用字符串或者数字去表示一些状态，也经常会面临缺乏语义性或者重复定义的问题，这时使用Symbol是最好的选择，每次新创建的Symbol都是唯一的，不会产生重复，而且我们可以给Symbol传入相应的描述。

看下面的例子，我们使用Symbol来表达订单的几种状态，而不是字符串和数字

```javascript
let statuses = {
    OPEN: Symbol('已下单'),
    IN_PROGRESS: Symbol('配送中'),
    COMPLETED: Symbol('订单完成'),
    CANCELED: Symbol('订单取消')
};

// 完成订单
task.setStatus(statuses.COMPLETED);

```

### 二) 使用 symbol 作为对象属性

使用`Symbol`作为属性名称

```javascript
let statuses = {
    OPEN: Symbol('已下单'),
    IN_PROGRESS: Symbol('配送中'),
    COMPLETED: Symbol('订单完成'),
    CANCELED: Symbol('订单取消')
};

let status = Symbol('status');

let task = {
    [status]: statuses.OPEN,
    description: '学习 ES6 Symbol'
};

console.log(task);

```

使用`Object.keys()`获取对象的所有可枚举属性

```javascript
console.log(Object.keys(task));
// ["description"]

```

使用`Object.getOwnPropertyNames()` 获取所有属性，无论是否是可枚举

```javascript
console.log(Object.getOwnPropertyNames(task));
// ["description"]

```

那么要获取对象中的Symbol属性，需要使用ES6新增的`Object.getOwnPropertySymbols()`方法

```javascript
console.log(Object.getOwnPropertySymbols(task));
//[Symbol(status)]

```

`Object.defineProperty()/Object.defineProperties()`方法

```
let s1 = Symbol('foo'),
s2 = Symbol('bar'),
s3 = Symbol('baz'),
s4 = Symbol('qux');
let o = {
[s1]: 'foo val'
};
// 这样也可以：o[s1] = 'foo val';
console.log(o);
// {Symbol(foo): foo val}
Object.defineProperty(o, s2, {value: 'bar val'});
console.log(o);
// {Symbol(foo): foo val, Symbol(bar): bar val}
Object.defineProperties(o, {
[s3]: {value: 'baz val'},
[s4]: {value: 'qux val'}
});
console.log(o);
// {Symbol(foo): foo val, Symbol(bar): bar val,
// Symbol(baz): baz val, Symbol(qux): qux val}
```

`Object.getOwnProperty-Descriptors()`会返回同时包含常规和符号属性描述符的对象。

`Reflect.ownKeys()`会返回两种类型的键：

```
let s1 = Symbol('foo'),
s2 = Symbol('bar');
let o = {
[s1]: 'foo val',
[s2]: 'bar val',
baz: 'baz val',
qux: 'qux val'
};
console.log(Object.getOwnPropertySymbols(o));
// [Symbol(foo), Symbol(bar)]
console.log(Object.getOwnPropertyNames(o));
// ["baz", "qux"]
console.log(Object.getOwnPropertyDescriptors(o));
// {baz: {...}, qux: {...}, Symbol(foo): {...}, Symbol(bar): {...}}
console.log(Reflect.ownKeys(o));
// ["baz", "qux", Symbol(foo), Symbol(bar)]
```

因为符号属性是对内存中符号的一个引用，所以直接创建并用作属性的符号不会丢失。但是，如果
没有显式地保存对这些属性的引用，那么必须遍历对象的所有符号属性才能找到相应的属性键：

```
let o = {
[Symbol('foo')]: 'foo val',
[Symbol('bar')]: 'bar val'
};
console.log(o);
// {Symbol(foo): "foo val", Symbol(bar): "bar val"}
let barSymbol = Object.getOwnPropertySymbols(o)
.find((symbol) => symbol.toString().match(/bar/));
console.log(barSymbol);
// Symbol(bar)
```



## 常用内置符号：Well-known symbol

ES6在原型链上定义了与 `Symbol` 相关的属性来暴露更多的语言内部逻辑。`well-known Symbol` 为标准对象定义了一些以前只在语言内部可见的功能。

### Symbol.asyncIterator

表示“一个方法，该方法返回对象默认的 AsyncIterator。由 for-await-of 语句使用”。

换句话说，这个符号表示实现异步迭代器 API 的函数

```
class Emitter {
constructor(max) {
this.max = max;
this.asyncIdx = 0;
}
async *[Symbol.asyncIterator]() {
while(this.asyncIdx < this.max) {
yield new Promise((resolve) => resolve(this.asyncIdx++));
}
}
}
async function asyncCount() {
let emitter = new Emitter(5);
for await(const x of emitter) {
console.log(x);
}
}
asyncCount();
// 0
// 1
// 2
// 3
// 4
```



### Symbol.hasInstance

`Symbol.hasInstance` 是一个改变`instanceof`操作符默认行为的symbol，通常我们会这样使用`instanceof
obj instanceof type;

那么JavaScript 就会执行 `Symbol.hasIntance` 方法，像下面这样

```ini
type[Symbol.hasInstance](obj);

```

它会调用type的`Symbol.hasInstance`静态方法，将obj作为参数

```javascript
class Stack {
}
console.log([] instanceof Stack);
// false

```

`[]` 数组不是Stack类所创建的实例，所以返回false。

假设要使`[]` 数组是Stack类所创建的实例，返回true，我们可以重写Symbol.hasInstance的方法

```javascript
class Stack {
    static [Symbol.hasInstance](obj) {
        return Array.isArray(obj);
    }
}
console.log([] instanceof Stack);
// true

```

### Symbol.iterator

`Symbol.iterator` 指定函数是否会返回对象的迭代器。

具有 `Symbol.iterator` 属性的对象称为可迭代对象。

在ES6中，Array、Set、Map和string都是可迭代对象。

ES6提供了for...of循环，它可以用在可迭代对象上。

```javascript
var numbers = [1, 2, 3];
for (let num of numbers) {
    console.log(num);
}

// 1
// 2
// 3

```

在背后，JavaScript引擎首先调用`numbers`数组的 `Symbol.iterator` 方法来获取迭代器对象，然后它调用 `iterator.next()` 方法并将迭代器对象的value属性复制到`num`变量中，3次迭代后，对象的`done `属性为`true`，循环推出。

我们可以通过`Symbol.iterator`来获取数组的迭代器对象。

```javascript
var iterator = numbers[Symbol.iterator]();

console.log(iterator.next()); // Object {value: 1, done: false}
console.log(iterator.next()); // Object {value: 2, done: false}
console.log(iterator.next()); // Object {value: 3, done: false}
console.log(iterator.next()); // Object {value: undefined, done: true}

```

默认情况下，一个自己定义的集合是不可以迭代的，但是我们可以用Symbol.iterator使其可迭代

```javascript
class List {
  constructor() {
    this.elements = [];
  }

  add(element) {
    this.elements.push(element);
    return this;
  }

  *[Symbol.iterator]() {
    for (let element of this.elements) {
      yield element;
    }
  }
}

let chars = new List();
chars.add('A')
     .add('B')
     .add('C');

// 使用Symbol.iterator实现了迭代
for (let c of chars) {
  console.log(c);
}

// A
// B
// C

```

### Symbol.isConcatSpreadable

我们可以使用concat()方法来合并两个数组

```javascript
let odd  = [1, 3],
    even = [2, 4];
let all = odd.concat(even);
console.log(all); // [1, 3, 2, 4]

```

我们也可以使用concat()来传入单个元素，而非数组

```javascript
let extras = all.concat(5);
console.log(extras); // [1, 3, 2, 4, 5]

```

在上面的例子中，我们将一个数组传给concat()方法时，concat()方法会将数组拓展为单个元素。但是，它会以不同的方式去对待单个原始参数，在ES6之前，我们无法更改此行为。

```javascript
let list = {
    0: 'JavaScript',
    1: 'Symbol',
    length: 2
};
let message = ['Learning'].concat(list);
console.log(message); // ["Learning", Object]

```

将list对象合并到 `['Learning']` 数组中，但list对象中的各个元素并没有被合并到数组中。

要在concat()时将`list`对象中的元素单独添加到数组中的，我们需要将`Symbol.isConcatSpreadable`属性添加到list对象中，像下面这样

```javascript
let list = {
    0: 'JavaScript',
    1: 'Symbol',
    length: 2,
    [Symbol.isConcatSpreadable]: true
};
let message = ['Learning'].concat(list);
console.log(message); // ["Learning", "JavaScript", "Symbol"]

```

如果将`Symbol.isConcatSpreadable`设置为false，concat()就会将`list`整个对象合并到数组中。

### Symbol.toPrimitive

`Symbol.toPrimitive` 方法决定了当一个对象被转换成原始值时的行为。

JavaScript引擎在每个类型值的原型上定义了Symbol.toPrimitive方法。

`Symbol.toPrimitive`方法接受一个hint参数，该参数会是下面三个值，string、number、default，hint参数用来指定返回值的类型。hint参数由JavaScript引擎根据使用对象的上下文进行填充。

```javascript
function Money(amount, currency) {
    this.amount = amount;
    this.currency = currency;
}

Money.prototype[Symbol.toPrimitive] = function(hint) {
    var result;
    switch (hint) {
        case 'string':
            result = this.amount + this.currency;
            break;
        case 'number':
            result = this.amount;
            break;
        case 'default':
            result = this.amount + this.currency;
            break;
    }
    return result;
}

var price = new Money(10000, '人民币');

console.log('我有 ' + price); // Price is 799USD
console.log(+price + 1); // 800
console.log(String(price)); // 799USD

```

### 其他

- `Symbol.match(regex)`：一个在调用 `String.prototype.match()` 方法时调用的方法，用于比较字符串。
- `Symbol.replace(regex, replacement)`：一个在调用 `String.prototype.replace()` 方法时调用的方法，用于替换字符串的子串。
- `Symbol.search(regex)`：一个在调用 `String.prototype.search()` 方法时调用的方法，用于在字符串中定位子串。
- `Symbol.species(regex)`：用于创建派生对象的构造函数。
- `Symbol.split`：一个在调用 `String.prototype.split()` 方法时调用的方法，用于分割字符串。
- `Symbol.toStringTag`：一个在调用 `String.prototype.toString()` 方法时使用的字符串，用于创建对象描述。
- `Symbol.unscopables`：一个定义了一些不可被 with 语句引用的对象属性名称的对象集合。

## 参考资料

- https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol/asyncIterator


原文链接：https://juejin.cn/post/7017375285699952648
