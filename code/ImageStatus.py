from Snapshot import Snapshot
class ImageStatus:
    def __init__(self):
        self.currentIndex = 0
        self.snapshots = []
        self.snapshots.append(Snapshot())

    def addSnapshotRGB(self, rgbValue, rgbOperation):
        # Todo IF next exsists  - delete ALL next
        new = Snapshot()
        new.myCopy(self.snapshots[self.currentIndex])
        new.setRGB(rgbValue, rgbOperation)
        self.snapshots.append(new)
        self.currentIndex = self.currentIndex + 1


