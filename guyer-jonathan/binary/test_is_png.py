from is_png import is_png

def test_is_png():
    assert is_png("data/PNG_transparency_demonstration_1.png")

def test_is_not_png():
    assert not is_png("data/not_png.txt")

def test_broken_png():
    assert not is_png("data/broken.png")
