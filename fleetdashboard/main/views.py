from fleetdashboard import db
from . import main
from fleetdashboard.models import Vehicle, Status, Expense, Notification, NotifList, History

from flask import (
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request,
    jsonify,
    current_app
)

from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required,
)

from datetime import timedelta, date, datetime
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)

from .main_forms import vehicle_form, status_form, expense_form, hidden_form
import json
import uuid
from sqlalchemy import func


@main.route("/", methods=("GET", "POST"), strict_slashes=False)
def dashboard():
    if current_user.is_authenticated:
        # Data cards
        total_count = db.session.query(Status.status).count()
        total_count2 = db.session.query(func.count(Status.status))

        # Active Card info
        active_count = Status.query.filter_by(status="ACTIVE").count()
        telicon_active_count = len(db.session.query(Status).join(Vehicle).filter(Vehicle.ownership_type == "TELiCON") \
                                   .filter(Status.status == "ACTIVE").all())
        own_third_active = active_count - telicon_active_count

        # Garage Card info
        garage_count = Status.query.filter_by(status="GARAGE").count()
        telicon_garage_count = len(db.session.query(Status).join(Vehicle).filter(Vehicle.ownership_type == "TELiCON") \
                                   .filter(Status.status == "GARAGE").all())
        own_third_garage = garage_count - telicon_garage_count

        # Parked Card info
        parked_count = Status.query.filter_by(status="PARKED").count()
        telicon_parked_count = len(db.session.query(Status).join(Vehicle).filter(Vehicle.ownership_type == "TELiCON") \
                                   .filter(Status.status == "PARKED").all())
        own_third_parked = parked_count - telicon_parked_count

        own_count = db.session.query(Status).join(Vehicle).filter(Vehicle.ownership_type == "Own Vehicle").all()
        third_count = db.session.query(Status).join(Vehicle).filter(Vehicle.ownership_type == "3rd Party").all()

        # Chart
        expense_by_month = db.session.query(db.func.sum(Expense.cost), Expense.month).group_by(Expense.month).order_by(
            Expense.month).all()
        expense_by_year = db.session.query(db.func.sum(Expense.cost), Expense.year).group_by(Expense.year).order_by(
            Expense.year).all()
        expense_over_time = []
        label_over_time = []
        for amount, month in expense_by_month:
            expense_over_time.append(amount)
            label_over_time.append(month)

        return render_template("main/dashboard.html", title="Home", expense_over_time=json.dumps(expense_over_time),
                               label_over_time=json.dumps(label_over_time),
                               active_count=active_count,
                               garage_count=garage_count,
                               parked_count=parked_count,
                               telicon_active_count=telicon_active_count,
                               own_third_active=own_third_active,
                               telicon_garage_count=telicon_garage_count,
                               own_third_garage=own_third_garage,
                               telicon_parked_count=telicon_parked_count,
                               own_third_parked=own_third_parked,
                               )
    else:
        return redirect(url_for('auth.login'))


@main.route("/details", methods=("GET", "POST"), strict_slashes=False)
@login_required
def details():
    vehicles = Vehicle.query
    form = vehicle_form()
    today = date.today()
    # Add new vehicles to the database
    if request.method == 'POST':
        print(request.form)
        try:
            new_vehicle = Vehicle(T_Number=request.form['T_Number'], white_plate=request.form['white_plate'],
                                  green_plate=request.form['green_plate'],
                                  department=request.form['department'],
                                  ownership_type=request.form['ownership_type'],
                                  owner_name=request.form['owner_name'],
                                  driver_name=request.form['driver_name'],
                                  region=request.form['region'],
                                  amber=request.form['amber'],
                                  flow_sticker=request.form['flow_sticker'],
                                  telicon_sticker=request.form['telicon_sticker'],
                                  lpg_gas=request.form['lpg_gas'],
                                  manufacturer=request.form['manufacturer'],
                                  car_model=request.form['car_model'],
                                  year=request.form['year'],
                                  color=request.form['color'],
                                  chasis_number=request.form['chasis_number'],
                                  engine_number=request.form['engine_number'],
                                  service_date=datetime.strptime(request.form['service_date'], "%Y-%m-%d").date(),
                                  registration_exp=datetime.strptime(request.form['registration_exp'],
                                                                     "%Y-%m-%d").date(),
                                  fitness_exp=datetime.strptime(request.form['fitness_exp'], "%Y-%m-%d").date(),
                                  carrier_exp=datetime.strptime(request.form['carrier_exp'], "%Y-%m-%d").date(),
                                  cn_exp=datetime.strptime(request.form['cn_exp'], "%Y-%m-%d").date(),
                                  insurance_exp=datetime.strptime(request.form['insurance_exp'], "%Y-%m-%d").date(),
                                  insurance_company=request.form['insurance_company'],
                                  gas_type=request.form['gas_type']
                                  )
            db.session.add(new_vehicle)
            db.session.commit()
            print('new vehicle added')

            new_status = Status(T_Number=request.form['T_Number'],
                                status="ACTIVE",
                                date_garage=None,
                                garage_reason=None,
                                repair_id=str(uuid.uuid4()),
                                estimated_repair_time=None,
                                date_parked=None,
                                park_reason=None,
                                date_active=today,
                                active_notes=None)
            db.session.add(new_status)
            db.session.commit()
            print('New status added')

        except Exception as e:
            print(e)

        return redirect(url_for('main.details'))

    return render_template("main/details.html", vehicles=vehicles, form=form, today=today)


