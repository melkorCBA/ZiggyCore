try:
    import pika
    import json

except Exception as e:
    print("Sone Modules are missings {}".format_map(e))


class MetaClass(type):

    _instance ={}

    def __call__(cls, *args, **kwargs):

        """ Singelton Design Pattern  """

        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]

class RabbitMqConfigureSender():

    def __init__(self, queue='default', host='localhost', routingKey='default', exchange=''):
        """ Configure Rabbit Mq Server  """
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange

class RabbitMqSender():

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

        print("Published Message: {}".format(payload))
        self._connection.close()

# if __name__ == "__main__":
#     server = RabbitmqConfigure(queue='text-to-speech',
#                                host='localhost',
#                                routingKey='speak',
#                                exchange='speech')

#     rabbitmq = RabbitMq(server)
#     rabbitmq.publish(payload="his wikiHow teaches you how to install FFmpeg onto your Windows 10 computer. FFmpeg is a command line-only program that allows you to convert videos and audio into different formats, as well as record live audio and video.")