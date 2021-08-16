from flask import Markup
import psycopg2
import modules.config as c
from modules.categorization import *

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
	date = Column(String)
	links = Column(String)

def search(search_terms, exp_in, tag_list, salary_in, nullzp, sources, sort_by):
	jobs = s.query(Jobs.url, Jobs.title, Jobs.company, Jobs.salary, Jobs.description, Jobs.img, Jobs.date, Jobs.id, Jobs.exp, Jobs.links).all()
	job_list = []
	for c in jobs:
		for term in search_terms.split(' '):
			match = detect_category(term, c.title)
		job = (c.url, c.title, c.company, int(c.salary), Markup(c.description), c.date, match, c.img, c.id, c.exp, c.links)
		if nullzp == 1:
			if match > 0 and exp_in >= c.exp and (salary_in <= int(c.salary) or int(c.salary) == 0):
				if tag_list == "anything":
					if any(x in c.url for x in sources.split(' ')) or any(x in c.links for x in sources.split(' ')):
						job_list.append(job)
				else:
					for i in tag_list.split(' '):
						if i in c.title.lower() or i in Markup(c.description):
							if any(x in c.url for x in sources.split(' ')) or any(x in c.links for x in sources.split(' ')):
								job_list.append(job)
		else:
			if match > 0 and exp_in >= c.exp and (salary_in <= int(c.salary) and int(c.salary) != 0):
				if tag_list == "anything":
					job_list.append(job)
				else:
					for i in tag_list.split(' '):
						if i in c.title.lower() or i in Markup(c.description):
							if any(x in c.url for x in sources.split(' ')) or any(x in c.links for x in sources.split(' ')):
								job_list.append(job)
		
	sorted_job_list = sorted(job_list, key=lambda x: x[5], reverse=True)
	return(sorted_job_list)