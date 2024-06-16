from sqlalchemy import Column, Integer, Float, Date, DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
import datetime
from flask_login import UserMixin

# Класс магазина, в котором храним информацию о названии, номер, и почта

class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, default="")
    phone_number = Column(String(100), nullable=False, default="")
    mail = Column(String(200), nullable=False, default="")
    address = Column(String(200), nullable=False, default="")
    login = Column(String(100), unique=True)
    password = Column(String(200))


class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), default='')
    cost = Column(String(40), default='')
    photo = Column(String(100), default='')
    sostav = Column(String(350), default='')  # Изменен тип поля sostav на Text
    weight = Column(String(110), default='')
    category_id = Column(Integer, ForeignKey('category.id'))  # Добавлена связь с таблицей Category

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, default='')

class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer,primary_key=True)
    name = Column(String(200), default='')
    phone = Column(String(40), default='')
    email = Column(String(100), default='')
    address = Column(String(400), default='')
    dni_nedeli = Column(String(110), default='')
    time = Column(String(50), default='')

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    FIO = Column(String(250), nullable=False)
    phone = Column(String(120), nullable=False)
    guests_count = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=False)

# Функция для инициализации БД
def init_db():
    from database import engine
    Base.metadata.create_all(bind=engine)
    db_session.commit()

# Функции для вывода схемы таблиц
def print_schema(table_class):
    from sqlalchemy.schema import CreateTable, CreateColumn
    print(str(CreateTable(table_class.table).compile(db_engine)))

def print_columns(table_class,  * attrNames):
    from sqlalchemy.schema import CreateTable, CreateColumn
    c = table_class.table.c
    print(',\r\n'.join((str(CreateColumn(getattr(c, attrName)).compile(db_engine)) for attrName in attrNames if hasattr(c, attrName))))

# Если этот файл запускается напрямую, то инициировать БД
if __name__ == "__main__":
    init_db()  # Проверка правильности созданных классов и связи между классом блюда и категорией
