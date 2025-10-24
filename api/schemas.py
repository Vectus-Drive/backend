from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from enum import Enum

class Role(Enum):
    CUSTOMER = "CUSTOMER"
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"
    
class Transaction(Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT" 

# ------------------- USER SCHEMAS -------------------
class UserBase(BaseModel):

    model_config = ConfigDict(from_attributes=True) 

    name: str
    username: str
    nic: str
    email: EmailStr
    address: Optional[str]
    telephone_no: Optional[str]
    role: Literal["customer", "employee"] = "customer"

class UserCreate(UserBase):
    password: str
    image: Optional[str]

class UserResponse(UserBase):
    user_id: str

# # ------------------- USER SCHEMAS -------------------
# class UserBase(BaseModel):
#     username: str
#     role: Optional[str] = "customer"


# class UserCreate(UserBase):
#     password: str
#     pass

# class UserResponse(UserBase):
#     u_id: str
#     class Config:
#         form_attributes = True


# ------------------- CUSTOMER SCHEMAS -------------------
class CustomerBase(BaseModel):
    name: str
    nic: str
    email: EmailStr
    image: Optional[str] = None
    address: Optional[str] = None
    telephone_no: Optional[str] = None

class CustomerCreate(CustomerBase):
    image: Optional[str]
    pass

class CustomerResponse(CustomerBase):
    customer_id: str

# ------------------- EMPLOYEE SCHEMAS -------------------
class EmployeeBase(BaseModel):
    name: str
    nic: str
    email: EmailStr
    image: Optional[str] = None
    address: Optional[str] = None
    telephone_no: Optional[str] = None

class EmployeeCreate(CustomerBase):
    image: Optional[str]
    pass

class EmployeeResponse(CustomerBase):
    customer_id: str


# # ------------------- CAR SCHEMAS -------------------
class CarBase(BaseModel):
    license_no: str
    name: str
    type: str
    seats: int
    fuel: str
    transmission: str
    doors: int
    description: Optional[str] = None
    features: Optional[int] = None
    price_per_day: float
    availability_status: Optional[str] = "Available"
    condition: str
    image: Optional[str] = None
    last_service_date: Optional[datetime] = None


class CarCreate(CarBase):
    pass


class CarResponse(CarBase):
    car_id: str

# ------------------- BOOKING SCHEMAS -------------------
class BookingBase(BaseModel):
    customer_id: int
    car_id: int
    time_period: int
    fine: Optional[float] = 0.0


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    booking_id: int
    booked_at: datetime
    returned_at: Optional[datetime] = None

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
#         form_attributes = True


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
#         form_attributes = True


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
#         form_attributes = True


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
#         form_attributes = True
