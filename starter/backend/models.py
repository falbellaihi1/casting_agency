import os

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import json
import os
database_name = "casting_agency"
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
#database_path = "postgresql://{}:{}@{}/{}".format(DBUSER, DBPASS, 'localhost:5432', database_name)
database_path = "postgresql://postgres:0000@{}/{}".format('localhost:5432', database_name)
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    # con = psycopg2.connect("dbname=postgres user=postgres password=0000")
    # print(con)
    # con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # cur = con.cursor()
    # cur.execute('DROP DATABASE IF EXISTS {};'.format(database_name))
    # cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
    # cur.close()
    # con.close()
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
def create_db():
    db.create_all()



class Movies(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id':self.id,
            'title':self.title,
            'release_date':self.release_date,
        }

    def __repr__(self):
        return f' movie {self.id}, {self.title}, {self.release_date}'


class Actors (db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    def __init__(self, name, age, gender):
        self.name = name
        self.age =age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id':self.id,
            'name':self.name,
            'age':self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return f' movie {self.id}, {self.title}, {self.release_date}'