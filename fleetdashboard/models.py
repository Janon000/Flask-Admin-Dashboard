from fleetdashboard import db
from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from select import select
from datetime import date, datetime


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.email


class Vehicle(db.Model):
    __tablename__ = "vehicle"

    T_Number = db.Column(db.String(10), primary_key=True, index=True, nullable=False)
    white_plate = db.Column(db.String(10))
    green_plate = db.Column(db.String(10))
    department = db.Column(db.String(64))
    ownership_type = db.Column(db.String(64))
    owner_name = db.Column(db.String(64))
    driver_name = db.Column(db.String(64))
    region = db.Column(db.String(64))
    amber = db.Column(db.String(10))
    flow_sticker = db.Column(db.String(10))
    telicon_sticker = db.Column(db.String(10))
    lpg_gas = db.Column(db.String(10))
    manufacturer = db.Column(db.String(25))
    car_model = db.Column(db.String(25))
    year = db.Column(db.String(64))
    color = db.Column(db.String(64))
    chasis_number = db.Column(db.String(64))
    engine_number = db.Column(db.String(64))
    odometer = db.Column(db.Integer)
    service_date = db.Column(db.Date)
    registration_exp = db.Column(db.Date)
    fitness_exp = db.Column(db.Date)
    carrier_exp = db.Column(db.Date)
    cn_exp = db.Column(db.Date)
    insurance_exp = db.Column(db.Date)
    insurance_company = db.Column(db.String(64))
    gas_type = db.Column(db.String(64))
    status = db.relationship('Status', backref='details', lazy=True)

    @classmethod
    def registration_stat(cls, date_field):
        if date_field is not None:
            if (date_field - date.today()).days < 0:
                return "Expired"
            elif (date_field - date.today()).days < 14:
                return "Soon"
            else:
                return "Good"

    @property
    def fitness_stat(self):
        if self.fitness_exp is not None:
            if (self.fitness_exp - date.today()).days < 0:
                return "Expired"
            elif (self.fitness_exp - date.today()).days < 14:
                return "Soon"
            else:
                return "Good"

    def to_dict(self):
        return {
            'T_Number': self.T_Number,
            'white_plate': self.white_plate,
            'green_plate': self.green_plate,
            'department': self.department,
            'ownership_type': self.ownership_type,
            'owner_name': self.owner_name,
            'driver_name': self.driver_name,
            'region': self.region,
            'amber': self.amber,
            'flow_sticker': self.flow_sticker,
            'telicon_sticker': self.telicon_sticker,
            'lpg_gas': self.lpg_gas,
            'manufacturer': self.manufacturer,
            'car_model': self.car_model,
            'year': self.year,
            'color': self.color,
            'chasis_number': self.chasis_number,
            'engine_number': self.engine_number,
            'odometer': self.odometer,
            'service_date': self.service_date,
            'registration_exp': self.registration_exp,
            'fitness_exp': self.fitness_exp,
            'carrier_exp': self.carrier_exp,
            'cn_exp': self.cn_exp,
            'insurance_exp': self.insurance_exp,
            'insurance_company': self.insurance_company,
            'gas_type': self.gas_type,
            'fitness_stat': self.fitness_stat
        }

    def __repr__(self):
        return '<Vehicle %r>' % self.T_Number


