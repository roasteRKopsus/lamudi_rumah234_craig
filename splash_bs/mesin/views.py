from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.utils import requote_uri

from . import models

# Create your views here.


LAMUDI_URL = 'https://www.lamudi.co.id/buy/?q={}'
OLX_URL = 'https://www.rumah.com/properti-dijual?freetext={}&market=residential&property_type_code[]=BUNG&property_type=B&ps=1'


def home_request(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_post_lamudi = []
    # LAMUDI SECTION

    final_url_lamudi = LAMUDI_URL.format(quote_plus(search))

    response_lamudi = requests.get(final_url_lamudi)
    headers = requests.utils.default_headers()
    headers.update({'user-agent': 'GoogleChrome'})

    data_lamudi = response_lamudi.text
    soup_lamudi = BeautifulSoup(data_lamudi, 'lxml')
    post_listing_lamudi = soup_lamudi.find_all(
        class_='card ListingCell-content js-MainListings-container ListingCell-wrapper')

    for post in post_listing_lamudi:
        post_title_lamudi = post.find(class_='ListingCell-KeyInfo-title').text

        post_title_lamudi = post_title_lamudi.strip()

        post_link_lamudi = post.find('a').get('href')

        if post.find(class_='PriceSection-FirstPrice'):
            post_price_lamudi = post.find(class_='PriceSection-FirstPrice').text
        else:
            post_price_lamudi = 'N/A'

        post_image_id = post.find(class_='ListingCell-image').img['data-src']

        final_post_lamudi.append((post_title_lamudi, post_price_lamudi, post_link_lamudi, post_image_id))
    # OLX SECTIONS

    final_url_olx = OLX_URL.format(quote_plus(search))
    print(final_url_olx)
    response_olx = requests.get(final_url_olx, )
    print(response_olx)
    headers = requests.utils.default_headers()
    headers.update({'user-agent': 'Google post_price_olx2Chrome'})

    final_post_olx = []


    data_olx = response_olx.content
    soup_olx = BeautifulSoup(data_olx, 'html.parser')

    post_listing_olx = soup_olx.find_all(class_='gallery-container')


    post_listing_olx_harga = soup_olx.find_all(class_='list-price pull-left')

    for post in post_listing_olx:
        post_title_olx = post.find('a').get('title')
        post_image_id_olx = post.find('img').get('content')
        post_link_olx = post.find('a').get('href')
        post_price_olx2 = []

    for post in post_listing_olx_harga:
        post_price_olx = post.find(class_='price').text
        post_price_olx2.append(post_price_olx)


        final_post_olx.append((post_title_olx, post_image_id_olx, post_link_olx, post_price_olx))


    for_frontend = {
        'search': search,
        'final_post': final_post_lamudi,
        'final_post2': final_post_olx,

    }

    return render(request, 'mesin/new_search.html', for_frontend)
