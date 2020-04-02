import os
from urllib.parse import urlparse
from places.constants import BLACKLISTED_DOMAINS
from django.conf import settings
from places.images_helper import create_collage_for_place

def check_link_against_blacklist(link):
    if link:
        parsed = urlparse(link)
        if parsed.hostname.replace('www.', '') in BLACKLISTED_DOMAINS:
            return None
    return link

def get_place_collage_picture(place_id):
    FILENAME = "{PLACES_MEDIA_ROOT}/{PLACE_ID}/{PLACE_ID}.jpg"
    filename = FILENAME.format(
        PLACES_MEDIA_ROOT = settings.PLACES_MEDIA_ROOT,
        PLACE_ID = place_id
    )
    if not os.path.exists(filename):
        filename = create_collage_for_place(place_id, filename)
    return filename
