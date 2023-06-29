# 汇编语言之[bx] 和 loop指令

1、[bx] 和 loop指令
[bx] 的含义：[bx]同样表示一个内存单元，它的偏移地址在bx中，段地址默认在ds中

loop指令的格式是：loop 标号，CPU执行loop指令的时候，要进行两步操作，

(cx) = (cx) - 1；

判断 cx 中的值，不为零则转至标号处执行程序，如果为零则向下执行。

例如：计算212

```
assume cs:code 

code segment 
	mov ax, 2
	
	mov cx, 11 ;循环次数
s:  add ax, ax 
	loop s     ;在汇编语言中，标号代表一个地址，标号s实际上标识了一个地址，
               ;这个地址处有一条指令：add ax，ax。
               ;执行loop s时，首先要将（cx）减1，然后若（cx）不为0，则向前
               ;转至s处执行add ax，ax。所以，可以利用cx来控制add ax，ax的执行次数。
	
	mov ax,4c00h 
	int 21h 
code ends 
end

```

**loop 和 [bx] 的联合应用**

计算ffff:0 ~ ffff:b单元中的数据的和，结果存储在dx中

问题分析：

这些内存单元都是字节型数据范围0 ~ 255 ，12个字节数据和不会超过65535，dx可以存下
对于8位数据不能直接加到 dx
解决方案：

用一个16位寄存器来做中介。将内存单元中的8位数据赋值到一个16位寄存器a中，再将ax中的数据加到dx

```
assume cs:code 

code segment 
	mov ax, 0ffffh ;在汇编源程序中，数据不能以字母开头，所以要在前面加0。
	mov ds, ax 
	mov bx, 0   ;初始化ds:bx指向ffff:0
	mov dx, 0   ;初始化累加寄存器dx，（dx）= 0
	
	mov cx, 12  ;初始化循环计数寄存器cx，（cx）= 12
s:  mov al, [bx]
	mov ah, 0
	add dx, ax  ;间接向dx中加上（（ds）* 16 +（bx））单元的数值
	inc bx      ;ds:bx指向下一个单元
	loop s 
	
	mov ax, 4c00h 
	int 21h 
code ends 
end
```

## 2、段前缀

```
mov ax, ds:[bx]
mov ax, cs:[bx]
mov ax, ss:[bx]
mov ax, es:[bx]
mov ax, ss:[0]
mov ax, cs:[0]
```

这些出现在访问内存单元的指令中，用于显式地指明内存单元的段地址
的“ds:”，“cs:”，“ss:”，“es:”，在汇编语言中称为段前缀。

**段前缀的使用**

将内存`ffff:0 ~ ffff:b`单元中的数据复制到`0:200 ~ 0:20b`单元中。

```
assume cs:code 

code segment 
	mov ax, 0ffffh 
	mov ds, ax   ;（ds）= 0ffffh 
	mov ax, 0020h
    mov es, ax   ;（es）= 0020h     0:200 等效于 0020:0
    mov bx, 0    ;（bx）= 0，此时ds:bx指向ffff:0，es:bx指向0020:0
    
	mov cx，12   ;（cx）=12，循环12次
s:  mov dl，[bx] ;（d1）=（（ds）* 16+（bx）），将ffff:bx中的字节数据送入dl 
	mov es:[bx]，dl ;（（es）*16+（bx））=（d1），将dl中的数据送入0020:bx 
	inc bx  ;（bx）=（bx）+1
	loop s 
	
	mov ax，4c00h 
	int 21h 
code ends 
end

```



## 资料

https://blog.csdn.net/qq_39654127/article/details/88698911