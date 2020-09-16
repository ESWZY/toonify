import model

from PIL import Image

# Successes

def test_face_detection():
    """Working face detection"""
    image_in = "test_data/face-ok.jpg"
    result = model.run(image_in)

    assert result["status"] == "success"
    assert isinstance(result["aligned_image"], Image.Image)
    assert isinstance(result["toonified_image"], Image.Image)
    assert result["message"] == ""

def test_face_detection_multi_face():
    """Uses first face if many found"""
    image_in = "test_data/two-face.jpg"
    result = model.run(image_in)

    assert result["status"] == "success"
    assert isinstance(result["aligned_image"], Image.Image)
    assert isinstance(result["toonified_image"], Image.Image)
    assert result["message"] == model.message["MULTIPLE_FACES"]

def test_face_detection_transparent():
    """Working face detection on transparent image"""
    image_in = "test_data/face-alpha.png"
    result = model.run(image_in)

    assert result["status"] == "success"
    assert isinstance(result["aligned_image"], Image.Image)
    assert isinstance(result["toonified_image"], Image.Image)
    assert result["message"] == ""

# Failures

def test_face_detection_no_face():
    """Fails if no faces found"""
    image_in = "test_data/no-face.jpg"
    result = model.run(image_in)

    assert result["status"] == "fail"
    assert result["aligned_image"] == None
    assert result["toonified_image"] == None
    assert result["message"] == model.message["NO_FACES"]

def test_face_detection_bad_file():
    """Fails if bad file"""
    image_in = "test_data/not-image.jpg"
    result = model.run(image_in)

    assert result["status"] == "fail"
    assert result["aligned_image"] == None
    assert result["toonified_image"] == None
    assert result["message"] == model.message["BAD_IMAGE"]