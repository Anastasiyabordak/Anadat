from Snapshot import Snapshot
class ImageStatus:
    def __init__(self):
        self.currentIndex = 0
        self.snapshots = []
        self.snapshots.append(Snapshot())

    def addSnapshot(self, rgbValue, rgbOperation):
        new = Snapshot()
        new.setRGB(rgbValue, rgbOperation)
        self.snapshots.append(new)
        self.currentIndex = self.currentIndex + 1