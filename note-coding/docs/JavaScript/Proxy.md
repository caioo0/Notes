# Proxy 

**Proxy** 对象用于创建一个对象的代理，从而实现基本操作的拦截和自定义（如属性查查、赋值、枚举、函数调用等）。

```
new Proxy(target, handler)
```



## 术语

handler

包含捕捉器（trap）的占位符对象，可译为处理器对象

traps

提供属性访问的方法。

target

被Proxy代理虚拟化的对象。它常被作为代理的存储后端。根据目标验证关于对象不可扩展性或不可配置属性的不变量（保持不变的语义）。

## 语法



```javascript
const p = new Proxy(target,handler)
```



### 参数

`target`

要使用`Proxy`包装的目标对象（可以是任何类型的对象，包括原生数据，函数，甚至另一个代理）。

`handler`

一个通常以函数作为属性的对象，各属性中的函数分别定义了在执行各种操作时代理`p`的行为。



## 方法

`Proxy.revocable()`

创建一个可撤销的`Proxy`对象。



## 示例

**基本示例**

```
let handler = {
    get: function(target,name){
        return name in target ? target[name] : 42;
    }
};

let p = new Proxy({},handle);

p.a = 1;

console.log(p.a,p.b);
```

**无操作转发代理**

```
let target = {};
let p = new Proxy(target, {});

p.a = 37;   // 操作转发到目标

console.log(target.a);    // 37. 操作已经被正确地转发

```

**[验证](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Proxy#验证)**

通过代理，你可以轻松地验证向一个对象的传值。下面的代码借此展示了 [`set`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Proxy/Proxy/set) handler 的作用。

http://m.yspaper.cn/creditsys/index.php?acturl=salecklist&login_openid=omQgktxat56iiMs5Y-7oCWjhCOoI