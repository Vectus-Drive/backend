from datetime import datetime
from .database import db


# ------------------- USERS -------------------
class User(db.Model):
    __tablename__ = "users"

    u_id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.String(20), nullable=False, default="customer"
    )  # admin, employee, customer

    # uselist=False makes sure that there will be only one to one relationship
    customer = db.relationship(
        "Customer", backref="user", uselist=False, cascade="all, delete"
    )
    employee = db.relationship(
        "Employee", backref="user", uselist=False, cascade="all, delete"
    )
    notifications = db.relationship(
           "Notification", backref="user", lazy=True, cascade="all, delete"
    )


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ------------------- CUSTOMERS -------------------
class Customer(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column(
        db.String(36), db.ForeignKey("users.u_id", ondelete="CASCADE"), primary_key=True
    )
    name = db.Column(db.String(100), nullable=False)
    nic = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(255))
    address = db.Column(db.String(255))
    telephone_no = db.Column(db.String(15))

    bookings = db.relationship(
        "Booking", backref="customer", lazy=True, cascade="all, delete"
    )
    transactions = db.relationship(
        "Transaction", backref="customer", lazy=True, cascade="all, delete"
    )
    reviews = db.relationship(
        "Review", backref="customer", lazy=True, cascade="all, delete"
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ------------------- EMPLOYEES -------------------
class Employee(db.Model):
    __tablename__ = "employees"

    employee_id = db.Column(
        db.String(36), db.ForeignKey("users.u_id", ondelete="CASCADE"), primary_key=True
    )
    name = db.Column(db.String(100), nullable=False)
    nic = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(255))
    address = db.Column(db.String(255))
    telephone_no = db.Column(db.String(15))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ------------------- CARS -------------------
class Car(db.Model):
    __tablename__ = "cars"

    car_id = db.Column(db.String(36), primary_key=True)
    license_no = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))
    seats = db.Column(db.Integer, nullable=False)
    fuel = db.Column(db.String(20), nullable=False, default="diesel")
    transmission = db.Column(db.String(20), nullable=False, default="automatic")
    features = db.Column(db.JSON)
    doors = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    price_per_day = db.Column(db.Float, nullable=False)
    availability_status = db.Column(db.Boolean, default=True)
    condition = db.Column(db.String(50), nullable=False)

    bookings = db.relationship(
        "Booking", backref="car", lazy=True, cascade="all, delete"
    )
    transactions = db.relationship(
        "Transaction", backref="car", lazy=True, cascade="all, delete"
    )
    services = db.relationship(
        "Service", backref="car", lazy=True, cascade="all, delete"
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ------------------- NOTIFICATIONS -------------------
class Notification(db.Model):
    __tablename__ = "notifications"

    notification_id = db.Column(db.String(36), primary_key=True)
    u_id = db.Column(
        db.String(36),
        db.ForeignKey("users.u_id", ondelete="CASCADE"),
        nullable=False,
    )
    text = db.Column(db.Text, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ------------------- BOOKINGS -------------------
class Booking(db.Model):
    __tablename__ = "bookings"

    booking_id = db.Column(db.String(36), primary_key=True)
    customer_id = db.Column(
        db.String(36),
        db.ForeignKey("customers.customer_id", ondelete="CASCADE"),
        nullable=False,
    )
    car_id = db.Column(
        db.String(36), db.ForeignKey("cars.car_id", ondelete="CASCADE"), nullable=False
    )
    booked_at = db.Column(db.DateTime, default=datetime.now)
    time_period = db.Column(db.Integer, nullable=False)
    returned_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default="pending")
    fine = db.Column(db.Float, default=0.0)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ------------------- SERVICES -------------------
class Service(db.Model):
    __tablename__ = "services"

    service_id = db.Column(db.String(36), primary_key=True)
    car_id = db.Column(
        db.String(36), db.ForeignKey("cars.car_id", ondelete="CASCADE"), nullable=False
    )
    transaction_amount = db.Column(db.Float, nullable=False)
    service_date = db.Column(db.DateTime, default=datetime.now)
    details = db.Column(db.Text, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ------------------- TRANSACTIONS -------------------
class Transaction(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(db.String(36), primary_key=True)
    transaction_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    customer_id = db.Column(
        db.String(36),
        db.ForeignKey("customers.customer_id", ondelete="CASCADE"),
        nullable=False,
    )
    car_id = db.Column(
        db.String(36), db.ForeignKey("cars.car_id", ondelete="CASCADE"), nullable=False
    )
    booking_id = db.Column(
        db.String(36),
        db.ForeignKey("bookings.booking_id", ondelete="SET NULL"),
        nullable=True,
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ------------------- REVIEWS -------------------
class Review(db.Model):
    __tablename__ = "reviews"

    review_id = db.Column(db.String(36), primary_key=True)
    customer_id = db.Column(
        db.String(36),
        db.ForeignKey("customers.customer_id", ondelete="CASCADE"),
        nullable=False,
    )
    stars = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ------------------- TOKEN BLOCK LIST -------------------
class Token(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    jti = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=True)
    expires = db.Column(db.DateTime, default=datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
