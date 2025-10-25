from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Literal, Union, List
from datetime import datetime
from enum import Enum


# ------------------- RESPONSE SCHEMAS -------------------
class Response(BaseModel):
    status: Literal["error", "success"]
    message: str


# ------------------- USER SCHEMAS -------------------
class UserBase(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    name: str
    username: str
    nic: str
    email: EmailStr
    address: str
    telephone_no: str
    role: Literal["customer", "employee"] = "customer"


class UserCreate(UserBase):
    password: str
    image: Optional[str] = None


class UserData(BaseModel):
    u_id: str
    username: str
    role: Literal["customer", "employee"] = "customer"


class UserResponse(Response):
    data: UserData | None


# ------------------- CUSTOMER SCHEMAS -------------------
class CustomerBase(BaseModel):
    name: str
    nic: str
    email: EmailStr
    image: Optional[str]
    address: Optional[str] = None
    telephone_no: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerData(CustomerBase):
    user: UserData


class CustomerResponse(Response):
    data: CustomerData | List[CustomerData] | None | str


# ------------------- EMPLOYEE SCHEMAS -------------------
class EmployeeBase(BaseModel):
    name: str
    nic: str
    email: EmailStr
    image: Optional[str]
    address: Optional[str] = None
    telephone_no: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeData(EmployeeBase):
    user: UserData


class EmployeeResponse(Response):
    data: EmployeeData | List[EmployeeData] | None | str


# # ------------------- SERVICE SCHEMAS -------------------
class ServiceBase(BaseModel):
    details: str

class ServiceCreate(ServiceBase):
    car_id: str

class ServiceUpdate(ServiceBase):
    pass

class ServiceData(ServiceBase):
    service_id: str

class ServiceResponse(Response):
    data: ServiceData | List[ServiceData] | str | None


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
