import psycopg2

conn =  psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
cur = conn.cursor()
cur.execute(
	"delete from jop2 where date < now() - interval '14 days'"
)
conn.commit() 
conn.close()
