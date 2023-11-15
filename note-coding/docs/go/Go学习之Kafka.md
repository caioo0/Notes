

# GO学习之 消息队列(Kafka)

## kafka 

### 下载kafka

```
go get github.com/Shopify/sarama
or 
go get github.com/IBM/sarama
```

### 生产者

首先用 sarama.NewConfig() 来创建一个 config 配置实体，然后通过 sarama.NewSyncProducer() 来创建一个生产者，用 &sarama.ProducerMessage{} 生成一个消息，通过 producer.SendMessage(message) 发送到制定 Topic 中。

```go
package main

import (
	"log"
	"time"

	"github.com/IBM/sarama"
)

func main() {
	// 配置 kafka 生产者
	config := sarama.NewConfig()
	config.Producer.RequiredAcks = sarama.WaitForAll
	config.Producer.Retry.Max = 5
	config.Producer.Return.Successes = true

	// 创建 Kafka 生产者
	producer, err := sarama.NewSyncProducer([]string{"192.168.1.20:9092"}, config)
	if err != nil {
		log.Fatalf("Creating producer: %v", err)
	}
	// 延迟关闭生产者链接
	defer producer.Close()

	// 定义消息 Topic是 go-test, 值为 Hello Kafka
	message := &sarama.ProducerMessage{
		Topic: "go-test",
		Value: sarama.StringEncoder("Hello Kafka!"),
	}

	// 发送消息
	for i := 0; i < 10; i++ {
		partition, offset, err := producer.SendMessage(message)
		if err != nil {
			log.Fatalf("Sending message: %v", err)
		}
		log.Printf("Message sent to partition %d at offset %d", partition, offset)
		time.Sleep(time.Second)
	}
}

```

### 消费者

消费者代码和生产者思路一致，首先创建一个 配置对象，通过 `sarama.NewConsumer()` 来创建消费者，然后通过 consumer.ConsumePartition() 监听到一个分区，进行消息消费。
通过 select 来区分是否成功获取到消息，还是获取到错误。

```go
package main

import (
	"log"

	"github.com/Shopify/sarama"
)

func main() {
	// 配置 Kafka 消费者
	config := sarama.NewConfig()
	config.Consumer.Return.Errors = true

	// 创建 Kafka 消费者
	consumer, err := sarama.NewConsumer([]string{"192.168.1.20:9092"}, config)
	if err != nil {
		log.Fatal(err)
	}
	// 延迟关闭消费者链接
	defer consumer.Close()
	//订阅主题，获取分区 partition
	partitionConsumer, err := consumer.ConsumePartition("go-test", 0, sarama.OffsetOldest)
	if err != nil {
		log.Fatalf("Consuming partition: %v", err)
	}
	// 延迟关闭分区链接
	defer partitionConsumer.Close()

	// 消费消息
	for {
		select {
		// 从 分区 通道中获取信息
		case msg := <-partitionConsumer.Messages():
			log.Printf("Received message: %s", string(msg.Value))
		// 如果从通道中获取消息失败
		case err := <-partitionConsumer.Errors():
			log.Fatalf("Received error: %v", err)
		}
	}
}

```

