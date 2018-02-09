from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# Database Configurations
app = Flask(__name__)
DATABASE = 'cmpe273'
PASSWORD = 'supersecure'
USER = 'root'

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@db/%s' % (USER, PASSWORD, DATABASE)

# Database migration command line
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    # Data Model User Table
    id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=False)
    category = db.Column(db.String(120), unique=False)
    description = db.Column(db.String(200), unique=False)
    link = db.Column(db.String(200), unique=False)
    estimated_costs = db.Column(db.Integer, unique=False)
    submit_date = db.Column(db.String(120), unique=False)
    status = db.Column(db.String(120), unique=False)
    decision_date = db.Column(db.String(120), unique=False)

    def __init__(self, id, name, email, category, description, link, estimated_costs, submit_date):
        # initialize columns
        self.id = id
        self.name = name
        self.email = email
        self.category = category
        self.description = description
        self.link = link
        self.estimated_costs = estimated_costs
        self.submit_date = submit_date
        self.status = "pending"
        self.decision_date = "09-08-2016"

    def __repr__(self):
        return 'User %r' % self.name


class CreateDB:
    def __init__(self, hostname=None):
        hostname_to_use = 'db'
        import sqlalchemy
        # connect to server
        engine = sqlalchemy.create_engine('mysql://%s:%s@%s' % (USER, PASSWORD, hostname_to_use))
        # create db
        engine.execute("CREATE DATABASE IF NOT EXISTS %s " % DATABASE)


if __name__ == '__main__':
    manager.run()
