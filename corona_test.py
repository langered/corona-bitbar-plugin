import unittest
import requests
from unittest.mock import patch

from corona import total_numbers, numbers_by_country, CoronaData

CORONA_BASIC_REQUEST_URL='https://wuhan-coronavirus-api.laeyoung.endpoint.ainize.ai/jhu-edu'

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

def mocked_successful_requests_get(*args, **kwargs):
    url = args[0]
    params = args[1]
    if url == CORONA_BASIC_REQUEST_URL + '/brief' and params == {}:
        return MockResponse({'confirmed': 1234, 'deaths': 666, 'recovered': 123}, 200)
    elif url == CORONA_BASIC_REQUEST_URL + '/latest' and params == {"iso2": "DE"}:
        return MockResponse([{'confirmed': 10, 'deaths': 1, 'recovered': 6, 'countryregion': 'Germany'}], 200)

    return MockResponse(None, 404)

def mocked_failing_requests_get(*args, **kwargs):
    return MockResponse(None, 404)

class CoronaTest(unittest.TestCase):

    #
    # test total numbers
    #
    @patch('requests.get', side_effect=mocked_successful_requests_get)
    def test_total_numbers(self, mock_get):
        expected_corona_data = CoronaData(1234, 123, 666)
        compare_corona_data(self, total_numbers(), expected_corona_data)

    @patch('requests.get', side_effect=mocked_failing_requests_get)
    def test_total_numbers_failed_request(self, mock_request_get):
        expected_corona_data = CoronaData(0, 0, 0)
        compare_corona_data(self, total_numbers(), expected_corona_data)

    #
    # test number by country
    #
    @patch('requests.get', side_effect=mocked_successful_requests_get)
    def test_numbers_by_country(self, mock_request_get):
        expected_corona_data = CoronaData(10, 6, 1, 'Germany')
        compare_corona_data(self, numbers_by_country('de'), expected_corona_data)

    @patch('requests.get', side_effect=mocked_failing_requests_get)
    def test_numbers_by_country_failed_request(self, mock_request_get):
        expected_corona_data = CoronaData(0, 0, 0)
        compare_corona_data(self, numbers_by_country('de'), expected_corona_data)


def compare_corona_data(self, returned_data, expected_data):
    self.assertEqual(returned_data.confirmed, expected_data.confirmed)
    self.assertEqual(returned_data.recovered, expected_data.recovered)
    self.assertEqual(returned_data.deaths, expected_data.deaths)
    self.assertEqual(returned_data.countryregion, expected_data.countryregion)

