#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3

# <bitbar.title>Corona numbers plugin</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>langered</bitbar.author>
# <bitbar.author.github>langered</bitbar.author.github>
# <bitbar.desc>Plugin to query numbers of corona.</bitbar.desc>
# <bitbar.image>http://www.hosted-somewhere/pluginimage</bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>http://url-to-about.com/</bitbar.abouturl>

import requests
import yaml

CORONA_BASIC_REQUEST_URL='https://wuhan-coronavirus-api.laeyoung.endpoint.ainize.ai/jhu-edu'

class CoronaData:
    def __init__(self, confirmed = 0, recovered = 0, deaths = 0, countryregion = ''):
        self.confirmed = confirmed
        self.recovered = recovered
        self.deaths = deaths
        self.countryregion = countryregion
    def __str__(self):
        return f'Confirmed: {self.confirmed}, Recovered: {self.recovered}, Deaths: {self.deaths}, Countryregion: {self.countryregion}'
    def print_bitbar(self):
        confirmed_value = str(self.confirmed) + ' | color=blue'
        recovered_value = str(self.recovered) + ' | color=green'
        deaths_value = str(self.deaths) + ' | color=red'

        output = """%s
%s
%s
%s """ % (self.countryregion, confirmed_value, recovered_value, deaths_value)
        return output

def total_numbers():
    total_corona_number_url = CORONA_BASIC_REQUEST_URL + '/brief'
    corona_json = __get_corona_data(total_corona_number_url)
    if corona_json == {}:
        return CoronaData()
    return CoronaData(corona_json['confirmed'], corona_json['recovered'], corona_json['deaths'])

def numbers_by_country(iso2_country_code):
    total_corona_number_url = CORONA_BASIC_REQUEST_URL + '/latest'
    params = {
            "iso2": iso2_country_code.upper()
    }
    corona_json = __get_corona_data(total_corona_number_url, params)
    if corona_json == {}:
        return CoronaData()
    return CoronaData(corona_json[0]['confirmed'], corona_json[0]['recovered'], corona_json[0]['deaths'], corona_json[0]['countryregion'])

def __get_corona_data(url, params = {}):
    response = requests.get(url, params)
    if response.status_code != 200:
        return {}
    return response.json()



# with open("config.yml", "r") as ymlfile:
#     cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

total_corona_numbers = total_numbers()
print(total_corona_numbers.print_bitbar())

print('---')
numbers_of_country = numbers_by_country('de')
print(numbers_of_country.print_bitbar())
