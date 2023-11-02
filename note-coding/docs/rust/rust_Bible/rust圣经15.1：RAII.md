# 作用域规则

作用域在所有权（ownership）、借用（borrow）和生命周期（lifetime）中起着重要作用。也就是说，作用域告诉编译器什么时候借用是合法的、什么时候资源可以释放、以及变量何时被创建或销毁。



## RAII

Rust的变量不只是在栈中保存数据：它们也占有资源，比如`Box<T>`占有堆(heap)中的内存。

Rust强制实行RAII (Resource Acquisition Is Init)