import mysql.connector
from flask import jsonify


def get_mysql_schema(data):
    if validate_mysql_req(data) == False:
        #  send status code 400 if the request is invalid
        return jsonify({"error": "Invalid Request"}), 400
    try:
        mysql_conn = mysql.connector.connect(
            host=data["host"],
            port=data["port"],
            user=data["user"],
            password=data["password"],
            database=data["database"],
        )
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute("SHOW TABLES")
        tables = mysql_cursor.fetchall()
        json_tables = []
        for table in tables:
            mysql_cursor.execute("DESCRIBE " + table[0])
            columns = mysql_cursor.fetchall()
            json_columns = []
            for column in columns:
                json_columns.append(
                    {
                        "Field": column[0],
                        "Type": column[1].decode("utf-8"),
                        "Null": column[2],
                        "Key": column[3],
                        "Default": column[4],
                        "Extra": column[5],
                    }
                )
            json_tables.append({"Table": table[0], "Columns": json_columns})
        mysql_cursor.close()
        mysql_conn.close()
        return jsonify({"success": "true", "data": json_tables})
    except Exception as e:
        print(e)
        #  send status code 400 if the request is invalid
        return jsonify({"error": "Invalid Request"}), 400


def validate_mysql_req(data):
    # check if all the required fields are present in the dictionary
    if not (data.__contains__("host")):
        return False
    if not (data.__contains__("port")):
        data["port"] = 3306
    if not (data.__contains__("user")):
        return False
    if not (data.__contains__("password")):
        return False
    if not (data.__contains__("database")):
        return False
    return True
