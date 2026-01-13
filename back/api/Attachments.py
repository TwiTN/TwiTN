import os
from flask import request, session, send_from_directory
from flask_openapi3 import APIBlueprint
from werkzeug.utils import secure_filename

from lib.make_error import make_error
from .tags import attachment_tag

UPLOAD_FOLDER = "back/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

api = APIBlueprint("Attachments", __name__, url_prefix="attachments")


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@api.post(
    "/",
    tags=[attachment_tag],
    summary="Upload a file",
)
def upload_attachment():
    # Auth simple via session
    if "user_id" not in session:
        return make_error(401, "Unauthorized")

    if "file" not in request.files:
        return make_error(400, "No file provided")

    file = request.files["file"]

    if file.filename == "":
        return make_error(400, "Empty filename")

    if not allowed_file(file.filename):
        return make_error(400, "File type not allowed")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    return {
        "filename": filename,
        "url": f"/attachments/{filename}",
    }


@api.get(
    "/<string:filename>",
    tags=[attachment_tag],
    summary="Download a file",
)
def download_attachment(filename: str):
    return send_from_directory(UPLOAD_FOLDER, filename)
