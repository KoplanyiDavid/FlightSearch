from decouple import config

AMADEUS_API_KEY = config("AMADEUS_API_KEY")
AMADEUS_API_SECRET = config("AMADEUS_API_SECRET")
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

SHEETY_USERNAME = config("SHEETY_USERNAME")
SHEETY_PWD = config("SHEETY_PWD")

SHEET_URL = "https://api.sheety.co/1f64a373e866f672231eb62d7cf431a2/flightDeals/prices"

ORIGIN_LOCATION_CODE = "LON"