from bs4 import BeautifulSoup
import requests
import re
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:xvt192nv2r@localhost:5432/peton", echo=False)
Base = declarative_base()
session = sessionmaker(bind=engine)
s = session()

class Jobs(Base):
	__tablename__ = 'jop2'
	id = Column(Integer, primary_key=True)
	title = Column(String(250), nullable=False)
	url = Column(String(250))
	company = Column(String(250))
	exp = Column(Integer)
	salary = Column(Integer)
	description = Column(String)
	img = Column(String)

def get_exp(description_text):
	description_dict = {"<li>": "<p>", "<span": "<p>", "<br/>": "<p>", "&nbsp;": "<p>", u"\xa0": u" "}
	for i, j in description_dict.items():
		description_text = description_text.replace(i, j).strip()
	desc_list = description_text.split("<p>")
	try:
		y1 = ['1+ ', '1 y', '1 г', '1 ле', '1 р', '1+ г', '1+ л', '1+ р', '1-го го', 'не менее одного', 'не менее год', 'более одного', 'один год', '1-2', '1-3', '1 to 2', '1 to 3', '1 до 2', '1 до 3', 'half a year', 'полгода', 'півроку']
		y2 = ['2+ ', '2 y', '2 г', '2 ле', '2 р', '2+ г', '2+ л', '2+ р', '2-х р', '2-х л', '2х л', '2х р', 'двох', 'двух', '2-3', '2-4', '2-5', '2 to 3', '2 to 4', '2 to 5', '2 до 3', '2 до 4', '2 до 5', '1.5', '1,5', 'полтора', 'півтора']
		y3 = ['3+ ', '3 y', '3 г', '3 ле', '3 р', '3+ г', '3+ л', '3+ р', '3-х р', '3-х л', '3х л', '3х р', 'трьох', 'трёх', 'трех', '3-4', '3-5', '3-6', '3 to 4', '3 to 5', '3 to 6', '3 до 4', '3 до 5', '3 до 6', '2.5', '2,5']
		y4 = ['4+ ', '4 y', '4 г', '4 ле', '4 р', '4+ г', '4+ л', '4+ р', '4-х р', '4-х л', '4х л', '4х р', '4-5', '4-6', '4 to 5', '4 to 6', '4 до 5', '4 до 6', '3.5', '3,5']
		y5 = ['5+ ', '5 y', '5 г', '5 ле', '5 р', '5+ г', '5+ л', '5+ р', 'пяти']
		exps = ['exp', 'досв', 'опыт', 'years in']
		exp = []
		for i in desc_list:
			if any(x in i.lower() for x in exps):
				if any(x in i for x in y5) and not '0.5' in i and not ' до 5' in i and not ' to 5' in i and not '-5' in i:
					exp.append(5)
				elif any(x in i for x in y4) and not ' до 4' in i and not ' to 5' in i and not '-4' in i:
					exp.append(4)
				elif any(x in i for x in y3) and not ' до 3' in i and not ' to 5' in i and not '-3' in i:
					exp.append(3)
				elif any(x in i for x in y2) and not ' до 2' in i and not ' to 5' in i and not '-2' in i:
					exp.append(2)
				elif any(x in i for x in y1):
					exp.append(1)
			else:
				exp.append(0)
			exp_final = max(exp)
	except Exception as e:
		exp_final = 0
	return(exp_final)

def clean_title(title):
	title_dic = {"удаленно": "", "удалённо": "", "на дому": "", "-centre": "-центра", " центра": "-центра", "()": ""}
	for i, j in title_dic.items():
		title = title.replace(i, j).strip()
	return title
	
