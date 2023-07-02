import psycopg2

conn_string = "host='localhost' dbname='postgres' user='admin' password='admin'"
conn = psycopg2.connect(conn_string)

