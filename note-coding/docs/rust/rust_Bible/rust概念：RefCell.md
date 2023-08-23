# 智能指针-RefCell<T>

借用规则，任何时候引用必须有效（原主存在），只能有一个可变引用或多个不可变引用

```
fn main() { 
	let x = 5;  // not let mut ,不可变
	let y = &mut x;  // 报错，不能可变借用不可变值
}
```

RefCell<T>用来实现内部可变性，internal mutability，即数据可以在自身的方法中改变自身，但对外是不可变的。

Box<T>, Rc<T>, RefCell<T>比较：

Rc<T>，允许多重拥有，不可变借用，编译时检查

Box<T>，单一拥有者，可变或不可变借用，编译时检查(Deref, DerefMut)

RefCell<T>, 单一拥有者，可变或不可变借用，运行时检查。可变不可变是对外的，都可以在内部改变。其实是把不安全的操作包装在安全的接口中，适用于：我比编译器明白，我知道我在干什么。

```
//这个例子要求实现外部特性，检查流量并发送消息
#![allow(unused_variables)]
fn main() {
pub trait Messenger {
    fn send(&self, msg: &str);  //外部特性，不能改动
}

pub struct LimitTracker<'a, T: 'a + Messenger> {
//这样的语法哪里都没讲，拿来就用
//<'a，表示本结构的生命期，结构存在的时候，所有引用元素都得活着
//结构的元素有泛型，所以得声明，该元素有生命期，所以泛型也得声明生命期，T: 'a

//该泛型要实施Messenger, 只好用个加号，T:'a + Messenger
//附录B, table B-1, Operators, "+", Table B-5: Trait Bound Constraints
//trait + trait, 'a + trai: Compound type constraint
//差评差评差评

//全部加起来<'a, T: 'a + Messenger>
//应该等价于，<'a, T: 'a> where T: Messenger

    messenger: &'a T, //'a&T不好吗？
    value: usize,
    max: usize,
}

impl<'a, T> LimitTracker<'a, T>  //没有<'a, T: 'a>
    where T: Messenger {
    pub fn new(messenger: &T, max: usize) -> LimitTracker<T> { 
    //不返回指针， &T的生命期隐含在定义中, 参数只有一个指针，没有歧义，所以不需要<'a, T: 'a>。猜测。
    //总之，如果不是明确需要生命期先不要管，反正编译器会告诉你
        LimitTracker {
            messenger,  //messenger=messenger, 域名与参数同名，简化赋值
            value: 0,
            max,  //max=max
        }
    }

    pub fn set_value(&mut self, value: usize) {
        self.value = value;

        let percentage_of_max = self.value as f64 / self.max as f64;

        if percentage_of_max >= 0.75 && percentage_of_max < 0.9 {
            self.messenger.send("Warning: You've used up over 75% of your quota!");
        } else if percentage_of_max >= 0.9 && percentage_of_max < 1.0 {
            self.messenger.send("Urgent warning: You've used up over 90% of your quota!");
        } else if percentage_of_max >= 1.0 {
            self.messenger.send("Error: You are over your quota!");
        }
    }
}
}

#[cfg(test)]
mod tests {
    use super::*;

    struct MockMessenger {
        sent_messages: Vec<String>,
    }

    impl MockMessenger {
        fn new() -> MockMessenger {
            MockMessenger { sent_messages: vec![] }
        }
    }

    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
            self.sent_messages.push(String::from(message));
        }
    }

    #[test]
    fn it_sends_an_over_75_percent_warning_message() {
        let mock_messenger = MockMessenger::new();  //sent_messages==vec![]
        let mut limit_tracker = LimitTracker::new(&mock_messenger, 100);  

        limit_tracker.set_value(80);  
        //调用MockMessenger.send(), 改变sent_messages大小，不可变，编译不通过

        assert_eq!(mock_messenger.sent_messages.len(), 1);
    }
}

//编译结果
error[E0596]: cannot borrow immutable field `self.sent_messages` as mutable
  --> src/lib.rs:52:13
   |
51 |         fn send(&self, message: &str) {  //编译器建议修改函数参数，但Messenger是外部特性
   |                 ----- use `&mut self` here to make mutable
52 |             self.sent_messages.push(String::from(message));
   |             ^^^^^^^^^^^^^^^^^^ cannot mutably borrow immutable field

//用RefCell的解决方案
#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::RefCell;  //引入

    struct MockMessenger {
        sent_messages: RefCell<Vec<String>>,  //包装, 不可变
    }

    impl MockMessenger {
        fn new() -> MockMessenger {
            MockMessenger { sent_messages: RefCell::new(vec![]) }  //RefCell<vec![]>
        }
    }

    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {  //&self，&MockMessenger, 仍然不可变
            self.sent_messages.borrow_mut().push(String::from(message));
            //RefCell<Vec<String>>.borrow_mut()返回RefMut<T>
            //RefMut<T>.push  -> Vec<String>.push  //"."又重载了吗? 见下文
        }
    }

    #[test]
    fn it_sends_an_over_75_percent_warning_message() {
        // --snip--

        assert_eq!(mock_messenger.sent_messages.borrow().len(), 1);
        //RecRef<Vec<String>>.borrwo() -> Ref<T> -> &Vec<String>
    }
}
//RefCell运行时检查借用规则，只能有一个borrow_mut()，或者多个borrow()
```

