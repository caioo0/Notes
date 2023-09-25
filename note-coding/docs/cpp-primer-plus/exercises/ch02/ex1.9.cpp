//
// Created by Jochoi on 2023/9/23.
//

#include <iostream>
using namespace std;
int main()
{
    int a = 50,sum ;
    while(a<=100)
    {
        cout << "a 的值" << a << endl;
        sum += a;
        a++;
    }
    cout << "最后结果为:" << sum << endl;
    return 0;

}