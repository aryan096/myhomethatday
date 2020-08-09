from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import datetime
import json
import config
from myhome.forms import SearchDateForm
from PIL import Image
from io import BytesIO
import imageio

def generate_gif(urls):
    images = []
    for url in urls:
        im = imageio.imread(url)
        images.append(im)

    imageio.mimsave('haha.gif', images, duration=0.5)

def get_and_render_images(request, date_object):
    '''
    This is the main helper function that does the bulk of the logic. It gets the API Key from the config file,
    creates the request URL from the API using the passed in date object, gets the json, parses it, creates a
    list of all the images for the given date, handles the form, and renders the html for the given date
    '''
    # get the api key
    api_key = config.api_key

    # Next, we can make a request url using the date_object parameter and API key
    request_url = "https://api.nasa.gov/EPIC/api/natural/date/" + str(date_object) + "?api_key=" + api_key

    # next, we can request the API endpoint and get the images json
    response = requests.get(request_url)
    images_json = response.json()

    images = []
    urls = []
    # iterate through the list of images, we get a dict of each image with useful information
    for image_data in images_json:
        # for each image, we store its id, time, url
        image = {}
        image['id'] = image_data['identifier']
        image['time'] = image_data['date'].split()[1]
        url = 'https://api.nasa.gov/EPIC/archive/natural/' + str(date_object.year) + '/' + str('{:02d}'.format(date_object.month)) + '/' \
            + str('{:02d}'.format(date_object.day)) + '/png/' + image_data['image'] + '.png?api_key=' + api_key
        image['url'] = url
        urls.append(url)
        images.append(image)



    # FORM HANDLING
    if request.method == 'POST':
        form = SearchDateForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            date = form.cleaned_data['search_date']
            date = date.strftime('%Y-%m-%d')
            return redirect('/'+ date)

        else:
            date = date_object

    else:
        date = date_object
        form = SearchDateForm(initial={'search_date': date})


    return render(request, 'myhome/home2.html', {
        'date': str(date_object),
        'images': images,
        'form': form,
    })

def home(request):
    '''
    The home function calls the get_and_render_images function using yesterday's date
    '''

    # First we need to get yesterday's date
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    return get_and_render_images(request, yesterday)


def parse_date(date):
    '''
    This function parses a passed in date string (formatted like 2020-05-05) and returns
    a datetime object of the same date
    '''
    date_split = date.split('-')
    year = int(date_split[0])
    month = int(date_split[1])
    day = int(date_split[2])

    datetime_object = datetime.datetime(year,month,day)
    return datetime_object

def search(request, date):
    '''
    This function renders the page for a user selected date through the form
    It creates a datetime object using the parse_date function and then calls the
    get_and_render_images function
    '''
    return get_and_render_images(request, parse_date(date).date())
