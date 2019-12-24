# author: nurw
#
# straight forward monthly data (column weatherevent still contains weather events not reported)

from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_weather(beginmonth, endmonth, year):
    weather = []
    for month in range(beginmonth, endmonth):
        theurl = 'https://freemeteo.co.id/weather/jakarta/history/monthly-history/?gid=1642911&station=26293&month=' + str(
            month) + '&year=' + str(year) + '&language=english&country=indonesia'

        thepage = requests.get(theurl)
        soup = BeautifulSoup(thepage.text, 'html.parser')

        for temp in soup.find_all('div', attrs={'class': 'table hourly'}):
            for i in range(1, len(temp.find_all('tr'))):
                weather.append(
                    [temp.find_all('tr')[i].find_all('td')[0].text, temp.find_all('tr')[i].find_all('td')[1].text,
                     temp.find_all('tr')[i].find_all('td')[2].text, temp.find_all('tr')[i].find_all('td')[3].text,
                     temp.find_all('tr')[i].find_all('td')[9].text])

    dfweather = pd.DataFrame(weather, columns=['date', 'mintemp', 'maxtemp', 'windspeed', 'weatherevent'])

    dfweather.to_csv('weather.csv', index=False)


if __name__ == '__main__':
    print("""
    To use this: input year of the weather you want to extract (e.g. 2019).
    input range months (e.g. begin month=1, end month=10 => it means jan to september)
    
    For this version the city set to Jakarta.
    """)
    year = int(input('Year: '))
    begin_month = int(input('Begin month: '))
    end_month = int(input('End month: '))
    print('Processing...')
    get_weather(begin_month, end_month, year)
    print('it finished, check weather.csv in your directory')
