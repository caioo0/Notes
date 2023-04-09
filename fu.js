//实例1
function fn() {
    var arr = [];
    for (var i = 0; i < 5; i++) {

        arr[i] = function () {
            return i;
        }
    }
    return arr;
}

var list = fn();
console.log(list[1]);

//实例2
for(var i=0,len=list.legnth;i<len;i++){
    console.log(i);
    console.log(list[i]())
}
var age = 10;
function foo(){
    console.log(age);//-----------------1
    var name = "hunt_bo";
    return function(){
        console.log(name);
    }
}
var bar =  foo();
bar();
//实例3
function addCount(){
    var count = 0;
    return function(){
        count += 1;
        console.log(count);
    }
}
var fun1 = addCount();
var fun2 = addCount();
fun1();//1
fun1();//2
fun1();//3
fun2();//1
fun2();//2
//实例4
function fn(){
    var a = 3;
    return function(){
        return ++a;
    }
}
console.log(fn()());//4
console.log(fn()());//4
console.log(fn()());//4
var newFn = fn();
console.log(newFn());//4
console.log(newFn());//5
console.log(newFn());//6

//实例5
(function(window) {
    var m = 0;
    function getM(){
        return m;
    }
    function seta(val){
        m = val;
    }
    window.g = getM;
    window.f = seta;
})(this);
this.f(100);
console.log(this.g());//100


//实例6


// var lis = document.getElementsByTagName("li");
// for(var i=0;i<lis.length;i++) {
//     (function (i) {
//         lis[i].onclick = function () {
//             console.log(i);
//         };
//     })(i);
// }

//实例7
function fnnn(){
    var arr = [];
    for(var i = 0;i < 5;i ++){
        arr[i] = function(){
            return i;
        }
    }
    return arr;
}
var list = fnnn();
for(var i = 0,len = list.length;i < len ; i ++){
    console.log(list[i]());
}