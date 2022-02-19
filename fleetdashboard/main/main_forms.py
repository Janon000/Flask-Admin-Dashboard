from wtforms import (
    StringField,
    PasswordField,
    IntegerField,
    HiddenField
)
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp, Optional
from wtforms import ValidationError, SubmitField
from fleetdashboard.models import User

class vehicle_form(FlaskForm):
    T_Number = StringField(validators=[Length(1, 14), InputRequired()])
    white_plate = StringField(validators=[Length(0, 64)])
    green_plate = StringField(validators=[Length(0, 64)])
    department = StringField(validators=[Length(0, 64)])
    ownership_type = StringField(validators=[Length(0, 64)])
    owner_name = StringField(validators=[Length(0, 64)])
    driver_name = StringField(validators=[Length(0, 64)])
    region = StringField(validators=[Length(0, 64)])
    amber = StringField(validators=[Length(0, 10)])
    flow_sticker = StringField(validators=[Length(0, 10)])
    telicon_sticker = StringField(validators=[Length(0, 10)])
    lpg_gas = StringField(validators=[Length(0, 10)])
    manufacturer = StringField(validators=[Length(0, 25)])
    car_model = StringField(validators=[Length(0, 64)])
    year = StringField(validators=[Length(0, 6)])
    color = StringField(validators=[Length(0, 10)])
    chasis_number = StringField(validators=[Length(0, 25)])
    engine_number = StringField(validators=[Length(0, 25)])
    odometer = IntegerField(validators=[Optional()])
    service_date = DateField(validators=[Optional()])
    registration_exp = DateField(validators=[Optional()])
    fitness_exp = DateField(validators=[Optional()])
    carrier_exp = DateField(validators=[Optional()])
    cn_exp = DateField(validators=[Optional()])
    insurance_exp = DateField(validators=[Optional()])
    insurance_company = StringField(validators=[Length(0, 64)])
    gas_type = StringField(validators=[Length(0, 25)])


class status_form(FlaskForm):
    T_Number = StringField(validators=[Length(1, 14), InputRequired()], render_kw={'readonly': True})
    status = StringField(validators=[InputRequired(), Length(0, 64)], render_kw={'readonly': True})
    # Garage
    date_garage = DateField(validators=[InputRequired()], format='%Y-%m-%d')
    garage_reason = StringField(validators=[Length(0, 250)])
    repair_id = StringField(validators=[Length(0, 64)])
    estimated_repair_time = StringField(validators=[Length(0, 64)])
    # Parked
    date_parked = DateField(validators=[InputRequired()])
    park_reason = StringField(validators=[Length(0, 250)])
    # Active
    date_active = DateField(validators=[Optional()])
    active_notes = StringField(validators=[Length(0, 250)])
    page_name = HiddenField()


class service_form(FlaskForm):
    T_Number = StringField(validators=[Length(1, 14), InputRequired()], render_kw={'readonly': True})
    odometer = IntegerField()
    service_date = DateField()


class expense_form(FlaskForm):
    id = HiddenField()
    repair_id = HiddenField()
    expense_status = StringField(validators=[Length(0, 10)])
    cost_description = StringField(validators=[Length(0, 100)])
    cost = IntegerField()


class hidden_form(FlaskForm):
    t_num = HiddenField()