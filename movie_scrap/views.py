from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from .models import *
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

engine = create_engine('postgresql://postgres:1234@localhost:5432/movie_data')

def home(request):
    return render(request, 'home.html', {'name': 'Sandesh'})


'''def add(request):
    val1 = int(request.POST["num1"])
    val2 = int(request.POST["num2"])
    result = int(val1 + val2)
    return render(request, 'result.html', {'result': result})
'''


def movie(request):
    movie_name = request.GET['Movie_name']

    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    browser = webdriver.Chrome(options=op)
    browser.get('https://www.imdb.com/')
    '''response = requests.get('https://www.imdb.com/')
    soup = BeautifulSoup(response.text,'html.parser')
    '''
    # movie_name = input()
    search_bar = browser.find_element_by_css_selector('#suggestion-search')
    search_bar.send_keys(movie_name)
    search_bar.submit()
    title_url = browser.current_url
    browser.maximize_window()  # For maximizing window
    browser.implicitly_wait(20)  # gives an implicit wait for 20 s
    title_name = browser.find_element_by_css_selector('#main > div > div.findSection > table > tbody > tr.findResult.odd > td.result_text > a')
    print(title_name)
    title_name.click()

    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')
    movie_container = soup.findAll('div', class_='title_bar_wrapper')
    movie_genre_container = []
    for movie in movie_container:
        movie_rating = float(movie.find('div', {"class": "ratingValue"}).find('strong').find('span', {
            "itemprop": "ratingValue"}).get_text())

        #print(movie_rating)
        movie_genre = movie.find('div', {'class': 'subtext'}).findAll('a')
        for i in range(0, len(movie_genre) - 1):
            value = str(movie_genre[i].get_text())
            movie_genre_container.append(value)


    data_col = pd.DataFrame({'movie_name':movie_name,'movie_rating': movie_rating,'movie_genre':movie_genre_container})
    data_col.to_sql('movie_scrap_movie_data', engine, if_exists='append',index=False)
    #data_col.to_sql('movie_scrap_movie_scrap', database_url, if_exists='append', index=True)

    return render(request, 'result.html', {'result': data_col})
# Create your views here.

def Genre(request):
    genre = request.GET['Genre']
    obj = movie_data.objects.filter(movie_genre=genre)
    total= 0
    rating = []
    for k in obj:
        rating.append(k.movie_rating)
    for i in rating:
        total += i
        rating_avg = float(total/len(rating))

    return render(request,'rating_avg.html',{'rating_avg':rating_avg})

'''
def Romance(request):
    return render(request, 'home.html')
'''