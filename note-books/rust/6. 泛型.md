# 泛型

举几个例子感受一下泛型的使用：

示例1：

```
fn add_i8(a:i8,b:i8) -> i8 {
	a + b
}

fn add_i32(a:i32,b:i32) -> i32 {
	a + b
}

fn add_f64(a:f64,b:f64) -> f64 {
	a + b 
}

fn add<T: std::ops::Add<Output = T>>(a:T,b:T) -> T {
	a+b
}

fn main (){
	println!("add i8：{}",add_i8(2i8,3i8));
	println!("add i8：{}",add_i32(2i32,3i32));
	println!("add i8：{}",add_f64(2f64,3f64));
	println!("add：{}",add(2f64,3f64));
}
```

```rust

// 实现一个结构体 Point 让代码工作
struct Point<T,U>{
    x:T,
    y:U,
}

fn main() {
    let integer = Point { x: 5, y: 10 };
    let float = Point { x: 1, y: 4.0 };
}
```

```

// 为 Val 增加泛型参数，不要修改 `main` 中的代码
struct Val<T> {
    val: T,
}

impl<T> Val<T> {
    fn value(&self) -> &T {
        &self.val
    }
}


fn main() {
    let x = Val{ val: 3.0 };
    let y = Val{ val: "hello".to_string()};
    println!("{}, {}", x.value(), y.value());
}
```

```
struct Point<T, U> {
    x: T,
    y: U,
}

impl<T, U> Point<T, U> {
    // 实现 mixup，不要修改其它代码！
    fn mixup<V,W>(self,other:Point<V,W>) ->Point<T,W>{
        Point {
            x: self.x,
            y: other.y,
        }
    }
}

fn main() {
    let p1 = Point { x: 5, y: 10 };
    let p2 = Point { x: "Hello", y: '中'};

    let p3 = p1.mixup(p2);

    assert_eq!(p3.x, 5);
    assert_eq!(p3.y, '中');
}
```

```

// 修复错误，让代码工作
struct Point<T> {
    x: T,
    y: T,
}

impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}

fn main() {
    let p = Point{x: 5.0_f32, y: 10.0_f32};
    println!("{}",p.distance_from_origin())
}
```

### const 泛型

```
// 填空
fn print_array<T:std::fmt::Debug,const N:usize>(arr:[T;N]) {
    println!("{:?}", arr);
}
fn main() {
    let arr = [1, 2, 3];
    print_array(arr);

    let arr = ["hello", "world"];
    print_array(arr);
}

```

