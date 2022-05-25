class Motor:
    def __init__(self, name="") -> None:
        self.name = name

    def moveInside(self):
        print("motor : %s moved inside" % self.name)
    
    def moveOutside(self):
        print("motor : %s moved outside" % self.name)