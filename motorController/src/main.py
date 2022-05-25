from queueReciver import RabbitMqServerConfigure, rabbitmqServer
from motorAction import MotorAction
import json

motorACtionController = MotorAction()

def main():
    motorActionServerConfig = RabbitMqServerConfigure(host='localhost', queue='motor-action',  routingKey='m-action',  exchange='main-exchnage')
    motorActionServer = rabbitmqServer(server=motorActionServerConfig)
    motorActionServer.subscribeQueue(motorActionCallback)
    print("speaker is idle..")

def motorActionCallback(body):
    data = json.loads(body)
    actionExpression = data["expression"]
    motorACtionController.setCurrentAction(actionExpression)
    motorACtionController.projectAction()

main()
