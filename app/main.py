import os
from base64 import b64encode

from flask import Flask, request, render_template

from io import BytesIO
import model
import face_detection

app = Flask(__name__)

def url_encode_image(image, im_format="jpeg"):
    """Encode PIL image as url"""
    file_output = BytesIO()
    image.save(file_output, format=im_format)
    data = file_output.getvalue()
    data_url = f"data:image/{im_format};base64,{b64encode(data).decode()}"
    return data_url

def process_image():

    image = request.files["image"]
    display_images = None

    filename = image.filename
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in [".jpg", ".jpeg", ".png", ".bmp"]:
            return "fail", "Not a valid file type", (None, None)

    result = model.run(image)

    if result["status"] == "success":
        display_images = (
                            url_encode_image(result["aligned_image"]),
                            url_encode_image(result["toonified_image"]),
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
            except:
                status = "fail"
                message = "Something unexpected happened..."
                display_images = (None, None)
            return render_template("upload_image.html", 
                            status=status,
                            images=display_images,
                            message=message)
    
    return render_template("upload_image.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
