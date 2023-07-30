import mysql.connector
import flask
from flask import request, jsonify
from mysql_schema import get_mysql_schema

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Route for MySQL Schema
@app.route('/mysql', methods=['GET'])
def getSchema():
    return get_mysql_schema(request.args)

if __name__ == '__main__':
    app.run()
