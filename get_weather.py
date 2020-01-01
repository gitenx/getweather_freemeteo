# author: nurw
#
# straight forward monthly data (column weatherevent still contains weather events not reported)

from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date


def get_weather(beginmonth, endmonth, year):
    weather = []

    for month in range(beginmonth, endmonth+1):
        theurl = 'https://freemeteo.co.id/weather/jakarta/history/monthly-history/?gid=1642911&station=26293&month=' + str(month) + '&year=' + str(year) + '&language=english'

        thepage = requests.get(theurl)
        soup = BeautifulSoup(thepage.text, 'html.parser')

        for temp in soup.find_all('div', attrs={'class': 'table hourly'}):
            if len(temp.find_all('tr')) > 1:
                for i in range(1, len(temp.find_all('tr'))):
                    weather.append([temp.find_all('tr')[i].find_all('td')[0].text, temp.find_all('tr')[i].find_all('td')[1].text, 
                        temp.find_all('tr')[i].find_all('td')[2].text, temp.find_all('tr')[i].find_all('td')[3].text,
                        temp.find_all('tr')[i].find_all('td')[9].text])
            else:
                print('weather information not found!')
                break

    dfweather = pd.DataFrame(weather, columns=['date', 'mintemp', 'maxtemp', 'windspeed', 'weatherevent'])
    fname = 'weather_jkt_{}{}{}_{}'.format(begin_month, end_month, year,date.today())

    dfweather.to_csv(fname + '.csv', index=False)


def find_city(city):
    found = True
    result = ''

    theurl = 'https://freemeteo.co.id/weather/search/?q=' + city + '&pg=0&language=english'

    thepage = requests.get(theurl)
    soup = BeautifulSoup(thepage.text, 'html.parser')

    for c in soup.find_all('p', attrs={'class': 'title no-results'}):
        result = c.find_all('span')[0].text
    
    if result == 'Sorry, no results':
        found = False
    else:
        found = True
    
    return found


if __name__ == '__main__':
    print("""
    How to use:
    - input year of the weather you want to extract (e.g. 2019).
    - input range months (e.g. begin month=1, end month=10 => it means jan to oct)
    """)
    while True:
        try:
            # city =  input('City: ')
            year = int(input('Year: '))
            begin_month = int(input('Begin month: '))
            end_month = int(input('End month: '))

            if not int(year) or not int(begin_month) or not int(end_month):
                raise ValueError('cannot leave everything empty')
            else:
                if year < 0 or len(str(year)) < 4 or begin_month < 0 or end_month < 0 or begin_month > 12 or end_month > 12 or begin_month > end_month:
                    print('year or begin month or end month might be wrong, please check!\n')
                else:
                    print('Processing...')
                    get_weather(begin_month, end_month, year)
                    print('it finished, csv file in your directory')

                    break

        except ValueError as e:
            print(e)
            

