from flask import Markup
import psycopg2
import modules.config as c
from modules.categorization import *

from sqlalchemy import Column, Integer, String, create_engine, or_, and_
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

	if nullzp == 1:
		for row in s.query(Jobs).filter(or_(Jobs.salary >= salary_in, Jobs.salary == 0)).filter(Jobs.exp <= exp_in).order_by('date'):
			match = detect_category(search_terms, row.title)
			if match > 0:
				print(row.title)
				job_list.append([row.url, row.title, row.company, int(row.salary), Markup(row.description), row.date, match, row.img, row.id, row.exp, row.links])
	else:
		for row in s.query(Jobs).filter(and_(Jobs.salary >= salary_in, Jobs.salary != 0)).filter(Jobs.exp <= exp_in).order_by('date'):
			match = detect_category(search_terms, row.title)
			if match > 0:
				print(row.title)
				job_list.append([row.url, row.title, row.company, int(row.salary), Markup(row.description), row.date, match, row.img, row.id, row.exp, row.links])


		
	sorted_job_list = sorted(job_list, key=lambda x: x[5], reverse=True)
	return(sorted_job_list)