@main.route('/details/data')
@login_required
def details_data():
    # server side datatable
    query = Vehicle.query

    # search filter
    search = request.args.get('search[value]')

    if search:
        query = query.filter(db.or_(
            Vehicle.T_Number.like(f'%{search}%'),
            Vehicle.driver_name.like(f'%{search}%')
        ))

    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['T_Number', 'department', 'region', 'driver_name', 'ownership_type', 'registration_exp',
                            'fitness_exp', 'carrier_exp', 'insurance_exp']:
            col_name = 'T_Number'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Vehicle, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    return {'data': [vehicle.to_dict() for vehicle in query],
            'recordsFiltered': total_filtered,
            'recordsTotal': Vehicle.query.count(),
            'draw': request.args.get('draw', type=int),
            }


@main.route("/update/<T_Number>", methods=("GET", "POST"), strict_slashes=False)
@login_required
def update_details(T_Number):
    # query vehicle details and populate page
    vehicle = Vehicle.query.filter_by(T_Number=T_Number).first()
    form = vehicle_form(obj=vehicle)
    print(form.year)

    if form.validate_on_submit():
        print("success")
        try:
            form.populate_obj(vehicle)
            db.session.commit()
            return redirect(url_for('main.details'))

        except Exception as e:
            flash(e, "danger")

    return render_template("main/update.html",
                           T_Number=T_Number,
                           form=form
                           )


@main.route("/active", methods=("GET", "POST"), strict_slashes=False)
@login_required
def active():
    # Query the list of vehicles in the garage
    active_vehicles = Status.query.filter_by(status="ACTIVE")

    # Initialize the forms needed for updating status and expense
    active_status = status_form()
    hidden = hidden_form()

    # if update form is submitted
    if request.method == 'POST':
        print("success")
        status = Status.query.filter_by(T_Number=request.form['T_Number']).first()
        active_status = status_form(obj=request.form)
        print(request.form)
        try:
            status.status = active_status.status.data
            status.active_notes = active_status.active_notes.data
            status.date_active = active_status.date_active.data
            if request.form.get('page_name', False):
                status.repair_id = str(uuid.uuid4())
            else:
                status.repair_id = active_status.repair_id.data
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(e, "danger")
    else:
        print('lol')

    return render_template("main/active.html", vehicles=active_vehicles, hidden=hidden, form=active_status,
                           page_name='ACTIVE')


@main.route('/active/data')
@login_required
def active_data():
    query = Status.query.filter_by(status="ACTIVE")
    return {'data': [status.to_dict() for status in query]}


@main.route("/parked", methods=("GET", "POST"), strict_slashes=False)
@login_required
def parked():
    # Query the list of vehicles in the garage
    parked_vehicles = Status.query.filter_by(status="PARKED")

    # Initialize the forms needed for updating status and expense
    parked_status = status_form()

    # if update form is submitted
    if request.method == 'POST':
        status = Status.query.filter_by(T_Number=request.form['T_Number']).first()
        parked_status = status_form(obj=request.form)
        print(request.form)
        try:
            status.status = parked_status.status.data
            status.park_reason = parked_status.park_reason.data
            status.date_parked = parked_status.date_parked.data
            if request.form.get('page_name', False):
                status.repair_id = str(uuid.uuid4())
            else:
                status.repair_id = parked_status.repair_id.data

            # Add change to history table
            new_history = History(T_Number=request.form['T_Number'],
                                  status=parked_status.status.data,
                                  date_garage=None,
                                  garage_reason=None,
                                  repair_id=status.repair_id,
                                  estimated_repair_time=None,
                                  date_parked=parked_status.date_parked.data,
                                  park_reason=parked_status.park_reason.data,
                                  date_active=None,
                                  active_notes=None)
            db.session.add(new_history)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(e, "danger")
            print(e)
    else:
        print('lol')

    return render_template("main/park.html", vehicles=parked_vehicles, form=parked_status, page_name='PARKED')


