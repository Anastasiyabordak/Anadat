from Snapshot import Snapshot


class ImageStatus:
    def __init__(self):
        self.currentIndex = 0
        self.snapshots = []
        self.snapshots.append(Snapshot())

    def addSnapshotRGB(self, rgbValue, rgbOperation):
        if self.currentIndex != 0:
            self.snapshots = self.snapshots[:self.currentIndex + 1]
        new = Snapshot()
        new.myCopy(self.snapshots[self.currentIndex])
        new.setRGB(rgbValue, rgbOperation)
        self.snapshots.append(new)
        self.currentIndex = self.currentIndex + 1

    def addSnapshotColor(self, color):
        if self.currentIndex != 0:
            self.snapshots = self.snapshots[:self.currentIndex + 1]
        new = Snapshot()
        new.myCopy(self.snapshots[self.currentIndex])
        new.setColor(color)
        self.snapshots.append(new)
        self.currentIndex = self.currentIndex + 1

    # update rgb - True - reset, False - prev rgb
    def addShanpshotImage(self, image, updateRGB):
        if self.currentIndex != 0:
            self.snapshots = self.snapshots[:self.currentIndex + 1]
        new = Snapshot()
        new.myCopy(self.snapshots[self.currentIndex])
        new.setImage(image)
        if updateRGB == True:
            new.setRGB()
            new.color = (0, 0, 0)
        self.snapshots.append(new)
        self.currentIndex = self.currentIndex + 1

    def getColor(self):
        return self.snapshots[self.currentIndex].color

    def getImage(self):
        return self.snapshots[self.currentIndex].originalImage

    def getRGB(self):
        return self.snapshots[self.currentIndex].getRGB()

    def setUndo(self):
        if self.currentIndex == 0:
            return False
        else:
            self.currentIndex = self.currentIndex - 1
            return True

    def setRedo(self):
        if self.currentIndex < len(self.snapshots) - 1:
            self.currentIndex = self.currentIndex + 1
            return True
        else:            
            return False

    def removeDub(self):
        self.snapshots = self.snapshots[:self.currentIndex]