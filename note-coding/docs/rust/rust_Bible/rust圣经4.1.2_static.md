# &'static 和 T:'static

`'static` 在 Rust 中是相当常见的，例如字符串字面值就具有 `'static` 生命周期:

```
fn main()
{
	let mark_twain: &str = "Samuel Clemens";

	print_author(mark_twain);
}

fn print_author(author: &'static str) {
	println!("{}",author);
}
```

除此之外，特征对象的生命周期也是 `'static`，例如[这里](https://course.rs/compiler/fight-with-compiler/lifetime/closure-with-static.html#特征对象的生命周期)所提到的。

除了 `&'static` 的用法外，我们在另外一种场景中也可以见到 `'static` 的使用:

```
use std::fmt::Display;
fn main() {
    let mark_twain = "Samuel Clemens";
    print(&mark_twain);
}

fn print<T: Display + 'static>(message: &T) {
    println!("{}", message);
}
```

在这里，很明显 `'static` 是作为生命周期约束来使用了。 **那么问题来了， `&'static` 和 `T: 'static` 的用法到底有何区别？**



## &'static

`&'static` 对于生命周期有着非常强的要求：一个引用必须要活得跟剩下的程序一样久，才能被标注为 `&'static`。

对于字符串字面量来说，它直接被打包到二进制文件中，永远不会被 `drop`，因此它能跟程序活得一样久，自然它的生命周期是 `'static`。

但是，**`&'static` 生命周期针对的仅仅是引用，而不是持有该引用的变量，对于变量来说，还是要遵循相应的作用域规则** :

```rust
use std::{slice::from_raw_parts,str::from_utf8_unchecked};

fn get_memory_location() ->(usize,usize){

 // “Hello World” 是字符串字面量，因此它的生命周期是 `'static`.
  // 但持有它的变量 `string` 的生命周期就不一样了，它完全取决于变量作用域，对于该例子来说，也就是当前的函数范围
  let string = "“Hello,World";
  let pointer = string.as_ptr() as usize;
  let length = string.len();
  (pointer,length)
  // 'string' 在这里被drop释放
  // 虽然变量被释放，无法再被访问，但是数据依然还会继续存活
}

fn get_str_at_location(pointer:usize,length:usize) -> &'static str{
	unsafe{from_utf8_unchecked(from_raw_parts(pointer as *const u8,length))}
}

fn main(){
	let (pointer,length)  = get_memory_location();
	let message = get_str_at_location(pointer,length);

	println!(
		"The {} bytes at 0x{:X} Stored: {}",
		length,pointer,message 
		)
}
```

上面代码有两点值得注意：

- `&'static` 的引用确实可以和程序活得一样久，因为我们通过 `get_str_at_location` 函数直接取到了对应的字符串
- 持有 `&'static` 引用的变量，它的生命周期受到作用域的限制，大家务必不要搞混了

## [`T: 'static`](https://course.rs/advance/lifetime/static.html#t-static)

相比起来，这种形式的约束就有些复杂了。

首先，在以下两种情况下，`T: 'static` 与 `&'static` 有相同的约束：`T` 必须活得和程序一样久。

```rust
use std::fmt::Display;

// fn print_it<T: Debug + 'static> (input: &T) {
// 	println!("'static value passed in is : {:?}",input);
// }

fn main() {
	let r1;
	let r2;
	{
		static STATIC_EXAMPLE: i32 = 42;
		r1 = &STATIC_EXAMPLE;
		let x = "&'static str";
		r2 = x;
	}

	println!("&'static i32:{}",r1);
	println!("&'static str: {}",r2);

	// r1 和 r2 持有的数据都是 'static 的，因此在花括号结束后，并不会被释放

	let r3: &str;
	{
		let s1 = "String".to_string();

		static_bound(&s1);

		r3 = &s1;
	}

	println!("{}",r3);

}

fn static_bound<T: Display + 'static>(t: &T) {
	println!("{}",t);
}
```

## static 到底针对谁？

大家有没有想过，到底是 `&'static` 这个引用还是该引用指向的数据活得跟程序一样久呢？

**答案是引用指向的数据**，而引用本身是要遵循其作用域范围的，我们来简单验证下：

