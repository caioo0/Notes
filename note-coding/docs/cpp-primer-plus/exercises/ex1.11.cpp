#include <iostream>
int main()
{
	std::cout << "input two numbers";
	std::cout << std::endl;
	int v1,v2;
	std::cin >> v1 >> v2;
    int i = v1;
    if(v1>v2)
    {
        std::cout << " ��һ�����ִ��ڵڶ������֣���������" << std::endl; 
        return 0;
    }
	while(i<=v2 )
    {
        std::cout << i << std::endl;
        
        i++;
    }
    std::cout << std::endl;
    return 0;
}