# This file will need to use the DataManager, FlightSearch, FlightData, NotificationManager
# classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import dotenv
import os

dotenv.load_dotenv()

API_KEY = os.getenv("REACT_APP_API_KEY")

data_manager_obj = DataManager(API_KEY)
flight_search_obj = FlightSearch(API_KEY)
notification_manager_obj = NotificationManager()

city_dict = data_manager_obj.post_iata_to_google_sheet()

for city, code_low_price in city_dict.items():
    flight_details = flight_search_obj.search_flight(code_low_price)
    if flight_details is not None:
        from_city = "London-STN"
        to_city = f"{city}-{code_low_price[0]}"
        print(to_city)
        from_date = flight_details[0][0]
        print(from_date)
        to_date = flight_details[0][1]
        print(to_date)
        price = flight_details[1][0]
        # notification_manager_obj.send_sms(from_city, to_city, from_date, to_date, price)

# new_user = Users()
# new_user.add_user()
