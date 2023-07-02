import psycopg2

# conn_string = "host='localhost' dbname='postgres' user='admin' password='admin'"
conn_string = "host='ep-patient-sky-333978-pooler.us-east-1.aws.neon.tech' dbname='test' user='aarontravass' password='QbGq3Jv6zhAM'"
conn = psycopg2.connect(conn_string)

