from pyspark import SparkConf, SparkContext
def MyPartitioner(key):
 print("MyPartitioner is running")
 print('The key is %d' % key)
 return key%10
def main():
 print("The main function is running")
 conf = SparkConf().setMaster("local").setAppName("MyApp")
 sc = SparkContext(conf = conf)
 data = sc.parallelize(range(10),5)
 data.map(lambda x:(x,1)) \
 .partitionBy(10,MyPartitioner) \
 .map(lambda x:x[0]) \
 .saveAsTextFile("file:///data/spark/rdd/partitioner")
if __name__ == '__main__':
 main()