from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import modules.credentials as c

engine = create_engine(c.ENGINE, echo=False)
Base = declarative_base()
session = sessionmaker(bind=engine)
s = session()

class Jobs(Base):
	__tablename__ = c.TABLE
	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=False)
	url = Column(String)
	company = Column(String)
	exp = Column(Integer)
	salary = Column(Integer)
	description = Column(String)
	img = Column(String)

def get_jobs():
	return s.query(Jobs.title, Jobs.company).all()

def get_last_id():
	return s.query(Jobs).order_by(Jobs.id.desc()).first().id + 1

def add_job(url, title, company, salary, description_text, img_src, exp_final, job_id):
	new_job = Jobs(url=url, title=title, company=company, salary=salary, description=description_text, img=img_src, id=job_id, exp=exp_final)
	print(url, title, exp_final)
	s.add(new_job)
	#s.commit() 