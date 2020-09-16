import numpy as np
import onnxruntime as rt
import PIL
from PIL import Image
from pathlib import Path
import face_detection

MODEL_FILE = "model.onnx"
session = rt.InferenceSession(MODEL_FILE)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

message = {
            "NO_FACES": "Didn't find any faces in the supplied image.",
            "MULTIPLE_FACES": "Found more than one face, processing just the first.",
            "BAD_IMAGE": "Image file could not be opened",
          }

def run(image_in):
    """Apply complete workflow to raw image file and return results"""
    result = {
                "status": "success",
                "aligned_image": None,
                "toonified_image": None,
                "message": "",
             }

    try:
        im = Image.open(image_in)
        im = im.convert("RGB")
    except PIL.UnidentifiedImageError as err:
        result["status"] = "fail"
        result["message"] = message["BAD_IMAGE"]
        return result
    
    result["aligned_image"], n_faces = align(im)
    if n_faces == 0:
        result["status"] = "fail"
        result["message"] = message["NO_FACES"]
    elif n_faces > 1:
        result["message"] = message["MULTIPLE_FACES"]

    if result["aligned_image"]:
        result["toonified_image"] = toonify(result["aligned_image"])
    
    return result


def align(image_in):
    landmarks = list(face_detection.get_landmarks(image_in))
    n_faces = len(landmarks)
    if n_faces == 0:
        aligned_image = None
    else:
        aligned_image = face_detection.image_align(image_in, landmarks[0])

    return aligned_image, n_faces

def toonify(image_in):
    im = image_in
    im = im.resize((512, 512))
    im_array = np.array(im, np.float32)
    im_array = (im_array/255)*2 - 1
    im_array = np.transpose(im_array, (2, 0, 1))
    im_array = np.expand_dims(im_array, 0)

    print("starting inference...")
    pred = session.run([output_name], {input_name: im_array})[0]
    print("finished!")

    pred = np.squeeze(255*(pred + 1)/2)
    pred = np.transpose(pred, (1, 2, 0))

    return Image.fromarray(pred.astype(np.uint8))