@main.route('/parked/data')
@login_required
def parked_data():
    query = Status.query.filter_by(status="PARKED")
    return {'data': [status.to_dict() for status in query]}


@main.route("/garage", methods=("GET", "POST"), strict_slashes=False)
@login_required
def garage():
    # Query the list of vehicles in the garage
    garage_vehicles = Status.query.filter_by(status="GARAGE")

    # Initialize the forms needed for updating status and expense
    garage_status = status_form()

    # if form is submitted
    if request.method == 'POST':
        status = Status.query.filter_by(T_Number=request.form['T_Number']).first()
        garage_status = status_form(obj=request.form)
        print(request.form)
        try:
            # Update status table
            status.status = garage_status.status.data
            status.garage_reason = garage_status.garage_reason.data
            status.date_garage = garage_status.date_garage.data
            if request.form.get('page_name', False):
                status.repair_id = str(uuid.uuid4())
            else:
                status.repair_id = garage_status.repair_id.data

            # Add change to history table
            new_history = History(T_Number=request.form['T_Number'],
                                  status=garage_status.status.data,
                                  date_garage=garage_status.date_garage.data,
                                  garage_reason=garage_status.garage_reason.data,
                                  repair_id=status.repair_id,
                                  estimated_repair_time=None,
                                  date_parked=None,
                                  park_reason=None,
                                  date_active=None,
                                  active_notes=None)
            db.session.add(new_history)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(e, "danger")
    else:
        print('lol')

    return render_template("main/garage.html", vehicles=garage_vehicles, form=garage_status, page_name='GARAGE')


@main.route('/garage/data')
@login_required
def garage_data():
    query = Status.query.filter_by(status="GARAGE")
    return {'data': [status.to_dict() for status in query]}


@main.route("/process_status", methods=("GET", "POST"), strict_slashes=False)
@login_required
def process_status():
    if request.method == 'POST':
        # Get T Number of vehicle
        t_num = request.form['t_num']
        # Get current status information for vehicle
        status = Status.query.filter_by(T_Number=t_num).first()

        # Check if this is a new record
        if request.form.get('new_record', False):
            form = status_form()
            form.T_Number.data = t_num
            form.status.data = request.form['page_name']
            form.page_name.data = 'True'
            expense = ""
        else:
            # Pre-populate status form to be submitted
            form = status_form(obj=status)
            expense = "${:,.2f}".format(status.repair_expense_sum)

        if request.form['page_name'] == 'GARAGE':
            return jsonify({'htmlresponse': render_template('main/garage_response.html', form=form, expense=expense)})
        if request.form['page_name'] == 'ACTIVE':
            return jsonify({'htmlresponse': render_template('main/active_update.html', form=form, expense=expense)})
        if request.form['page_name'] == 'PARKED':
            return jsonify({'htmlresponse': render_template('main/parked_update.html', form=form, expense=expense)})


@main.route("/process_history", methods=("GET", "POST"), strict_slashes=False)
@login_required
def process_history():
    if request.method == 'POST':
        # Get T Number and type of history
        t_num = request.form['t_num']
        status_type = request.form['page_name']
        # Get history for vehicle
        hist = db.session.query(History).filter(History.T_Number == t_num).filter(History.status == status_type)
        return jsonify({'htmlresponse': render_template('main/history.html', history=hist, T_Number=t_num)})


@main.route("/expenses", methods=("GET", "POST"), strict_slashes=False)
@login_required
def expenses():
    expense_table = Expense.query

    return render_template("main/expenses.html", expenses=expense_table,
                           )


@main.route('/expense/data')
@login_required
def expense_data():
    return {'data': [expense.to_dict() for expense in Expense.query]}


@main.route("/get_expense", methods=("GET", "POST"), strict_slashes=False)
@login_required
def get_expense():
    if request.method == 'POST':
        print(request.form['repair_id'])
        repair_id = request.form['repair_id']
        t_num = request.form['t_num']
        costs_query = Expense.query.filter_by(repair_id=repair_id)
        cost_list = []
        for cost in costs_query:
            cost_list.append(expense_form(obj=cost))

    return jsonify(
        {'htmlresponse': render_template('main/expense_response.html', cost_list=costs_query, repair_id=repair_id,
                                         t_num=t_num)})


