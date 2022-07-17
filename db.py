from sqlalchemy import exists, null, MetaData
from models import *
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
import pandas as pd
from datetime import date, datetime, timedelta

app = Flask(__name__)
bcrypt = Bcrypt(app)

def mk_session(fun):
    def wrapper(*args, **kwargs):
        s = session()
        kwargs['session'] = s
        try:
            res = fun(*args, **kwargs)
        except Exception as e:
            s.rollback()
            s.close()
            raise e

        s.close()
        return res
    wrapper.__name__ = fun.__name__
    return wrapper

#For Inserting User to table
@mk_session
def dbInsertUser(session=None):
    data = request.get_json()
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    if data['role'] == "admin":
        admin = True
    elif data['role'] == 'user':
        admin = False
    new_user = Users(username=data['username'], password=password, admin = admin, signup_date= getCurrentTime())
    session.add(new_user)
    session.commit()
    return jsonify({"message":"New User created"},data)

#For Login
@mk_session
def dbGetUserByName(username, session=None):
    query = session.query(Users).filter(Users.username==username).statement
    df = pd.read_sql( query, engine)
    print(df)
    if(not df.empty):
        return df.at[0,'id'], df.at[0, 'password']

#For gettting user from database
@mk_session
def dbGetUser(username, session=None):
    query = session.query(Users).filter(Users.username== username).statement
    df = pd.read_sql( query, engine)
    print(df)
    if(not df.empty):
        return df.at[0,'id']

#For placing order
@mk_session
def place_orders(data, session=None):
    for i in range(1,len(data)+1):
        item_name = data[('order'+str(i))]['item_name']
        query=session.query(Products).filter(Products.product==item_name).statement
        df = pd.read_sql(query,engine)
        print(df)
        total_price = float(data[('order'+str(i))]['quantity']) * (df.at[0,'price'])
        print(total_price)
        new_order = Orders(product_name = item_name,
        quantity = data[('order'+str(i))]['quantity'], 
        total_price = total_price,
        order_date = getCurrentTime())
        session.add(new_order)
        session.commit()
    return jsonify({"message":"Order placed!!"})

#For Uploading items into database
@mk_session
def items(session=None):
    with open('product_list.csv', 'r') as file:
        query = session.query(Products).filter(Products.product is not null).statement
        df1 = pd.read_sql(query,engine)
        print(df1)
        if(not df1.empty):
            df = pd.read_csv(file)
            df.set_index('id', inplace=True)
            print(df)
            for i in range(1,len(df)+1):
                ret = session.query(exists().where(Products.product==df.at[i,'product'])).scalar()
                print(ret)
                if ret is True:
                    updatePrice = {'price':float(df.at[i,'price'])}
                    session.query(Products).filter(Products.product==df.at[i,'product']).update(updatePrice)
                    session.commit()
                elif ret is False:
                    addItem = {'id': df.at[i,'id'], 'product':df.at[i,'product'], 'price':df.at[i,'price']}
                    session.query(Products).filter(Products.product)!=df.at[i,'product'].update(addItem)
                    session.commit()
        elif(df1.empty):
            df1 = pd.read_csv(file)
            df1.set_index('id', inplace=True)
            df1.to_sql('products', engine, if_exists='append')
        
    return jsonify({"message":"items uploaded to database"})

#For retrieving orders of 3 months
@mk_session
def check_orders(session=None):
    list1 = []
    prev_orders = session.query(Orders).filter(Orders.order_date>date.today()-timedelta(weeks=12)).all()

    for prev_order in prev_orders:
        list1.append({"product name":prev_order.product_name, "quantity": prev_order.quantity,
        "total price":prev_order.total_price, "order date": prev_order.order_date})
    return jsonify(list1)

def getCurrentTime():
 now = datetime.now()
 date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
 return date_time_str