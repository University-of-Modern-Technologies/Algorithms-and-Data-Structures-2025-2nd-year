#!/usr/bin/env python
import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672)
)
channel = connection.channel()

channel.exchange_declare(exchange="topic_logs", exchange_type="direct")
channel.queue_declare(queue="task_queue", durable=True)
channel.queue_bind(exchange="topic_logs", queue="task_queue")


def create_task(num: int):
    for i in range(num):
        message = f"Hello World! {i}"

        channel.basic_publish(
            exchange="topic_logs",
            routing_key="task_queue",
            body=message,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
        print(f" [x] Sent {message}")

    connection.close()


if __name__ == "__main__":
    create_task(5)
