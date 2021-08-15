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
	jobs = s.query(Jobs.url, Jobs.title, Jobs.company, Jobs.salary, Jobs.description, Jobs.img, Jobs.date, Jobs.id,  Jobs.exp, Jobs.links).all()
	job_list = []
	match = 0
	for c in jobs:
		url = c.url
		title = c.title
		company = c.company
		salary = int(c.salary)
		description = Markup(c.description)
		date = c.date
		img = c.img
		job_id = c.id
		exp = c.exp
		links = c.url
		for term in search_terms.split(' '):
			match = detect_category(term, title)
		job = (c.url, c.title, c.company, int(c.salary), Markup(c.description), c.date, match, c.img, c.id, c.exp, c.links)
		if exp is None:
			exp = 0
		if nullzp == 1:
			if match > 0 and exp_in >= exp and (salary_in <= salary or salary == 0):
				if tag_list == "anything":
					if any(x in url for x in sources.split(' ')) or any(x in links for x in sources.split(' ')):
						job_list.append(job)
					else:
						pass
				else:
					for i in tag_list.split(' '):
						if i in title.lower() or i in description:
							if any(x in url for x in sources.split(' ')) or any(x in links for x in sources.split(' ')):
								job_list.append(job)
							else:
								pass
						else:
							pass
			else:
				pass
		else:
			if match > 0 and exp_in >= exp and (salary_in <= salary and salary != 0):
				if tag_list == "anything":
					job_list.append(job)
				else:
					for i in tag_list.split(' '):
						if i in title.lower() or i in description:
							if any(x in url for x in sources.split(' ')) or any(x in links for x in sources.split(' ')):
								job_list.append(job)
							else:
								pass
						else:
							pass
			else:
				pass
		match = 0
		
	sorted_job_list = sorted(job_list, key=lambda x: x[5], reverse=True)
	return(sorted_job_list)