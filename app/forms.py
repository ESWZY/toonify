from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from flask_wtf.recaptcha import RecaptchaField

class ImageForm(FlaskForm):
    image = FileField("Upload an image!", validators=[FileRequired()])
    # recaptcha = RecaptchaField()