import argparse
import os
import io
import requests
import math
import threading
from PIL import Image
from places.google_places_helper import fetch_photos_for_place_id
from photocollage.collage import Page, Photo
from photocollage.render import RenderingTask, build_photolist
from django.conf import settings

class UserCollage(object):
    """Represents a user-defined collage
    A UserCollage contains a list of photos (referenced by filenames) and a
    collage.Page object describing their layout in a final poster.
    """
    def __init__(self, photolist):
        self.photolist = photolist

    def make_page(self, opts):
        # Define the output image height / width ratio
        ratio = 1.0 * opts.out_h / opts.out_w

        # Compute a good number of columns. It depends on the ratio, the number
        # of images and the average ratio of these images. According to my
        # calculations, the number of column should be inversely proportional
        # to the square root of the output image ratio, and proportional to the
        # square root of the average input images ratio.
        avg_ratio = (sum(1.0 * photo.h / photo.w for photo in self.photolist) /
                     len(self.photolist))
        # Virtual number of images: since ~ 1 image over 3 is in a multi-cell
        # (i.e. takes two columns), it takes the space of 4 images.
        # So it's equivalent to 1/3 * 4 + 2/3 = 2 times the number of images.
        virtual_no_imgs = 2 * len(self.photolist)
        no_cols = int(round(math.sqrt(avg_ratio / ratio * virtual_no_imgs)))
        self.page = Page(opts.out_w, ratio, no_cols)
        
        for photo in self.photolist:
            self.page.add_cell(photo)
        self.page.adjust()

class Options(object):
    def __init__(self):
        self.border_w = 0.05
        self.border_c = "white"
        self.out_w = 1200
        self.out_h = 628

def on_fail(exception):
            print(exception)

def create_collage_for_place(place_id, filename):
    #place_id = "ChIJc3Lll6YEdkgRPJboSPvZGwQ"
    photos = fetch_photos_for_place_id(place_id, 5)
    photolist = []
    for photo in photos:
        print(photo)
        response = requests.get(photo)
        photolist.append(io.BytesIO(response.content))

    collage = UserCollage(build_photolist(photolist))
    collage.make_page(Options())
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    t = RenderingTask(collage.page,output_file=filename, quality=2, on_fail=on_fail)
    t.start()
    t.join(5)
    if not os.path.exists(filename):
        return None
    return filename