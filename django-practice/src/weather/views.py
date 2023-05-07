from django.shortcuts import render, HttpResponse

import requests
from bs4 import BeautifulSoup as bs

def get_weather_city(city):
    city = city.replace(' ','+')
    url = f'https://www.google.com/search?q=weather+of+{city}'
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    LANGUAGE = 'en-GB,en-US;q=0.9,en;q=0.8'
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    response = session.get(url)
    soup = bs(response.text, 'html.parser')

    results = {}
    results['region'] = soup.find('span', attrs={'class':'BBwThe'}).text
    results['daytime'] = soup.find('div', attrs={'id': 'wob_dts'}).text.replace("\u202f"," ")
    results['weather'] = soup.find('span', attrs={'id': 'wob_dc'}).text
    results['temperature'] = soup.find('span', attrs={'id': 'wob_tm'}).text

    return results

# Create your views here.
def home_view(request):
    if request.method == "GET" and 'city' in request.GET:
        city = request.GET.get('city')
        results = get_weather_city(city)
        context = {'results': results}
    else:
        context = {}
    return render(request,'home.html', context)
