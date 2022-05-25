from motor import Motor
import time
class MotorAction:
    def __init__(self, currentAction="") -> None:
        self.currentAction = currentAction
        self.motor1 = Motor("motor1")
        self.motor2 = Motor("motor2")
        self.motor3 = Motor("motor3")

        #           motor3
        #
        #   motor1          motor2
        #

    def setCurrentAction(self, currentAction):
        print("MOTORS PROJECTING %s" % currentAction)
        self.currentAction  = currentAction
        
    def projectAction(self):
        self._projectExpression(self.currentAction)

    def _projectExpression(self, expression):
        if(expression == "no"):
            self.motor1.moveInside()
            self.motor2.moveOutside()
            time.sleep(1)
            self.motor1.moveOutside()
            self.motor2.moveInside()
            
        if(expression == "yes"):
            self.motor3.moveOutside()
            time.sleep(1)
            self.motor3.moveInside()
            
            
        if(expression == "no"):
            self.motor1.moveInside()
            time.sleep(1)
            self.motor2.moveOutside()
        if(expression == "special"):
            self.motor1.moveInside()
            self.motor2.moveOutside()
            self.motor3.moveInside()
            time.sleep(1)
            self.motor1.moveOutside()
            self.motor2.moveInside()
            self.motor3.moveOutside()

        
            

   

        