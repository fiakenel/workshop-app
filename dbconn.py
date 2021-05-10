import psycopg2

conn = psycopg2.connect(host='localhost',
                        port=5432,
                        database='workshop',
                        user='maksym',
                        password='')
cur = conn.cursor()