看一下RefCell<Vec>怎么调用的Vec.push()

```
//std::vec::Vec.push()
pub fn push(&mut self, value: T)  //定义

//文档例子
let mut vec = vec![1, 2];
vec.push(3);
assert_eq!(vec, [1, 2, 3]);

//试验一下
use std::cell::RefCell;

fn main() {
let a = RefCell::new(vec![2, 2, 3, 4]);

a.borrow_mut().push(8);  //RcMut<T>.push()

let b = a.borrow().len();  //Rc<T>.len()
println!("{}", b);  //5，可见RefCell -> Rc<T>可以直接调用被指向内容的方法

//assert_eq!(a, [2, 2, 3, 4, 8]);  错误，Vec!=RefCell
assert_eq!(a.into_inner(), vec![2, 2, 3, 4, 8]);  //没毛病，内部数组加一
}

//该语法说明了一个很重要的问题
//聪明指针包装了数据，同时(somehow)"继承"了他们的方法
//所以聪明指针可以直接调用被指向的内容的方法，对数据自身进行操作
//这种事说一声不好吗? 还是我真没看到
```

混合Rc<T> and RefCell<T>， 多重拥有兼可变

```
#[derive(Debug)]  //衍生属性
enum List {
    //Cons(i32, Rc<List>),  原来的
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use List::{Cons, Nil};
use std::rc::Rc;
use std::cell::RefCell;

fn main() {
    let value = Rc::new(RefCell::new(5));  //包装i32部分

    let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));  //构造List

    let b = Cons(Rc::new(RefCell::new(6)), Rc::clone(&a));  //使用聪明指针，再加上i32
    let c = Cons(Rc::new(RefCell::new(10)), Rc::clone(&a));

    *value.borrow_mut() += 10;  //*，deref, *(Rc<RefCell>) -> RefCell<T>
    //RefCell<T>.borrow_mut() -> &mut 5, 结果value=Rc<RefCell<15>>

    println!("a after = {:?}", a);  //debug formatter
    println!("b after = {:?}", b);
    println!("c after = {:?}", c);
}

//运行结果
//a after = Cons(RefCell { value: 15 }, Nil)  //只显示内容，不显示指针， 下同
//b after = Cons(RefCell { value: 6 }, Cons(RefCell { value: 15 }, Nil))
//c after = Cons(RefCell { value: 10 }, Cons(RefCell { value: 15 }, Nil))
```

至此，基本明白了。聪明指针部分教程比较差，也感觉rust语法还是有点乱。