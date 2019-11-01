from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRAIGSLIST_URL = "https://toronto.craigslist.org/search/?query={}"
IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search) + "&sort=rel")
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    # the 'a' is for the html tag <a>, looking for all classes with name result title
    post_listings = soup.find_all('li', {'class': 'result-row'})
    # img_src = post_listings[0].find('img').get('src')

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        """
        post_img_id = str(post.find('a').get('data-ids')).strip()
        if post_img_id != "None":
            post_image = "https://images.craiglist.org/" + post_img_id.split(",")[0][1:] + "_300x300.jpg"
        else:
            post_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDM-Zv5KaR07BWyyv8Vo2Y5AzUrZCXyHqxnuOFa2XCAR5mQDqZ&s"
        """

        """
        post_img = ""
        response_2 = requests.get(post_url)
        data_2 = response_2.text
        soup_2 = BeautifulSoup(data_2, features='html.parser')
        imgs = soup_2.find_all('img')
        for item in imgs:
            post_img = item['src']
        """
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        if post.find(class_='result-image').get('data-ids'):
            id = post.find(class_='result-image').get('data-ids').split(",")[0][2:]
            post_image = IMAGE_URL.format(id)
        else:
            post_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDM-Zv5KaR07BWyyv8Vo2Y5AzUrZCXyHqxnuOFa2XCAR5mQDqZ&s"

        final_postings.append((post_title,post_url,post_price,post_image))

    """
    post_title = post_listings[0].find(class_= 'result-title').text
    post_url = post_listings[0].find('a').get('href')
    post_price=post_listings[0].find(class_='result-price').text
    print(post_title)
    print(post_url)
    print(post_price)
    # print(img_src)
    for item in imgs:
        print(post_title)
        print("=================================================================================================")
        print(item['src'])
        print("=================================================================================================")
    """
    stuff_for_frontend = {
        'search' : search,
        'final_postings' : final_postings
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)