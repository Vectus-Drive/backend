from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ------------------- USER SCHEMAS -------------------
class UserBase(BaseModel):
    u_id: str
    username: str
    password: str
    role: Optional[str] = "customer"


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    class Config:
        orm_mode = True


# ------------------- CUSTOMER SCHEMAS -------------------
class CustomerBase(BaseModel):
    customer_id: str
    name: str
    nic: str
    email: EmailStr
    image: Optional[str] = None
    address: Optional[str] = None
    telephone_no: Optional[str] = None
    user_id: Optional[int] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    class Config:
        orm_mode = True


# # ------------------- CAR SCHEMAS -------------------
# class CarBase(BaseModel):
#     license_no: str
#     name: str
#     type: str
#     seats: int
#     fuel: str
#     transmission: str
#     doors: int
#     description: Optional[str] = None
#     features: Optional[int] = None
#     price_per_day: float
#     availability_status: Optional[str] = "Available"
#     condition: str
#     image: Optional[str] = None
#     last_service_date: Optional[datetime] = None


# class CarCreate(CarBase):
#     pass


# class CarResponse(CarBase):
#     car_id: int

#     class Config:
#         orm_mode = True


# # ------------------- BOOKING SCHEMAS -------------------
# class BookingBase(BaseModel):
#     customer_id: int
#     car_id: int
#     time_period: int
#     fine: Optional[float] = 0.0


# class BookingCreate(BookingBase):
#     pass


# class BookingResponse(BookingBase):
#     booking_id: int
#     booked_at: datetime
#     returned_at: Optional[datetime] = None

#     class Config:
#         orm_mode = True


# # ------------------- SERVICE SCHEMAS -------------------
# class ServiceBase(BaseModel):
#     car_id: int
#     details: str


# class ServiceCreate(ServiceBase):
#     pass


# class ServiceResponse(ServiceBase):
#     service_id: int
#     service_date: datetime

#     class Config:
#         orm_mode = True


# # ------------------- TRANSACTION SCHEMAS -------------------
# class TransactionBase(BaseModel):
#     transaction_type: str  # "credit" or "debit"
#     customer_id: int
#     car_id: int
#     booking_id: Optional[int] = None


# class TransactionCreate(TransactionBase):
#     pass


# class TransactionResponse(TransactionBase):
#     transaction_id: int
#     date: datetime

#     class Config:
#         orm_mode = True


# # ------------------- REVIEW SCHEMAS -------------------
# class ReviewBase(BaseModel):
#     customer_id: int
#     car_id: int
#     stars: int
#     topic: Optional[str] = None
#     description: Optional[str] = None


# class ReviewCreate(ReviewBase):
#     pass


# class ReviewResponse(ReviewBase):
#     review_id: int
#     created_at: datetime

#     class Config:
#         orm_mode = True


# # ------------------- TOKEN SCHEMAS -------------------
# class TokenBase(BaseModel):
#     jti: str
#     user_id: int
#     expires: datetime


# class TokenCreate(TokenBase):
#     pass


# class TokenResponse(TokenBase):
#     id: int
#     revoked_at: Optional[datetime]

#     class Config:
#         orm_mode = True
