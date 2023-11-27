

class Find:
    def findSmallest(self,list,item) :
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
    bs = Find()
    my_list= [5,3,6,10]   # 数组排序
    print("索引值：",bs.binary_search(my_list,5))
    print("128的真值：", math.log(128,2))






