import psycopg2
import modules.credentials as c

conn =  psycopg2.connect(dbname=c.DBNAME, user=c.USER, 
						password=c.PASSWORD, host=c.HOST)
cur = conn.cursor()
cur.execute(
	"delete from jop2 where date < now() - interval '14 days'"
)
conn.commit() 
conn.close()
