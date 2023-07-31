import psycopg2
from flask import jsonify
from mysql_schema import validate_mysql_req


def get_psql_schema(data):
    if validate_psql_req(data) == False:
        return jsonify({"error": "Invalid Request"})
    try:
        psql_conn = psycopg2.connect(
            host=data["host"],
            port=data["port"],
            user=data["user"],
            password=data["password"],
            database=data["database"],
        )
        psql_cursor = psql_conn.cursor()

        # Using a parameterized query to retrieve table names
        psql_cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )
        tables = psql_cursor.fetchall()

        json_tables = []
        for table in tables:
            # Using a parameterized query to retrieve column information for each table
            psql_cursor.execute(
                "SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = %s",
                (table[0],),
            )
            columns = psql_cursor.fetchall()
            json_columns = []
            for column in columns:
                json_columns.append(
                    {
                        "Field": column[0],
                        "Type": column[1].decode("utf-8"),
                        "Null": column[2],
                        "Default": column[3],
                    }
                )
            json_tables.append({"Table": table[0], "Columns": json_columns})
        print(json_tables)
        psql_cursor.close()
        psql_conn.close()
        return jsonify({"success": "true", "data": json_tables})

    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid Request"})


def validate_psql_req(data):
    if not (data.__contains__("port")):
        data["port"] = 5432
    # Rest of the validation is same as mysql
    return validate_mysql_req(data)
