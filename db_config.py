import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="HIVE",
        user="postgres",
        password="",
        host="localhost",
        port="5433"
    )
