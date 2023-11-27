

class Array:
    def binary_search(self,list,item) :
        low = 0 ;
        high =len(list)-1;

        while low <=high:
            mid = (low + high)
            guess = list[mid]
            if guess == item:
                return mid
            elif guess > item:
                high = mid -1
            else:
                low = mid +1
        return None


import math
if __name__ == '__main__':
    bs = Array()
    my_list= [1,3,4,5,6,7]   # 有序数组
    print("索引值：",bs.binary_search(my_list,5))
    print("128的真值：", math.log(128,2))






