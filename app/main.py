import os
from base64 import b64encode

from flask import Flask, request, render_template

import model

app = Flask(__name__)


@app.route('/')
def hello_world():
    name = os.environ.get('NAME', 'World')
    return 'Hello {}!'.format(name)

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image_out = model.run(image)
            data = image_out.getvalue()
            data_url = f"data:image/jpg;base64,{b64encode(data).decode()}"
            return render_template("show_image.html", image=data_url)

    return render_template("upload_image.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
