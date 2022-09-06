import requests
import os
import dotenv

dotenv.load_dotenv()


class Users:

    def __init__(self):
        self.SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT_USERS")
        self.is_equal = True
        self.email = ""

    def add_user(self):
        print("Welcome to Abhilash's Flight Club!")
        print("We find the best flight deals and email you...")
        first_name = input("What is your first name? \n")
        last_name = input("What is your last name? \n")
        while self.is_equal:
            self.email = input("What's your email? \n")
            email2 = input("Type your email again:: \n")
            if self.email != email2:
                print("Your email doesn't match. Try again...")
            else:
                self.is_equal = False

        body = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": self.email,
            }
        }
        response = requests.post(url=self.SHEETY_ENDPOINT, json=body)
        if response.status_code == 200:
            print("You're in the club! Looking forward for the best flight deal for you!!!")
