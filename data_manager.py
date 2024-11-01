import requests
from requests import HTTPError
from constants import SHEET_URL, SHEETY_USERNAME, SHEETY_PWD

class DataManager:

    def get_sheet_data(self):
        resp = requests.get(url=SHEET_URL, auth=(SHEETY_USERNAME, SHEETY_PWD))
        try:
            resp.raise_for_status()
        except HTTPError as err:
            if err.response.status_code == 404:
                print('Page not found')
            elif err.response.status_code == 401:
                print('Unauthorized access')
            else:
                print(f'HTTP error occurred: {err}')

        data = resp.json()
        return data
    
    def put_iata_codes(self, data) -> bool:

        for row in data["prices"]:
            new_data = {
                "price": {
                    "iataCode": row["iataCode"]
                }
            }

            resp = requests.put(url=f"{SHEET_URL}/{row["id"]}", json=new_data, auth=(SHEETY_USERNAME, SHEETY_PWD))
            try:
                resp.raise_for_status()
            except HTTPError as err:
                if err.response.status_code == 404:
                    print('Page not found')
                elif err.response.status_code == 401:
                    print('Unauthorized access')
                else:
                    print(f'HTTP error occurred: {err}')