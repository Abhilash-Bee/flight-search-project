from twilio.rest import Client
import os
import dotenv

dotenv.load_dotenv()


class NotificationManager:

    def __init__(self):
        self.ACC_SID = os.getenv("ACC_SID")
        self.AUTH_TOKEN = os.getenv("AUTH_TOKEN")
        self.MY_TWILIO_NO = os.getenv("MY_TWILIO_NO")
        self.MY_NO = os.getenv("MY_NO")

    def send_sms(self, from_city, to_city, from_date, to_date, price):
        client = Client(self.ACC_SID, self.AUTH_TOKEN)
        message = client.messages.create(
            body=f"Low price alert! only £{price} to fly from {from_city}"
                 f" to {to_city}, from {from_date} to {to_date}",
            from_=self.MY_TWILIO_NO,
            to=self.MY_NO,
        )
        print(message.status)
        print("Sent successfully")
