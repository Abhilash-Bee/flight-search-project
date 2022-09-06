from datetime import datetime
import requests
import os
import dotenv

dotenv.load_dotenv()

DATE = int(datetime.now().strftime("%d")) + 1
MONTH = int(datetime.now().strftime("%m"))
YEAR = int(datetime.now().strftime("%Y"))


class FlightSearch:

    def __init__(self, api_key):
        self.FLIGHT_SEARCH_API = os.getenv("FLIGHT_SEARCH_API")
        self.START_DATE = f"{DATE}/{MONTH}/{YEAR}"
        self.END_DATE = f"{DATE}/{MONTH + 6}/{YEAR}"
        self.dept_from_to = []
        check_month = (MONTH + 6) % 12
        if check_month > 0:
            nxt_year = YEAR + 1
            self.END_DATE = f"{DATE}/{check_month}/{nxt_year}"
        self.header = {
            "apikey": api_key
        }
        self.min_price_route = None

    def search_flight(self, code_low_price):
        flight_search_config_stop_0 = {
            "fly_from": "STN",
            "fly_to": code_low_price[0],
            "date_from": self.START_DATE,
            "date_to": self.END_DATE,
            "price_to": code_low_price[1],
            "vehicle_type": "aircraft",
            "max_stopovers": 0
        }
        flight_search_config_stop_1 = {
            "fly_from": "STN",
            "fly_to": code_low_price[0],
            "date_from": self.START_DATE,
            "date_to": self.END_DATE,
            "price_to": code_low_price[1],
            "vehicle_type": "aircraft",
            "max_stopovers": 1
        }
        min_price = code_low_price[1]
        response = requests.get(url=self.FLIGHT_SEARCH_API, params=flight_search_config_stop_0, headers=self.header)
        data = response.json()
        if len(data["data"]) == 0:
            response = requests.get(url=self.FLIGHT_SEARCH_API, params=flight_search_config_stop_1, headers=self.header)
            data = response.json()

        # print(len(data["data"]))
        for every_date in data["data"]:
            if every_date["price"] < min_price:
                min_price = every_date["price"]

        departures = []
        for every_date in data["data"]:
            if min_price == every_date["price"]:
                departures += every_date["route"]

        length = len(departures)
        # print(length)
        if length == 1:
            self.dept_from_to = [departures[0]["local_departure"][:10], departures[0]["local_departure"][:10]]
        elif len(departures) >= 2:
            year = int(departures[0]["local_departure"][0:4]) - int(departures[length - 1]["local_departure"][0:4])
            month = int(departures[0]["local_departure"][5:7]) - int(departures[length - 1]["local_departure"][5:7])
            if month <= 0 and year <= 0:
                self.dept_from_to = [departures[0]["local_departure"][:10],
                                     departures[length - 1]["local_departure"][:10]]
            else:
                self.dept_from_to = [departures[length - 1]["local_departure"][:10],
                                     departures[0]["local_departure"][:10]]
        else:
            return None

        return [self.dept_from_to, [min_price]]