class Parser():
	def __init__(self):
		self.job_id = s.query(Jobs).order_by(Jobs.id.desc()).first().id + 1
		
	def djinni_get_urls(self):
		response = requests.get('https://djinni.co/jobs/?remote_type=remote&page=5')
		soup = BeautifulSoup(response.content, 'html.parser')
		job_elements = soup.find_all('a', class_= 'profile')
		for element in job_elements:
			db_data = s.query(Jobs.title, Jobs.company).all()
			url = 'https://djinni.co' + element["href"]
			title = element.text.strip()
			salary = 0
			salary_element = element.find_next_sibling('span', class_= 'public-salary-item')
			if salary_element:
				salary = int(salary_element.text.split('$')[1].split('-')[-1])*27
			company = ''
			company_element = element.parent.find_next_sibling('div', class_= 'list-jobs__details').findChildren('div', class_= 'list-jobs__details__info')[0].findChildren('a')[1]
			if company_element:
				company = company_element.text
			if not any((title + ' ' + company) in ' '.join(row) for row in db_data):
				self.djinni_get_description(url, title, company, salary)
				
	def djinni_get_description(self, url, title, company, salary):
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		img_src = '/static/logo.svg'
		description_element = soup.find_all('div', class_= 'profile-page-section')[1]
		description_text = description_element.decode_contents().replace('\n\r', '</br>').replace('\n', '</br>')
		exp_element = soup.find('div', class_= 'list-jobs__details__info')
		exp_in_info = 0
		if exp_element and not 'без досв' in exp_element.text:
			exp_in_info = int(re.search(r'· (.+?) р', exp_element.text).group(1))
		exp_in_description = get_exp(description_text)
		exp_final = max(exp_in_description, exp_in_info)
		self.add_job(url, title, company, salary, description_text, img_src, exp_final)
		
	def rabota_get_urls(self):
		response = requests.get('https://api.rabota.ua/vacancy/search?count=10&parentId=1&scheduleId=3')
		for new_job in response.json()['documents']:
			db_data = s.query(Jobs.title, Jobs.company).all()
			title = new_job['name']
			company = new_job['companyName']
			if not any((title + ' ' + company) in ' '.join(row) for row in db_data):
				self.rabota_job(title, company, new_job['id'])
				
	def rabota_get_description(self, title, company, jid):
		response = requests.get('https://api.rabota.ua/vacancy?id=' + str(jid))
		url = 'https://rabota.ua/company' + str(response.json()['notebookId']) + '/vacancy' + str(response.json()['id'])
		img_src = 'https://company-logo-frankfurt.rabota.ua/cdn-cgi/image/w=250/' + response.json()['logo']
		description_text = response.json()['description']
		exp_final = get_exp(description_text)
		salary = max(response.json()['salaryFrom'], response.json()['salaryTo'], response.json()['salary'])
		self.add_job(url, title, company, salary, description_text, img_src, exp_final)
	
	def work_get_urls(self):
		response = requests.get('https://www.work.ua/jobs-it/?advs=1&employment=76&nosalary=1&page=' + str(i))
		soup = BeautifulSoup(response.content, 'html.parser')
		job_elements = soup.find_all('h2')
		for element in job_elements[:-6]:
			db_data = s.query(Jobs.title, Jobs.company).all()
			url = 'https://www.work.ua' + element.findChildren('a')[0]["href"]
			title = clean_title(element.findChildren('a')[0].text)
			company = ''
			company_element = element.find_next_sibling('div', class_= "add-top-xs")
			if company_element:
				company = company_element.text.split('·')[0].split(',')[0].strip()
			if not any((title + ' ' + company) in ' '.join(row) for row in db_data):
				self.work_get_description(url, title, company)
				
	def work_get_description(self, url, title, company):
		response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')
		img_element = soup.find('img', class_= "logo-job")
		img_src = '/static/logo.svg'
		if img_element:
			img_src = img_element['src']
		salary_elements = soup.find_all('b', class_ = 'text-black') + soup.find_all('span', class_ = 'text-muted')
		salary = 0
		for element in salary_elements:
			if '00' in element.text and not element.findChildren() and 'грн' in element.text:
				salary = int(''.join(i for i in element.text.split('–')[-1].split('-')[-1] if i.isdigit()))
			elif '00' in element.text and not element.findChildren() and '$' in element.text:
				salary = int(''.join(i for i in element.text.split('–')[-1].split('-')[-1] if i.isdigit()))
			else:
				break
		exp_element = soup.find('span', title = "Умови й вимоги").find_parent('p')
		exp_text = re.search(r'роботи від(.+?) ', exp_element.text)
		if exp_text:
			exp_in_info = int(exp_text.group(1) or 0)
		description_element = soup.find('div', id= "job-description")
		description_text = description_element.decode_contents()
		exp_in_description = get_exp(description_text)
		exp_final = max(exp_in_description, exp_in_info)
		self.add_job(url, title, company, salary, description_text, img_src, job_id, exp_final)
			
	def grc_get_urls(self):
		response = requests.get('https://grc.ua/search/vacancy?clusters=true&enable_snippets=true&items_on_page=100&no_magic=true&order_by=publication_time&search_period=7&text=&area=5&specialization=1&schedule=remote', headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(response.content, 'html.parser')
		job_elements = soup.select("a[href*='/vacancy/']")
		for element in job_elements[3:]:
			db_data = s.query(Jobs.title, Jobs.company).all()
			url = 'https://grc.ua/vacancy/' + element['href'].split('y/')[1].split('?')[0]
			title = element.text.strip()
			company = ''
			company_element = element.parent.parent.parent.parent.parent.parent.findChildren('a', class_= 'bloko-link bloko-link_secondary')[0]
			if company_element:
				company = company_element.text
			salary = 0
			salary_element = element.parent.parent.parent.parent.parent.parent.find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
			if salary_element:
				salary = int(''.join(i for i in salary_element.text.split('–')[-1] if i.isdigit()))
				if 'руб' in salary_element.text.lower():
					salary *= 0.36
				elif 'usd' in salary_element.text.lower():
					salary *= 27
				elif 'eur' in salary_element.text.lower():
					salary *= 32
			if not any((title + ' ' + company) in ' '.join(row) for row in db_data):
				self.grc_get_description(url, title, company, salary)
				
	def grc_get_description(self, url, title, company, salary):
		response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(response.content, 'html.parser')
		img_src = '/static/logo.svg'
		img_element = soup.find('img', class_= 'vacancy-company-logo__image')
		if img_element:
			img_src = img_element['src']
		description_element = soup.find('div', class_= 'vacancy-branded-user-content')
		if description_element:
			description_text = description_element.decode_contents()
		else:
			description_text = soup.find_all('div', class_= 'vacancy-section')[0].decode_contents()
		exp_element = soup.select('span[data-qa="vacancy-experience"]')[0].text[0]
		exp_in_info = int(''.join(i for i in exp_element.split('–')[0] if i.isdigit()) or 0)
		exp_in_description = get_exp(description_text)
		exp_final = max(exp_in_description, exp_in_info)
		print(url, title, company, salary, exp_final, self.job_id)
		self.add_job(url, title, company, salary, description_text, img_src, exp_final)		
			
	def add_job(self, url, title, company, salary, description_text, img_src, exp_final):
		new_job = Jobs(url=url, title=title, company=company, salary=salary, description=description_text, img=img_src, id=self.job_id, exp=exp_final)
		print(url, title, exp_final, salary)
		s.add(new_job)
		#s.commit()
		self.job_id += 1

	
def main():
	parser = Parser()
	parser.djinni_get_urls()	

if __name__ == '__main__':
	main()
