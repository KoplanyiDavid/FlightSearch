from constants import AMADEUS_API_KEY, AMADEUS_API_SECRET, TOKEN_ENDPOINT, IATA_ENDPOINT, FLIGHT_ENDPOINT
import requests
from requests import HTTPError

class FlightSearch:

    def __init__(self):
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': AMADEUS_API_KEY,
            'client_secret': AMADEUS_API_SECRET
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        response.raise_for_status()
        return response.json()['access_token']
    
    def get_iata_code(self, city_name: str) -> str:
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "1",
            "include": "AIRPORTS",
        }
        response = requests.get(
            url=IATA_ENDPOINT,
            headers=headers,
            params=query
        )

        try:
            response.raise_for_status()
        except HTTPError as err:
            if err.response.status_code == 404:
                print('Page not found')
            elif err.response.status_code == 401:
                print('Unauthorized access')
            else:
                print(f'HTTP error occurred: {err}')
        
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code
    
    def get_flights(self, origin_location_code: str, destination_location_code: str, departure_date: str, return_date: str, adults: int, non_stop: str):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_location_code,
            "destinationLocationCode": destination_location_code,
            "departureDate": departure_date,
            "returnDate": return_date,
            "nonStop": non_stop,
            "currencyCode": "EUR",
            "adults": adults,
            "max": 1
        }

        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query
        )

        try:
            response.raise_for_status()
        except HTTPError as err:
            if err.response.status_code == 404:
                print('Page not found')
                return "N/A"
            elif err.response.status_code == 401:
                print('Unauthorized access')
                return "N/A"
            else:
                print(f'HTTP error occurred: {err}')
                return "N/A"
            
        else:
            try:
                code = response.json()
            except IndexError:
                print(f"IndexError")
                return "N/A"
            except KeyError:
                print(f"KeyError")
                return "Not Found"
            else:
                return code