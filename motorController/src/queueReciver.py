try:
    import pika
    import json
    import ctypes  # An included library with Python install.   


except Exception as e:
    print("Some modules are missings {}".format(e))

class MetaClass(type):

    _instance ={}

    def __call__(cls, *args, **kwargs):

        """ Singelton Design Pattern  """

        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class RabbitMqServerConfigure(metaclass=MetaClass):

    def __init__(self, queue='default', host='localhost', routingKey='default', exchange=''):

        """ Server initialization   """

        self.host = host
        self.queue = queue
        self.routingKey = routingKey
        self.exchange = exchange

class rabbitmqServer():

    def __init__(self, server):

        """
        :param server: Object of class RabbitMqServerConfigure
        """

        self.server = server
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._tem = self._channel.queue_declare(queue=self.server.queue)
        print("Server started waiting for Messages on")
        print("Queue: %s Exchange: %s RoutingKey: %s" % (self.server.queue, self.server.exchange, self.server.routingKey))


    def utilityCallback(body, callback):
        callback(body)


    def subscribeQueue(self, returnCallback):
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback= lambda ch,method, properties, body: returnCallback(body),
            auto_ack=True)
        self._channel.start_consuming()

# def printData(body):
#     # data = json.loads(body)
#     # print(data['word'])
#     print(body)

# if __name__ == "__main__":
#     serverconfigure = RabbitMqServerConfigure(host='localhost',
#                                               queue='speech-to-text',  routingKey='deepspeech',  exchange='speech')

#     server = rabbitmqServer(server=serverconfigure)
#     server.subscribeQueue(printData)

