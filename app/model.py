import numpy as np
import PIL
from PIL import Image, ImageOps
from pathlib import Path
import face_detection
import requests

from io import BytesIO

from dotenv import load_dotenv
load_dotenv()
import os

import main

api_key = os.getenv("DEEP_AI_KEY")
TIMEOUT = 30
API_URL = "https://api.deepai.org/api/toonify"

message = {
            "NO_FACES": "Didn't find any faces in the supplied image.",
            "MULTIPLE_FACES": "Found more than one face, processing just the first.",
            "BAD_IMAGE": "Image file could not be opened.",
            "API_FAIL": "Problem talking to the DeepAI backend."
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
        try:
            im = ImageOps.exif_transpose(im)
        except:
            print("exif problem, not rotating")
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
        try:
            result["toonified_image"] = toonify(result["aligned_image"])
        except Exception as e:
            main.log("ERROR", "problem during request")
            main.log("ERROR", str(e))
            result["status"] = "fail"
            result["message"] = message["API_FAIL"]
    
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

    file_output = BytesIO()
    im.save(file_output, format="jpeg", quality=90)
    data = file_output.getvalue()
    
    main.log("DEBUG", "Sending request...")
    r = requests.post(
        API_URL,
        data={'align_face': "False"},
        files={'image': data},
        headers={'api-key': api_key},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    result = r.json()
    main.log("DEBUG", "Finished request")
        
    return result["output_url"]
    

