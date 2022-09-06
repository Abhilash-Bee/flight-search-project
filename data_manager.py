import requests
import json
import os
import dotenv

dotenv.load_dotenv()


class DataManager:

    def __init__(self, api_key):
        self.IATA_ENDPOINT = os.getenv("IATA_ENDPOINT")
        self.SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
        try:
            with open("sheety_complete_data.json") as sheety_file:
                self.city_data = json.load(sheety_file)
                self.fetch_data = False
        except FileNotFoundError:
            self.city_response = requests.get(url=self.SHEETY_ENDPOINT)
            self.city_data = self.city_response.json()
            self.fetch_data = True
            self.city_list = {city["city"]: city["lowestPrice"] for city in self.city_data["prices"]}

        self.city_dict = {}
        self.header = {
            "apikey": api_key
        }

    def post_iata_to_google_sheet(self):
        if self.fetch_data:
            count = 2
            for city, low_price in self.city_list.items():
                iata_config = {
                    "term": city,
                    "location_types": "city",
                }
                code_response = requests.get(url=self.IATA_ENDPOINT, params=iata_config, headers=self.header)
                code_data = code_response.json()
                code = code_data["locations"][0]["code"]
                body = {
                    "price": {
                        "iataCode": code,  # EACH CITY CODE
                    }
                }
                self.city_dict[city] = [code, low_price]
                sheety_response = requests.put(
                    url=f"{self.SHEETY_ENDPOINT}/{count}",
                    json=body
                )
                print(sheety_response.text)
                count += 1

            with open("sheety_complete_data.json", "w") as sheety_file:
                self.city_response = requests.get(url=self.SHEETY_ENDPOINT)
                self.city_data = self.city_response.json()
                json.dump(self.city_data, sheety_file, indent=4)

            return self.city_dict
        else:
            self.city_dict = {city["city"]: [city["iataCode"], city["lowestPrice"]]
                              for city in self.city_data["prices"]}
            return self.city_dict
