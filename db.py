from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Базовый класс для моделей
Base = declarative_base()

class Employees(Base):
    """Таблица сотрудников"""
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String)
    birth_date = Column(DateTime)
    notes = Column(String)

class Customers(Base):
    """Таблица клиентов"""
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    contact_name = Column(String)

class Orders(Base):
    """Таблица заказов"""
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customers.id))
    employee_id = Column(Integer, ForeignKey(Employees.id))
    order_date = Column(DateTime)
    ship_city = Column(String)

    # Связи с таблицей клиентов и сотрудников
    customer = relationship("Customers", backref=backref("orders"))
    employee = relationship("Employees", backref=backref("orders"))

engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Создаём таблицы в базе данных
Base.metadata.create_all(engine)

from datetime import date

# Получаем сегодняшнюю дату
today = date.today()

# Выбираем сотрудников старше 30 лет
old_employees = session.query(Employees).filter((today.year - Employees.birth_date.year) > 30).all()
print(old_employees)

# Находим нужного клиента и обновляем контактное лицо
client = session.query(Customers).filter_by(company_name='ООО Рога и Копыта').first()
if client:
    client.contact_name = 'Иван Иванов'
    session.commit()

# Удаляем заказ по номеру
order_to_remove = session.query(Orders).filter_by(order_id=1).first()
if order_to_remove:
    session.delete(order_to_remove)
    session.commit()