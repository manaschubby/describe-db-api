import mysql.connector
import flask
from flask import request, jsonify
from mysql_schema import get_mysql_schema
from postgresql_schema import get_psql_schema

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Route for MySQL Schema
@app.route("/mysql", methods=["GET"])
def getMysqlSchema():
    return get_mysql_schema(request.get_json())


# Route for PostgreSQL Schema
@app.route("/psql", methods=["GET"])
def getPsqlSchema():
    return get_psql_schema(request.get_json())


@app.route("/", methods=["GET"])
def home():
    print(request.get_json())
    return "<h1>Schema Generator</h1><p>This site is a prototype API for generating schema for MySQL and PostgreSQL databases.</p>"


#  Run the app using the following command:
#  python main.py

if __name__ == "__main__":
    app.run()
