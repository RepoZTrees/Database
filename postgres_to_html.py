# Postgres to html
# Write a function that will read out the entries in your customer database and # produce an HTML file with customer information
# database name: invoices_sql_alchemy

from faker import Faker
from jinja2 import Template
import csv
import psycopg2
import os
import jinja2

fake = Faker()

def main(html_file):
    current_path = os.getcwd()
    file_name = os.path.join(current_path,html_file)

    if os.path.exists(file_name):
        os.remove(file_name)

    conn = psycopg2.connect('dbname = invoices_sql_alchemy')
    curr = conn.cursor()
    curr.execute("""DROP TABLE IF EXISTS customer;""")
    curr.execute("""CREATE TABLE customer(id INTEGER PRIMARY KEY, name VARCHAR(50), jdate DATE, address TEXT, email VARCHAR(50));""")

    for i in range(1,21):
        id_ = i
        name = fake.name()
        date = fake.date()
        address = fake.address()
        email = fake.email()
        curr.execute("""INSERT INTO customer(id, name, jdate, address, email) VALUES(%s, %s, %s, %s, %s);""",
                     (id_,name, date, address, email))
        conn.commit()
        curr.execute("SELECT * FROM customer")
        results = curr.fetchall() # fetch all the records except header
        headers = [i[0] for i in curr. description] # curr.description fetch only header/title record        
    
    string = ""
    for i in headers:
        string += f"<th align='left' style='vertical-align: bottom;'>{i}</th>"
    title_tag = "<thead>" + "<tr style='width:100%; border:1px solid black; border-collapse:collapse;'>" + string + "</tr>" + "</thead>"

    tag1 = ""
    for result in results:
        string = ""
        for i in result:
            string += f"<td style='vertical-align: bottom;'>{i}</td>"
        tag1 += "<tr style='width:100%; border:1px solid black; border-collapse:collapse;'>" + string + "</tr>"

    data_tag = "<tbody>" + tag1 + "</tbody>"
    table = "<table style = 'width:100%; border:1px solid black; border-collapse:collapse;'>" + title_tag + data_tag + "</table>"
    with open(html_file,'w') as f:
        f.write(table)

if __name__ == '__main__':
    main("customer_info.html")
    
