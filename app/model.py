import numpy as np
import onnxruntime as rt
from PIL import Image
from io import BytesIO
from pathlib import Path

MODEL_FILE = "model.onnx"
session = rt.InferenceSession(MODEL_FILE)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

def run(image_in):
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

    out_im = Image.fromarray(pred.astype(np.uint8))
    png_output = BytesIO()
    out_im.save(png_output, format="jpeg")
    return png_output