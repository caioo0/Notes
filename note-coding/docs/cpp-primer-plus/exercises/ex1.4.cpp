#include <iostream>
int main()
{
	std::cout << "input two numbers";
	std::cout << std::endl;
	int v1,v2;
	std::cin >> v1 >> v2;
	std::cout << " 数值 " << v1;
    std::cout << " 和 " << v2 ;
    std::cout << "的积为";
	std::cout << v1 * v2 << std::endl;
    return 0;
}