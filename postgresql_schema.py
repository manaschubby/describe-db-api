import psycopg2
from flask import jsonify
from mysql_schema import validate_mysql_req

def get_psql_schema(data):
    pass

def validate_psql_req(data):
    if data['port'] == '':
        data['port'] = 5432
    # Rest of the validation is same as mysql
    return validate_mysql_req(data)