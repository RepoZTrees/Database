# Postgres to html
# Write a function that will read out the entries in your customer database and # produce an HTML file with customer information
# database name: invoices_sql_alchemy

import random
from faker import Faker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, BLOB, Date, Boolean, Table
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = "invoice_customer"
    id = Column(Integer, primary_key =  True)
    name = Column(String)
    jdate = Column(Date)
    address = Column(String)
    email = Column(String)
    invoices = relationship('Invoice', backref="customer")
    
class Invoice(Base):
    __tablename__ = "invoice_invoice"
    id = Column(Integer, primary_key = True)
    particulars = Column(String)
    date = Column(Date)
    amount = Column(Integer)
    customer_id = Column(Integer, ForeignKey('invoice_customer.id'))

def create_db():
    url = "postgres:///invoices_sql_alchemy"
    #url = "sqlite:///invoice_db.sqlite"
    engine = create_engine(url)
    Base.metadata.create_all(engine)

def get_session():
    url = "postgres:///invoices_sql_alchemy"
    #url = "sqlite:///"invoice_db.sqlite"
    engine = create_engine(url)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session


def main(html_file):
    create_db()
    session = get_session()
    records = session.query(Customer).all()
    header = Customer.__table__.columns.keys()

    string = ""
    for i in header:
        string += f"<th align='left' style='vertical-align: bottom;'>{i}</th>"
    title_tag = "<thead>" + "<tr style='width:100%; border:1px solid black; border-collapse:collapse;'>" + string + "</tr>" + "</thead>"

    tag1 = ""
    for record in records:
        string = ""
        for c in header:
            string += f"<td style='vertical-align: bottom;'>{getattr(record,c)}</td>"
        tag1 += "<tr style='width:100%; border:1px solid black; border-collapse:collapse;'>" + string + "</tr>"

    data_tag = "<tbody>" + tag1 + "</tbody>"
    table = "<table style = 'width:100%; border:1px solid black; border-collapse:collapse;'>" + title_tag + data_tag + "</table>"
    with open(html_file,'w') as f:
        f.write(table)

if __name__ == '__main__':
    main("sample.html")
    
