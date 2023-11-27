
class Array:
    def two_sum(self,list,target) :

        result = []
       for i, each in enumerate(list):
            if abs(target-each) >=0 and i not result:
                try:
                    tmp = list.index(target-each)




if __name__ == '__main__':
    bs = Array()
    nums = [2, 7, 11, 15]
    target = 9
    bs.two_sum(nums,target)






