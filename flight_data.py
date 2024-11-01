class FlightData:
    def __init__(self, depart_code: str, dest_code: str, price: float, currency: str):
        self.departure_airport_code = depart_code
        self.destination_airport_code = dest_code
        self.price = price
        self.currency = currency