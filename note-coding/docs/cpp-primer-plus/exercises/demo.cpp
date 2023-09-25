#include <iostream>
int main ()
{
    int ival = 1024;
    int* pi = &ival;  //pi 指向一个int型的数
    int** ppi = &pi;  //ppi 指向一个int型的数
    std::cout << "the value of ival \n"
         << "direct value: " << ival << "\n"
         << "indirect value: " << *pi << "\n"
         << "doubly indirect value: " << **ppi << ", ppi = " << ppi << " , *ppi = " << *ppi 
         << std::endl; 
}