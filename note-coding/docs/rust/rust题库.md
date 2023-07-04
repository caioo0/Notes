# rust题库

- 在华氏温度和摄氏度之间转换温度。
- 生成 n 阶斐波那契数列。
- 打印圣诞颂歌 “The Twelve Days of Christmas” 的歌词，利用歌曲中的重复部分（编写循环）。



**FizzBuzz问题**

```
/*
FizzBuzz问题
写一个程序打印1到100这些数字。
但是遇到数字为3的倍数的时候，打印“Fizz”替代数字，
5的倍数用“Buzz”代替，
既是3的倍数又是5的倍数打印“FizzBuzz”。
 */

fn fizz_buzz(n:i32) -> Vec<String> {
    let mut result = Vec::new();
    for i in 1..=n {
        if i%5 ==0 && i%3 ==0 {
            result.push("FizzBuzz".into());
        }else if i%5 == 0 {
            result.push("Buzz".into());
        }else if i%3 == 0 {
            result.push("Fizz".into());
        }else{
            result.push(i.to_string());
        }
    }
    result
}
fn main() {
    let r = fizz_buzz(100);
    dbg!(r);
}
```

