import smtplib
import random
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class OTP:
    def __init__(self):
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT"))
        self.GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
        self.PASSWORD = os.getenv("PASSWORD")
        # self.otp = 0

    def generate_otp(self):
        self.otp = random.randint(111111, 999999)
        return self.otp

    def send_otp(self, to_email):
        msg = EmailMessage()
        msg["Subject"] = "OTP Verification"
        msg["From"] = self.GMAIL_USERNAME
        msg["To"] = to_email
        msg.set_content(f"Your OTP Code: {self.otp}")

        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.GMAIL_USERNAME, self.PASSWORD)
            server.send_message(msg)
        
    def validate_otp(self, r_otp):
        return str(self.otp) == str(r_otp)