class Status(db.Model):
    __tablename__ = "status"

    T_Number = db.Column(db.String(10), db.ForeignKey('vehicle.T_Number'), primary_key=True, nullable=False)
    status = db.Column(db.String(64), index=True, nullable=False)
    # Garage
    date_garage = db.Column(db.Date)
    garage_reason = db.Column(db.Text)
    repair_id = db.Column(db.String(24))
    estimated_repair_time = db.Column(db.Date)
    # Parked
    date_parked = db.Column(db.Date)
    park_reason = db.Column(db.Text)
    # Active
    date_active = db.Column(db.Date)
    active_notes = db.Column(db.Text)
    estimated_repair_cost = db.relationship('Expense', backref='repair', lazy=True)

    @hybrid_property
    def repair_expense_sum(self):
        return sum(expense.cost for expense in self.estimated_repair_cost)

    @repair_expense_sum.expression
    def repair_expense_sum(cls):
        return (
            select([func.sum(Expense.cost)]).
                where(Expense.repair_id == cls.repair_id).
                label('repair_expense_sum')
        )

    def to_dict(self):
        return {
            'T_Number': self.T_Number,
            'status': self.status,
            'date_garage': self.date_garage,
            'garage_reason': self.garage_reason,
            'repair_id': self.repair_id,
            'estimated_repair_time': self.estimated_repair_time,
            'date_parked': self.date_parked,
            'park_reason': self.park_reason,
            'date_active': self.date_active,
            'active_notes': self.active_notes,
            'repair_expense_sum': self.repair_expense_sum,
        }

    def __repr__(self):
        return F"Vehicle Status {self.status},{self.T_Number}"


class Service(db.Model):
    __tablename__ = "service"

    T_Number = db.Column(db.String(10), db.ForeignKey('vehicle.T_Number'), nullable=False, primary_key=True)
    odometer = db.Column(db.Integer)
    service_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Last Service Date %r>' % self.service_date


class Expense(db.Model):
    __tablename__ = "expense"
    id = db.Column(db.Integer, primary_key=True)
    T_number = db.Column(db.String(10), nullable=True)
    repair_id = db.Column(db.String(10), db.ForeignKey('status.repair_id'), nullable=False)
    expense_status = db.Column(db.String(5), nullable=False)
    cost_description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date)
    month = db.Column(db.String(10))
    year = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'T_Number': self.T_number,
            'repair_id': self.repair_id,
            'expense_status': self.expense_status,
            'cost_description': self.cost_description,
            'cost': self.cost,
            'date': self.date,
            'month': self.month,
            'year': self.year,
        }


class Notification(db.Model):
    __tablename__ = "notification"

    T_Number = db.Column(db.String(10), db.ForeignKey('vehicle.T_Number'), nullable=False, primary_key=True)
    service_date = db.Column(db.Date)
    registration_exp = db.Column(db.Date)
    fitness_exp = db.Column(db.Date)
    carrier_exp = db.Column(db.Date)
    cn_exp = db.Column(db.Date)
    insurance_exp = db.Column(db.Date)

    @classmethod
    def date_stat(cls, date_field):
        if date_field is not None:
            if (date_field - date.today()).days < 0:
                return "Expired"
            elif (date_field - date.today()).days < 14:
                return "Soon"
            else:
                return "Good"

    def to_dict(self):
        return {
            'T_Number': self.T_Number,
            'service_date': self.service_date,
            'registration_exp': self.registration_exp,
            'fitness_exp': self.fitness_exp,
            'carrier_exp': self.carrier_exp,
            'cn_exp': self.cn_exp,
            'fitness_stat': self.date_stat
        }

    def to_date_list(self):
        return [('Service Date', self.service_date),
                ('Registration', self.registration_exp),
                ('Fitness', self.fitness_exp),
                ('Carrier', self.carrier_exp),
                ('Cover Note', self.cn_exp),
                ('Insurance', self.insurance_exp)]

    def __repr__(self):
        return '<Vehicle %r>' % self.T_Number


class NotifList(db.Model):
    __tablename__ = "notiflist"

    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)
    read = db.Column(db.String(5))


class History(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)
    T_Number = db.Column(db.String(10), db.ForeignKey('vehicle.T_Number'), nullable=False)
    status = db.Column(db.String(64), index=True, nullable=False)
    # Garage
    date_garage = db.Column(db.Date)
    garage_reason = db.Column(db.Text)
    repair_id = db.Column(db.String(24))
    estimated_repair_time = db.Column(db.Date)
    # Parked
    date_parked = db.Column(db.Date)
    park_reason = db.Column(db.Text)
    # Active
    date_active = db.Column(db.Date)
    active_notes = db.Column(db.Text)


