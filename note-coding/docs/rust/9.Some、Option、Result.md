

# Rust 学习之 Some、Option、Result

最近学习 Rust 时对它的所有权，借用等概念，包括语法之类的都还算好理解，但碰到 Some、Option、Result 这些，包括语句后面的 ? 号等等着实困惑了一把，不过经过各种资料的翻阅，总算是理解这几样东西的用法及存在的意义，在这里记录一下。



## **Option**

严格的来说，只有 Option 和 Result，Some 只是 Option 的一个值包装类型。

我们先来描述一个普通的场景，在很多语言中，获取一个数据可能会返回 null 来代表没有数据，拿 java 举个例：

```java
User user = model.getUser();

if (user == null) {
    throw new Exception("用户不存在");
}

System.out.println("你好：" + user.getName());
```

我们在拿到一个不确定，可能为空的值时，为了确保不出现 NullPointerException 的问题，需要先判断值是否是 null。

这个看起来没什么问题，不过仔细思考，实际上会有两个问题：

1. 开发者极容易忘记做 null 的判断，实际开发和测试中也许不容易碰到为 null 的情况，导致线上运行报错。
2. 即使只是为 null 时简单的抛异常，代码也显的有点啰嗦，这种简单的判断能不能少点代码？？

Rust 的 Option 就解决了这个问题。

Option 代表可能为空可能有值的一种类型，本质上是一个枚举，有两种分别是 Some 和 None。Some 代表有值，None 则类似于 null，代表无值。

感觉是不是有点多此一举，判断个 null 了事的事情，搞这么奇怪？

这里就又涉及到 Rust 的概念，它要在你编写和编译阶段就阻止可能的错误发生，而不是运行时才知道出错，Option 就能很好的做到这一点。那么我们来看看 Option 怎么解决上面说的两点问题。

```plain
let val: Option<u32> = get_some_val();
```

这个时候 val 只是个 Option<u32> 类型，里面的值是个无符号32位整形，怎么拿到它的值呢？两种方式，一个是 match，另一个是 if let。

```plain
//方法 match
match val {
    Some(num) => println!("val is: {}", num),
    None => println!("val is None")
}

//方法 if let
if let Some(num) = val {
    println!("val is: {}", num);
} else {
    println!("val is None");
}
```

有没有发现点什么？没？？我告诉你，你根本没办法无脑拿值用。无论是 match 还是 if let 这两种写法你都主观上的要取其中有效的值，即使 if let 不写 else 也是取到了有效的值才执行 if 块中的内容，结果就是你根本没法拿 None 来用，而且主观上感知很明显，也做不到忘记判断 null 这种事（只有故意不判断）。

另外 Option 类型可以让 Rust 在编译阶段就发现你代码的问题，如果写的有问题，连构建都不通过，第一个问题就这样解决了。

那么第二个问题，如果我就是想无脑拿值，如果值是 None 让程序直接报错，就跟上面那段 java 代码一样，如何做呢。

```plain
let num: u32 = val.unwrap();
```

就是这样，unwrap() 做的事就是有值返回值，如果值是 None 则直接 panic!，程序就挂了。

## **Result**

Result 翻译过来就是“结果”，想象一下，我们的接口，服务有非常常规的调用场景，正常返回值，异常返回错误或抛异常等等。而 Rust 里就定义有了一个 Result 用于此场景。

Result 内部本质又是一个枚举，内部分别是 Ok 和 Err，是 Ok 时则代表正常返回值，Err 则代表异常。

简单的一个演示：

```plain
let sr: Result<u32, &str> = Ok(123); //or Err("You are wrong");

match sr {
    Ok(v) => println!("sr value: {}", v),
    Err(e) => println!("sr is error {}", e)
}
```

演示里 sr 是 Result<u32, &str> 类型，正常时返回 u32 整数，异常时返回一段字符串。下方的 match 就可以对结果进行判断和取值。

什么？你就是想拿值，不正常的时候给我报错？为什么这个要和 Option 放一块说，因为它们有着千丝万缕的关系，使用 unwrap()

```plain
let val: u32 = sr.unwrap();
```

unwrap 和 Option 的一样，正常则拿值，异常则 panic!

这里有没有发现，无论是 match 取值，还是 unwrap() 暴力拿值，主观上都有非常明确的意图，而不存在莫名其妙拿了值就用，上线了抛一堆奇奇怪怪的问题的情况（无脑 unwrap 除外）。

## **? 的作用**

前面说到这个问号，它具体是什么作用呢？

想象一下，有这么一种场景，你要从多个函数里取值并计算，他们都可能返回 Result 的错误（Err），只要任何一个返回 Err，就中断并返回这个 Err，正常应该怎么做？

```plain
let sr: Result<u32> = rs.get_u32_result();

match sr {
    Ok(v) => println!("sr is ok: {}", v),
    Err(e) => return Err(e)
}

let st: Result<u8> = rs.get_u8_result();

match st {
    Ok(v) => println!("st is ok: {}", v),
    Err(e) => return Err(e)
}

let sum = sr.unwrap() + st.unwrap() as u32;
```

好像没啥问题，不过代码又有些啰嗦了，让我们用一用 ? 符号。

```plain
fn srst() -> Option<u32> {
    let sr: u32 = rs.get_u32_result()?;
    println!("sr is ok: {}", sr);
    
    let st: u8 = rs.get_u8_result()?;
    println!("st is ok: {}", st)
    
    Ok(sr + st as u32);
}

let sum: Option<u32> = srst();
```

使用 ? 后，你不需要挨个判断并返回，任何一个 ? 返回 Err 了函数都会直接返回 Err。

这里因为 ? 的行为是遇到 Err 直接返回 Err，众所周知，返回的行为必须在函数上，所以使用 ? 时，相关的代码必须在一个函数/方法里，而函数也应该返回 Result 类型，如果在 main() 中直接使用则同样需要把 main() 改为 main() -> Result.. 否则编译时会给你这个：

```plain
error[E0277]: the `?` operator can only be used in a function that returns `Result` or `Option` (or another type that implements `std::ops::Try`)
```

实际使用中的用法很多，? 不仅可以用于 Result 也可以用于 Option，另外这它们也提供 map, and_then 来做到链式依赖和组合使用来大大减少代码量。

Rust 这些看似不一样的地方，实际上都是为了做到一个目的：写代码和编译时就发现所有的错误，而不是运行时才发现。理解了这一点，你就能理解 Rust 的各种设定。