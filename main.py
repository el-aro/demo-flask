import os
import sys
import math
from flask import Flask
from flask import abort
from flask import request
from flask import make_response
from datetime import datetime
import time
import datetime
import json
import sqlalchemy
from utils.dao import DataAccessObject

def init_connection_engine():
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,  # 30 seconds
        pool_recycle=1800,  # 30 minutes
    )
    return pool

db = init_connection_engine()
dao = DataAccessObject(db)

app = Flask(__name__)
app.secret_key = '!secret'

person_minimal_input = [    
    'last_name' ,
    'first_name' ,
    'date_of_birth',
    'email'
]

def create_response(json_string, content_type = 'application/json', status_code = 200):
    response = make_response(json_string)                                           
    response.headers['Content-Type'] = '{0}; charset=utf-8'.format(content_type)
    response.status_code = status_code            
    return response

def fix_date_of_birth(persons):
    for person in persons:
        person['date_of_birth'] = person['date_of_birth'].strftime('%Y-%m-%d')

def get_request_data(request):
    return (
        request.args
        or request.form
        or request.get_json(force=True, silent=True)
        or request.data
        or {}
    )

def get_input_create():
    '''
        Metodo para validar el input para crear usuario.
    '''
    data = get_request_data(request)
    print(data)
    if len(data):
        print('paso len')
        for key, value in data.items():
            print('entro for')
            if key not in person_minimal_input:
                abort(422,'{"message":"input incorrecto, necesarios: name, first_name,date_of_birth,email"}')
    else:
        abort(422,'{"message":"input incorrecto, necesarios: name, first_name,date_of_birth,email"}')
    try:
        datetime.datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
    except ValueError:
        abort(422,'{"message":"input date_of_birth incorrecto, formato: name, YYYY-MM-DD"}')
    return data

@app.route('/api/user', methods=['GET'])
def user_search():
    data = get_request_data(request)
    page = 1 if 'pagina' not in data.keys() else int(data['pagina'])
    per_page = 10 if 'por_pagina' not in data.keys() else int(data['por_pagina'])
    total = dao.get_persons_total()['total']
    offset = (page - 1) * per_page if page > 1 else 0
    total_paginas = math.ceil(total / per_page)
    persons = dao.get_persons(offset, per_page)
    fix_date_of_birth(persons)
    parameters = {
        'pagina': page,
         "resultados" : persons,
        'por_pagina': per_page,
        'total': total,
        'total_paginas': total_paginas
    }
    return parameters
    return data

@app.route('/api/user/<user_id>', methods=['GET'])
def user_by_id(user_id):
    user = dao.get_person_by_id(user_id)
    if not user:
        abort(422,'{"message":"usuario no encontrado"}')
    user['date_of_birth'] = user['date_of_birth'].strftime('%Y-%m-%d')
    return create_response(json.dumps(user))

@app.route('/api/user', methods=['POST'])
def user_create():
    user_data = get_input_create()
    if dao.get_person_by_email(user_data['email']):
        abort(422,'{"message":"email ya registrado en sistema"}')
    person_id = dao.save_person(user_data)
    person = dao.get_person_by_id(person_id)
    person['date_of_birth'] = person['date_of_birth'].strftime('%Y-%m-%d')
    return create_response(json.dumps(person))

@app.route('/api/user/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    user = dao.get_person_by_id(user_id)
    if not user:
        abort(422,'{"message":"usuario no encontrado"}')
    dao.delete_person_by_id(user_id)
    return create_response(json.dumps({"message":"usuario borrado"}))

@app.route('/api/user/<int:user_id>', methods=['PUT'])
def user_update(user_id):
    user_data = get_input_create()
    if not dao.get_person_by_id(user_id):
        abort(422,'{"message":"usuario no encontrado"}')
    if dao.get_person_by_email(user_data['email']):
        abort(422,'{"message":"email ya registrado en sistema"}')
    user_data['id'] = int(user_id)
    dao.update_person(user_data)
    person = dao.get_person_by_id(user_id)
    person['date_of_birth'] = person['date_of_birth'].strftime('%Y-%m-%d')
    return create_response(json.dumps(person))

@app.errorhandler(422)
def generic_error(error):
    return create_response(error.description, status_code = 422)

if __name__ == '__main__':
    app.run()