@main.route("/add_expense", methods=("GET", "POST"), strict_slashes=False)
@login_required
def add_expense():
    if request.method == 'GET':
        last = Expense.query.order_by(Expense.id.desc()).first()
        return jsonify(last.id)

    if request.method == 'POST':
        print(request.form)
        if request.form['description'] == '' or request.form['amount'] == '':
            msg = "Missing fields"
        else:
            try:
                new_expense = Expense(
                    id=request.form['id'],
                    repair_id=request.form['repair_id'],
                    expense_status=request.form['paid'],
                    cost_description=request.form['description'],
                    cost=request.form['amount'],
                    T_number=request.form['t_num'],
                    date=date.today(),
                    month=date.today().strftime("%b"),
                    year=date.today().year
                )

                db.session.add(new_expense)
                db.session.commit()
                msg = "Success"
            except Exception as e:
                db.session.rollback()
                msg = "Error"
                print(e)
        return jsonify(msg)


@main.route("/update_expense", methods=("GET", "POST"), strict_slashes=False)
@login_required
def update_expense():
    if request.method == 'POST':
        print(request.form)
        try:
            update = Expense.query.filter_by(id=request.form['id']).first()
            update.cost_description = request.form['description']
            update.cost = request.form['amount']
            update.expense_status = request.form['paid']
            db.session.commit()
            msg = "Successfully updated"
        except Exception as e:
            db.session.rollback()
            print(e)
    return jsonify(msg)


@main.route("/delete_expense", methods=("GET", "POST"), strict_slashes=False)
@login_required
def delete_expense():
    if request.method == 'POST':
        try:
            print(request.form)
            delete_expenses = Expense.query.filter_by(id=request.form['id']).first()
            print(delete_expenses)
            db.session.delete(delete_expenses)
            db.session.commit()
            msg = "Successfully deleted"
        except Exception as e:
            db.session.rollback()
            print(e)

    return jsonify(msg)


@main.route("/notification", methods=("GET", "POST"), strict_slashes=False)
def notification():
    notification_list = []
    # Get current dates in mirrored vehicle detail table
    query = Notification.query
    # Check if the date is expired or soon to be expired, if yes add the date and vehicle to notification queue
    for vehcs in query:
        """date_list = vehicle.to_date_list()
        for field in date_list:
            if field[1] is not None:
                if vehicle.date_stat(field[1]) == 'Expired':
                    notification_list.append(F"{vehicle.T_Number} {field[0]} has <font color='red'>expired</font>")
                    # delete date from notification table if expired"""

        if vehcs.date_stat(vehcs.fitness_exp) == 'Expired':
            notification_list.append(F"{vehcs.T_Number} fitness has <font color='red'>expired</font>")
            vehcs.fitness_exp = None

        if vehcs.date_stat(vehcs.service_date) == 'Expired':
            notification_list.append(F"{vehcs.T_Number} service date has <font color='red'>expired</font>")
            vehcs.service_date = None

        if vehcs.date_stat(vehcs.registration_exp) == 'Expired':
            notification_list.append(F"{vehcs.T_Number} registration has <font color='red'>expired</font>")
            vehcs.registration_exp = None

        if vehcs.date_stat(vehcs.carrier_exp) == 'Expired':
            notification_list.append(F"{vehcs.T_Number} carrier has <font color='red'>expired</font>")
            vehcs.carrier_exp = None

        if vehcs.date_stat(vehcs.cn_exp) == 'Expired':
            notification_list.append(F"{vehcs.T_Number} cover note has <font color='red'>expired</font>")
            vehcs.cn_exp = None

        if vehcs.date_stat(vehcs.insurance_exp) == 'Expired':
            notification_list.append(F"{vehcs.T_Number} insurance has <font color='red'>expired</font>")
            vehcs.insurance_exp = None

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    # Add new notifications to notiflist table
    for notification in notification_list:
        new_notif = NotifList(notification=notification,
                              date=date.today(),
                              read="No")
        try:
            db.session.add(new_notif)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    # Purge notifications those older than 1 day
    new_query = NotifList.query
    for existing in new_query:
        if (existing.date - date.today()).days < 0:
            try:
                db.session.delete(existing)
                db.session.commit()
            except Exception as e:
                db.session.rollback()

    # Build list of notifications to display to user
    notif_list = [{'id': message.id, 'notification': message.notification, 'read': message.read} for message in
                  new_query]

    return jsonify(notif_list)


@main.route("/notification-read", methods=("GET", "POST"), strict_slashes=False)
def notification_read():
    if request.method == 'POST':
        ids = json.loads(request.form['ids'])
        for record in ids:
            query = NotifList.query.filter_by(id=record).first()
            try:
                query.read = "Yes"
                db.session.commit()
            except Exception as e:
                db.session.rollback()

    return jsonify('mhm')
