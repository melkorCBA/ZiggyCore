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

    def __init__(self, queues = [{"name": "default", "routingKey": ""}], host='localhost', exchange=''):

        """ Server initialization   """
        self.queues = queues
        self.host = host
        self.exchange = exchange

class rabbitmqServer():

    def __init__(self, server):

        """
        :param server: Object of class RabbitMqServerConfigure
        """
        
        self.server = server
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        for queue in self.server.queues:
            self._channel.queue_declare(queue=queue['name'])
        for queue in self.server.queues:
            self._channel.queue_bind(queue['name'], self.server.exchange, queue['routingKey'])
        
        print("Servers started waiting for Messages on")
        print("Queues:"),
        [print(i) for i in self.server.queues]
        print("Exchange: %s " % (self.server.exchange))

    def subscribeQueue(self, returnCallback):
        for queue in self.server.queues:
            self._channel.basic_consume(queue=queue['name'], on_message_callback= lambda ch,method, properties, body: returnCallback(ch,method, properties, body), auto_ack=True)
        self._channel.start_consuming()

