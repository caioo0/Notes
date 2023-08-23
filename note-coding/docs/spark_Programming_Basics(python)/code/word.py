from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MyApp")
sc = SparkContext(conf = conf)
lines = sc.textFile("file:///opt/spark/data/word.txt")
words = lines.map(lambda line:line.split(" "))
words.foreach(print)