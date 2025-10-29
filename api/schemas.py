from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Literal, Union, List, Dict, Any
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
    transaction_amount: float

class ServiceCreate(ServiceBase):
    car_id: str

class ServiceUpdate(ServiceBase):
    pass

class ServiceData(ServiceBase):
    service_id: str
    service_date: Optional[datetime] = None

class ServiceResponse(Response):
    data: ServiceData | List[ServiceData] | str | None


# # ------------------- TRANSACTION SCHEMAS -------------------
class TransactionBase(BaseModel):
    transaction_amount: Optional[float] = 0.0
    transaction_type: Literal["credit", "debit"] = "debit"
    
class TransactionCreate(TransactionBase):
    booking_id: str

class TransactionUpdate(TransactionBase):
    pass

class TransactionData(TransactionBase):
    transaction_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TransactionResponse(Response):
    data: TransactionData | List[TransactionData] | None | str

# ------------------- REVIEW SCHEMAS -------------------
class ReviewBase(BaseModel):
    stars: int
    topic: Optional[str] = None
    description: Optional[str] = None

class ReviewCreate(ReviewBase):
    customer_id: str

class ReviewUpdate(ReviewBase):
    pass

class ReviewData(ReviewBase):
    review_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ReviewResponse(Response):
    data: ReviewData | List[ReviewData] | None | str


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
    make: str
    model: str
    seats: int
    fuel: Literal["diesel", "petrol"] = "diesel"
    transmission: Literal["automatic", "manual"] = "automatic"
    doors: int
    description: str
    features: List[str]
    price_per_day: float
    availability_status: bool
    condition: str
    image: Optional[str] = None

class CarCreate(CarBase):
    pass

class CarData(CarBase):
    car_id: str
    services: ServiceData | List[ServiceData] | None

class CarCreateResponse(BaseModel):
    car_id: str
    license_no: str
    make: str
    model: str

class CarResponse(Response):
    data: CarCreateResponse | CarData | List[CarData] | None | str



# ------------------- BOOKING SCHEMAS -------------------
class BookingBase(BaseModel):
    time_period: int
    status: Literal["pending", "booked", "canceled"] = "pending"
    fine: Optional[float] = 0.0

class BookingCreate(BookingBase):
    customer_id: str
    car_id: str

class BookingUpdate(BookingBase):
    pass

class BookingData(BookingBase):
    booking_id: str

class BookingResponse(Response):
    data: BookingData | List[BookingData] | None | str

# ------------------- NOTIFICATION SCHEMAS -------------------
class NotificationBase(BaseModel):
    text: str

class NotificationCreate(NotificationBase):
    u_id: str

class NotificationUpdate(NotificationBase):
    pass

class NotificationData(BaseModel):
    notification_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class NotificationResponse(Response):
    data: NotificationData | List[NotificationData] | None | str
