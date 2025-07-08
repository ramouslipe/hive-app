import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="HIVE",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )

