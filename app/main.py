import os
from base64 import b64encode
from io import BytesIO
import json

from flask import Flask, request, render_template

import model
import face_detection

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # upload limit

PROJECT = 'toonify';

def log(level, message):
    # Build structured log messages as an object.
    global_log_fields = {}

    # Add log correlation to nest all log messages
    # beneath request log in Log Viewer.
    trace_header = request.headers.get('X-Cloud-Trace-Context')

    if trace_header and PROJECT:
        trace = trace_header.split('/')
        global_log_fields['logging.googleapis.com/trace'] = (
            f"projects/{PROJECT}/traces/{trace[0]}")

    # Complete a structured log entry.
    entry = dict(severity=level,
                message=message,
                # Log viewer accesses 'component' as jsonPayload.component'.
                component='arbitrary-property',
                **global_log_fields)

    print(json.dumps(entry))

def url_encode_image(image, im_format="jpeg"):
    """Encode PIL image as url"""
    file_output = BytesIO()
    image.save(file_output, format=im_format, quality=90)
    data = file_output.getvalue()
    data_url = f"data:image/{im_format};base64,{b64encode(data).decode()}"
    return data_url

def process_image():

    image = request.files["image"]
    display_images = None

    filename = image.filename
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext.lower() not in [".jpg", ".jpeg", ".png", ".bmp"]:
            return "fail", "Not a supported file type", (None, None)

    result = model.run(image)

    if result["status"] == "success":
        display_images = (
                            url_encode_image(result["aligned_image"]),
                            result["toonified_image"],
                         )

    return result["status"], result["message"], display_images

@app.route('/poke')
def hello_world():
    return "awake!"

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            try:
                status, message, display_images = process_image()
            except Exception as e:
                status = "fail"
                message = "Something unexpected happened..."
                display_images = (None, None)
                log("ERROR", str(e))
                
            if status == "fail":
                log("NOTICE", message)

            return render_template("upload_image.html", 
                            status=status,
                            images=display_images,
                            message=message)
    
    return render_template("upload_image.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
