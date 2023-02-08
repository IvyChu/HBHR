import os
import secrets
from PIL import Image
from flask import current_app
from hbhr import log

def check_picture_size(picture, width=400, height=400):
    if picture:
        i = Image.open(picture)
        if (i.size[0] < width) or (i.size[1] < height):
            return True
    return False

def cropbbox(imagewidth,imageheight, thumbwidth,thumbheight):
    """ cropbbox(imagewidth,imageheight, thumbwidth,thumbheight)

        Compute a centered image crop area for making thumbnail images.
          imagewidth,imageheight are source image dimensions
          thumbwidth,thumbheight are thumbnail image dimensions

        Returns bounding box pixel coordinates of the cropping area
        in this order (left,upper, right,lower).
    """
    # determine scale factor
    fx = float(imagewidth)/thumbwidth
    fy = float(imageheight)/thumbheight
    f = fx if fx < fy else fy

    # calculate size of crop area
    cropheight,cropwidth = int(thumbheight*f),int(thumbwidth*f)

    # for centering use half the size difference of the image and the crop area
    dx = (imagewidth-cropwidth)/2
    dy = (imageheight-cropheight)/2

    # return bounding box of centered crop area on source image
    return dx,dy, cropwidth+dx,cropheight+dy

def save_thumbnail(form_picture, width=400, height=400, path_to_pic='static/profile_pics', pic_name=''):
    if pic_name:
        random_hex = pic_name
    else:
        random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, path_to_pic, picture_fn)

    output_size = (width, height)

    i = Image.open(form_picture)

    # Make it crop the image to the exact size it needs to be for width/height with keeping the result aspect ratio
    img_width = i.width
    img_height = i.height

    bbox = cropbbox(img_width,img_height, width,height)
    im = i.crop(bbox)
    im.thumbnail(output_size)
    im.save(picture_path)

    log.debug(f"Saved thumb {picture_path}")

    return picture_fn


def save_photo(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/imgs', picture_fn)

    # Make a thumbnail
    thumbnail_hex = random_hex + '_th'
    thumbnail_fn = save_thumbnail(form_picture, path_to_pic='static/imgs',pic_name=thumbnail_hex)

    i = Image.open(form_picture)
    i.save(picture_path)

    log.debug(f"Saved pic {picture_path}")

    return (picture_fn, thumbnail_fn)
