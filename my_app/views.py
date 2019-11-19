from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models
import sys


BASE_CRAIGSLIST_URL = "https://toronto.craigslist.org/search/?query={}"
IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    try:
        models.Search.objects.get(search=search)
    except Exception as e:
        models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search) + "&sort=rel")
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    # the 'a' is for the html tag <a>, looking for all classes with name result title
    post_listings = soup.find_all('li', {'class': 'result-row'})
    print(sys.getsizeof(str(post_listings)))
    # img_src = post_listings[0].find('img').get('src')

    output = create_entry_for_view(post_listings)

    stuff_for_frontend = {
        'search' : search,
        'final_postings' : output
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)


def create_entry_for_view(post_listings):
    final_postings = []
    count = 0

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        if post.find(class_='result-image').get('data-ids'):
            id = post.find(class_='result-image').get('data-ids').split(",")
            post_image = []
            for item in [item for item in id if item.strip() != ""]:
                post_image.append(IMAGE_URL.format(item[2:]))
        else:
            post_image = [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDM-Zv5KaR07BWyyv8Vo2Y5AzUrZCXyHqxnuOFa2XCAR5mQDqZ&s"]

        final_postings.append((post_title, post_url, post_price, post_image, count))
        count += 1
    return final_postings


