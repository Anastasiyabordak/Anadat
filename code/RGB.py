class RGB:
    def __init__(self, value=0, operation='>='):
        self.redValue = value
        self.greenValue = value
        self.blueValue = value
        self.redOperation = operation
        self.greenOperation = operation
        self.blueOperation = operation

    def setRGB(self, value=[0,0,0], operation=['>=', '>=', '>=']):
        self.redValue = value[0]
        self.greenValue = value[1]
        self.blueValue = value[2]
        self.redOperation = operation[0]
        self.greenOperation = operation[1]
        self.blueOperation = operation[2]
