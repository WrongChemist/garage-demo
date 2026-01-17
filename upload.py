import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_car_image(file):
    if not file:
        return None
    filename = secure_filename(file.filename)
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    return filename
