#include <iostream>
using namespace std;
 
int main ()
{
   // 带有 5 个元素的双精度浮点型数组
   double runoobAarray[5] = {1000.0, 2.0, 3.4, 17.0, 50.0};

 
   cout << "使用 runoobAarray 作为地址的数组值 " << endl;
   for ( int i = 0; i < 5; i++ )
   {
       cout << "*(runoobAarray + " << i << ") : ";
       cout << *(runoobAarray + i) << endl;
   }
 
   return 0;
}