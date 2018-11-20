from RGB import RGB


class Snapshot:
    def __init__(self):
        self.rgb = RGB()
        self.color = [0,0,0]
        self.originalImage = []

    def setRGB(self, rgbValue=[0,0,0], rgbOperation=['>=', '>=', '>=']):
        self.rgb.setRGB(rgbValue, rgbOperation)

    def resetRGB(self):
        self.rgb.setRGB()

    def setColor(self, nColor = [0,0,0]):
        self.color = nColor
    def myCopy(self, value):
        self.rgb.redValue = value.rgb.redValue
        self.rgb.greenValue =  value.rgb.greenValue
        self.rgb.blueValue = value.rgb.blueValue
        self.rgb.redOperation  = value.rgb.redOperation
        self.rgb.greenOperation = value.rgb.greenOperation
        self.rgb.blueOperation = value.rgb.blueOperation
        self.color = value.color
        self.originalImage = value.originalImage
    def setImage(self, value):
        self.originalImage = value