import os
from io import BytesIO

from PIL import Image
from pyimgur import Imgur
from PyMatcha.utils.static import IMGUR_CLIENT_ID
from PyMatcha.utils.static import IMGUR_CLIENT_SECRET

imgur_client = Imgur(client_id=IMGUR_CLIENT_ID, client_secret=IMGUR_CLIENT_SECRET)


def upload_image(bytesio_img: BytesIO, username: str):
    path = f"{username}.png"
    Image.open(bytesio_img).convert("RGB").save(path)
    uploaded_image = imgur_client.upload_image(path=path, title=username)
    os.remove(path)
    return uploaded_image.link
