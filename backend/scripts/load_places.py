import django
import sys
import os
sys.path.append(os.path.dirname(__file__) + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'carebackend.settings'
django.setup()
from places.models import Neighborhood, NeighborhoodEntry, Place, Area
import pandas as pd
import sys

fl = sys.argv[1]

df = pd.read_csv(fl)

df = df.where(pd.notnull(df), None)

for _, row in df.iterrows():
    try:
        p = Place.objects.get(place_id=row['place_id'])
    except Place.DoesNotExist:
        p = Place(
            place_id=row['place_id'])
    
    p.lat = row['lat']
    p.lng = row['lng']
    p.address = row['formatted_address']
    p.user_rating = row['rating']
    if not p.name:
        p.name = row['name']
    p.num_ratings = row['user_ratings_total']
    p.place_url = '%.200s' % row['website']

    if row.get('gift_card_url') != None:
        p.gift_card_url = row.get('gift_card_url')

    #p.photo_attribution = row['image_attribution']
    p.image_url = row['photo_url']
            
    p.save()