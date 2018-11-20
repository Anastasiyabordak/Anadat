from RGB import RGB


class Snapshot:
    def __init__(self):
        self.rgb = RGB()

    def setRGB(self, rgbValue, rgbOperation):
        self.rgb.setRGB(rgbValue, rgbOperation)

    def resetRGB(self):
        self.rgb.setRGB()
