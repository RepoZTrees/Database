import csv
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, BLOB, Date, Boolean, Table
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Customer(Base):
    __tablename__="invoice_customer"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    jdate = Column(Date)
    address = Column(String)
    email = Column(String)
    invoices = relationship('Invoice', backref="customer")


class Invoice(Base):
    __tablename__="invoice_invoice"
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
    #url = "sqlite:///invoice_db.sqlite"
    engine = create_engine(url)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session

def main(fname):
    session = get_session()
    #print(session.query(Customer()
    c =  session.query(Customer).all()
    #for row in session.query(Customer).all():
        #print(row.id)
    
    with open(fname, 'wt') as f:
        writer = csv.writer(f)
        writer.writerow(('id','name','address','email'))
        for i in c:
            id_,name,address,email = i.id,i.name,i.address,i.email
            csv_row = (id_,name,address,email)
            writer.writerow(csv_row)

if __name__ == "__main__":
    main(sys.argv[1])
