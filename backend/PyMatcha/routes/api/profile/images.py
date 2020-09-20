from io import BytesIO

from flask import Blueprint
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.image import Image
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.images import upload_image
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput

images_bp = Blueprint("images", __name__)


@images_bp.route("/profile/images", methods=["POST"])
@jwt_required
def add_image_profile():
    is_primary = request.args.get("is_primary", "false") == "true"
    # check if the post request has the file part
    if "file[]" not in request.files:
        raise BadRequestError("No file passed in request")
    file = request.files["file[]"]
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == "":
        raise BadRequestError("No filename passed in request")
    if file:
        tmp_img = BytesIO()
        file.save(tmp_img)
        link = upload_image(tmp_img, current_user.username)
        # TODO: Check if an image is already primary
        # TODO: Check if no more than 5 images
        Image.create(current_user.id, link, is_primary=is_primary)
        return SuccessOutput("image", link)
    else:
        raise ValueError("NO FILE")


@images_bp.route("/profile/images/<image_id>", methods=["DELETE"])
@jwt_required
def delete_image_profile(image_id):
    try:
        image = Image.get(id=image_id)
    except ValueError:
        raise NotFoundError(f"Image not found for user {current_user.id}")
    image.delete()
    return Success("Image successfully deleted.")


@images_bp.route("/profile/images/<image_id>", methods=["PUT"])
@jwt_required
def change_main_image(image_id):
    try:
        image = Image.get(id=image_id)
    except ValueError:
        raise NotFoundError(f"Image not found for user {current_user.id}")
    try:
        current_main_image = Image.get_multi(user_id=current_user.id, is_primary=True)
    except NotFoundError:
        # That means there was no primary image before
        pass
    else:
        current_main_image.is_primary = False
        current_main_image.save()
    image.is_primary = True
    image.save()


@images_bp.route("/profile/images", methods=["GET"])
@jwt_required
def get_images_profile():
    images = Image.get_multis(user_id=current_user.id)
    ret = []
    if images:
        ret = [image.to_dict() for image in images]
    return SuccessOutput("images", ret)
