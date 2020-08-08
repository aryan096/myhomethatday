from django.http import HttpResponse
from django.shortcuts import render
import requests
import datetime
import json
import config 

def home(request):
    '''
    The home will just cycle through the images of yesterday
    '''

    api_key = config.api_key

    # First we need to get yesterday's date
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    # Next, we can make a request url using yesterday's date and API key
    request_url = "https://api.nasa.gov/EPIC/api/natural/date/" + str(yesterday) + "?api_key=" + api_key
    print(request_url)
    # next, we can request the API endpoint and get the images json
    response = requests.get(request_url)
    images_json = response.json()

    images = []
    # iterate through the list of images, we get a dict of each image with useful information
    for image_data in images_json:
        # for each image, we store its id, time, url
        image = {}
        image['id'] = image_data['identifier']
        image['time'] = image_data['date'].split()[1]
        url = 'https://api.nasa.gov/EPIC/archive/natural/' + str(yesterday.year) + '/' + str('{:02d}'.format(yesterday.month)) + '/' \
            + str('{:02d}'.format(yesterday.day)) + '/png/' + image_data['image'] + '.png?api_key=' + api_key
        image['url'] = url
        images.append(image)

    return render(request, 'myhome/home.html', {
        'date': str(yesterday),
        'images': images
    })