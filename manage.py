def deploy():
    """Run deployment tasks. Create the database using the flask application context"""

    from fleetdashboard import create_app
    from flask_migrate import upgrade, migrate, init, stamp

    app = create_app()
    app.app_context().push()


    # migrate database to latest revision
    init()
    stamp()
    migrate()
    upgrade()


def register():
    """Register a user directly to the database using application context"""
    from fleetdashboard import create_app, db, bcrypt
    from fleetdashboard.models import User, Service, Notification, NotifList, Vehicle, History, Expense, Status
    from werkzeug.routing import BuildError
    from sqlalchemy import create_engine, inspect, MetaData

    from sqlalchemy.exc import (
        IntegrityError,
        DataError,
        DatabaseError,
        InterfaceError,
        InvalidRequestError,
    )

    app = create_app()
    app.app_context().push()
    db.create_all()

    try:
        newuser = User(
            email="dummy@email.com",
            pwd=bcrypt.generate_password_hash("Password123."),
        )

        db.session.add(newuser)
        db.session.commit()

    except InvalidRequestError:
        db.session.rollback()
        print(f"Something went wrong!", "danger")
    except IntegrityError:
        db.session.rollback()
        print(f"User already exists!.", "warning")
    except DataError:
        db.session.rollback()
        print(f"Invalid Entry", "warning")
    except InterfaceError:
        db.session.rollback()
        print(f"Error connecting to the database", "danger")
    except DatabaseError:
        db.session.rollback()
        print(f"Error connecting to the database", "danger")
    except BuildError:
        db.session.rollback()
        print(f"An error occured !", "danger")

    engine = create_engine("sqlite:///database.db")
    metadata_obj = MetaData(bind=engine)
    insp = inspect(engine)
    print(insp.get_table_names())

    MetaData.reflect((metadata_obj))
    users_table = metadata_obj.tables['user']
    print(users_table.columns)

    query = db.select([
        users_table.c.id,
        users_table.c.email,
        users_table.c.pwd,
    ])

    result = engine.execute(query).fetchall()
    print(result)


def delete():
    from fleetdashboard.models import Expense
    from sqlalchemy import create_engine

    # app = create_app()
    # app.app_context().push()
    # delete records
    # db.session.query(Service).delete()
    # db.session.commit()

    # Vehicle.query.all()

    engine = create_engine("sqlite:///database.db")
    Expense.__table__.drop(engine)


register()