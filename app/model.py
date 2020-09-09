import numpy as np
import onnxruntime as rt
from PIL import Image
from io import BytesIO
from pathlib import Path

from google.cloud import storage
bucket_name = "toonify-models"
blob_name = "model.onnx"

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    print("downloading blob")
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )


def run(image_in):
    im = Image.open(image_in)
    im = im.resize((512, 512))
    im_array = np.array(im, np.float32)
    im_array = (im_array/255)*2 - 1
    im_array = np.transpose(im_array, (2, 0, 1))
    im_array = np.expand_dims(im_array, 0)

    if not Path(blob_name).exists():
        print("getting model and session")
        download_blob(bucket_name, blob_name, blob_name)
    
    sess = rt.InferenceSession(blob_name)

    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name

    print("starting inference...")
    pred = sess.run(
        [output_name], {input_name: im_array})[0]
    print("finished!")

    pred = np.squeeze(255*(pred + 1)/2)
    pred = np.transpose(pred, (1, 2, 0))

    out_im = Image.fromarray(pred.astype(np.uint8))
    png_output = BytesIO()
    out_im.save(png_output, format="jpeg")
    return png_output