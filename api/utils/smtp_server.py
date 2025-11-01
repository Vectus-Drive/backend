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
    
    def clean_str(self, s):
        return s.encode('utf-8', 'ignore').decode('utf-8')

    def send_otp(self, to_email):
        msg = EmailMessage()
        msg['Subject'] = self.clean_str("OTP Verification")
        msg['From'] = self.clean_str(self.GMAIL_USERNAME)
        msg['To'] = self.clean_str(to_email)
        msg.set_content(f"Your OTP Code: {self.otp}", charset="utf-8")

        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.GMAIL_USERNAME, self.PASSWORD)
            server.send_message(msg)
        
    def validate_otp(self, r_otp):
        return str(self.otp) == str(r_otp)