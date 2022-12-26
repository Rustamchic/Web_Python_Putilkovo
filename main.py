import json
from flask import Flask, request, render_template, jsonify, redirect
import psycopg2
import random
"""Основной задачей данного веб-приложения является построение универсального контроля 
купленных квартир гражданами в городе Путилково"""
app = Flask(__name__)
data = [{'id' : 0, 'name' : 'Rustic', 'surname' : 'Khilyazov', 'flat_quantity' : 3},
        {'id' : 1, 'name' : 'Ilya Konstantinovich', 'surname' : 'Shatalov', 'flat_quantity' : 10}]
conn = psycopg2.connect(
    host="localhost",
    database="JK_Putilkovo",
    user="postgres",
    password="Rustic_MAI",
    port=5432
)
cursor = conn.cursor()
success_message = {'success': True}


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/users', methods=['GET'])
def get_users():
    data_users = []
    sql = 'SELECT * FROM user'
    cursor.execute(sql)
    data = cursor.fetchall()
    for buyer in data:
        data_users.append({'id': buyer[0],
                            'name': buyer[1],
                            'surname': buyer[2],
                            'flat_quantity': buyer[3]})
    print(data_users)
    print(request.url)
    return render_template('owners.html', owners=data_users)


@app.route('/users/<id_user>', methods=['GET'])
def get_user(id_user):
    data_user = []
    sql = 'SELECT * FROM owner WHERE id_user = %s'
    cursor.execute(sql, (id_user,))
    data = cursor.fetchall()
    for sq_user in data:
        data_user.append({'id': sq_user[0],
                            'name': sq_user[1],
                            'surname': sq_user[2],
                            'flat_quantity': sq_user[3]})
    print(data_user)
    print(request.url)
    return render_template('owner.html', owners=data_user[0])

@app.route('/users/<id_user>/flat', methods=['GET'])
def get_cars(id_user):
    sql = 'SELECT * FROM flat, user WHERE user.id_user = flat.id_user and flat.id_user = %s'
    cursor.execute(sql, (id_user,))
    data = cursor.fetchall()
    Fdata = []
    if not not data:
        for fl in data:
            data.append({'id': fl[0],
                             'quality': fl[1],
                             'area': fl[2],
                             'name': fl[3],
                             'surname': fl[4],
                             'phone_number': fl[5]})
        print(data)
        print(request.url)
    return render_template('cars.html', data=Fdata, id=id_user)

@app.route('/owners', methods=['POST'])
def add_owner():
    sql = 'INSERT INTO owner VALUES (%s, %s, %s, %s)'
    id = random.randint(1, 999999)
    name = request.get_json()['name']
    surname = request.get_json()['surname']
    quality = request.get_json()['quality of flats']
    cursor.execute(sql, (id, name, surname, quality))
    conn.commit()
    return get_user(id)


@app.route('/owners/<id_owner>', methods=['DELETE'])
def del_owners(id_user):
    sql = 'DELETE FROM user WHERE id_owner = %s'
    cursor.execute(sql, (id_user,))
    conn.commit()
    return get_users()


@app.route('/users/<id_user>', methods=['PUT'])
def update_owner(id_owner):
    sql = 'UPDATE user SET name = %s, surname = %s, quality = %s WHERE id_user = %s'
    name = request.get_json()['name']
    surname = request.get_json()['surname']
    quality = request.get_json()['quality']
    cursor.execute(sql, (name, surname, quality))
    conn.commit()
    return get_user(id_owner)
if __name__ == '__main__':
    app.run(debug = True)