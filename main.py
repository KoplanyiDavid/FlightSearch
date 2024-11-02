import time
import datetime
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import FlightData
from constants import ORIGIN_LOCATION_CODE
from func_messaging import send_message

data_manager = DataManager()
flight_search = FlightSearch()
flight_data = []

data = data_manager.get_sheet_data()

for row in data["prices"]:
    if row['iataCode'] == "":
        row["iataCode"] = flight_search.get_iata_code(row["city"])
        time.sleep(2)

data_manager.put_iata_codes(data)

six_month_period = datetime.datetime.now() + datetime.timedelta(days=6*30)
departure_date = datetime.datetime.now() + datetime.timedelta(days=1)

for row in data["prices"]:
    print(f"Getting non-stop flights from {row["city"]}...")
    result_json_data = flight_search.get_flights(
                                                    origin_location_code=ORIGIN_LOCATION_CODE, 
                                                    destination_location_code=row["iataCode"], 
                                                    departure_date=departure_date.strftime("%Y-%m-%d"),
                                                    return_date=six_month_period.strftime("%Y-%m-%d"),
                                                    adults=1,
                                                    non_stop="true"
                                                )
    if result_json_data is None or not result_json_data["data"]:
        print(f"Getting flights from {row["city"]}...")
        result_json_data = flight_search.get_flights(
                                                        origin_location_code=ORIGIN_LOCATION_CODE, 
                                                        destination_location_code=row["iataCode"], 
                                                        departure_date=departure_date.strftime("%Y-%m-%d"),
                                                        return_date=six_month_period.strftime("%Y-%m-%d"),
                                                        adults=1,
                                                        non_stop="false"
                                                    )
        if result_json_data is None or not result_json_data["data"]:
            print("No data found")
        else:
            print(f"{row["city"]}: {result_json_data["data"][0]["price"]["total"]} {result_json_data["data"][0]["price"]["currency"]}")
            flight_data.append(FlightData(ORIGIN_LOCATION_CODE, row["iataCode"], float(result_json_data["data"][0]["price"]["total"]), result_json_data["data"][0]["price"]["currency"]))
    else:
        print(f"{row["city"]}: {result_json_data["data"][0]["price"]["total"]} {result_json_data["data"][0]["price"]["currency"]}")
        flight_data.append(FlightData(ORIGIN_LOCATION_CODE, row["iataCode"], float(result_json_data["data"][0]["price"]["total"]), result_json_data["data"][0]["price"]["currency"]))
    time.sleep(3)

if flight_data != []:
    cheapest_flight: FlightData = flight_data[0]
    min_index = 0
    index = 0

    for data in flight_data:
        if data.price < cheapest_flight.price:
            min_price = FlightData(data).price
            min_index = index
        index += 1

    send_message(f"Cheapest flight: {cheapest_flight.destination_airport_code} for {cheapest_flight.price} {cheapest_flight.currency}")

else:
    send_message("Flight not found")
