import psycopg2

conn =  psycopg2.connect(dbname='h44940c_udalenka', user='h44940c_admin', 
						password='xvt192nv2r', host='localhost')
cur = conn.cursor()
cur.execute(
	"delete from jop2 where date < now() - interval '14 days'"
)
conn.commit() 
conn.close()