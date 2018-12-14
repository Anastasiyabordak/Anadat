from RGB import RGB
from ImageStatus import ImageStatus


def test_set():
    temp = RGB()
    assert temp.blueOperation == ">="


def test_Snapshot():
    temp = ImageStatus()
    temp.addSnapshotRGB([1, 2, 3], ["=", "=", "="])
    assert [1, 2, 3, "=", "=", "="] == temp.getRGB()
    temp.addShanpshotImage([1, 2, 3], False)
    assert [1, 2, 3] == temp.getImage()
    assert [1, 2, 3, "=", "=", "="] == temp.getRGB()
    temp.addShanpshotImage([1, 2, 3], True)
    assert [1, 2, 3] == temp.getImage()
    assert [0, 0, 0, ">=", ">=", ">="] == temp.getRGB()
    assert len(temp.snapshots) == 4
    temp.setUndo()
    assert temp.currentIndex == 2
    assert [1, 2, 3] == temp.getImage()
    assert [1, 2, 3, "=", "=", "="] == temp.getRGB()
    temp.setUndo()
    assert temp.currentIndex == 1
    assert [1, 2, 3, "=", "=", "="] == temp.getRGB()
    temp.setUndo()
    assert temp.currentIndex == 0
    assert temp.getImage() == ()
    temp.setUndo()
    assert temp.currentIndex == 0
    temp.setRedo()
    assert temp.currentIndex == 1
    assert [1, 2, 3, "=", "=", "="] == temp.getRGB()
    temp.setRedo()
    assert temp.currentIndex == 2
    assert [1, 2, 3] == temp.getImage()
    assert [1, 2, 3, "=", "=", "="] == temp.getRGB()
    temp.setRedo()
    assert temp.currentIndex == 3
    assert [1, 2, 3] == temp.getImage()
    assert [0, 0, 0, ">=", ">=", ">="] == temp.getRGB()