try:
    import pika
    import json

except Exception as e:
    print("Sone Modules are missings {}".format_map(e))




class RabbitmqConfigure():

    def __init__(self, queue='default', host='localhost', routingKey='default', exchange=''):
        """ Configure Rabbit Mq Server  """
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange

class RabbitMq():

    def __init__(self, server):

        """
        :param server: Object of class RabbitmqConfigure
        """

        self.server = server

        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def publish(self, payload ={}):

        """
        :param payload: JSON payload
        :return: None
        """
        # payload = json.dumps(payload)
        self._channel.basic_publish(exchange=self.server.exchange,
                      routing_key=self.server.routingKey,
                      body= str(json.dumps(payload)))

        # print("Published Message: {}".format(payload))
        self._connection.close()

# if __name__ == "__main__":
#     server = RabbitmqConfigure(queue='speech-to-text', host='localhost', routingKey='listen', exchange='speech')
#     rabbitmq = RabbitMq(server)
#     rabbitmq.publish(payload={"Data":22})