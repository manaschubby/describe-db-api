import mysql.connector
from flask import request, jsonify

def get_mysql_schema(data):
    if(validate_mysql_req(data)==False):
        return jsonify({'error': 'Invalid Request'})
    try:
        mysql_conn = mysql.connector.connect(
            host=data['host'],
            port=data['port'],
            user=data['user'],
            password=data['password'],
            database=data['database']
        )
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute("SHOW TABLES")
        tables = mysql_cursor.fetchall()
        for table in tables:
            mysql_cursor.execute("DESCRIBE " + table[0])
            columns = mysql_cursor.fetchall()
            print(columns)
        mysql_cursor.close()
        mysql_conn.close()
        return jsonify({'success': 'true'})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Invalid Request'})
    

def validate_mysql_req(data):
    if data['host'] == '':
        return False
    if data['port'] == '':
        data['port'] = 3306
    if data['user'] == '':
        return False
    if data['password'] == '':
        return False
    if data['database'] == '':
        return False
    return True