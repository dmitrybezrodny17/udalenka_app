import requests
from bs4 import BeautifulSoup
from modules.helpers import *
from modules.alchemy import *

def get_urls():
	job_id = get_last_id()
	page = requests.get('https://ua.jooble.org/SearchResult?date=8&loc=2')
	response = BeautifulSoup(page.content, 'html.parser')
	job_elements = response.find_all('h2', class_= 'JobCard_position_heading__15V35')
	for element in job_elements:
		db_data = get_jobs()
		url = 'https://ua.jooble.org/jdp/' + element.findChildren('a')[0]['href'].split('/')[4]
		if 'ckey' in url:
			break
		title = element.text.replace('(Удаленная работа)', '').strip()
		company = ''
		company_element = element.parent.parent.select('div[class*="GoodEmployerWidget_company"]')[0]
		if company_element:
			company = company_element.text
		salary = 0
		salary_element = element.parent.parent.select('p[class*="JobCard_salary"]')[0]
		if salary_element:
			if 'день' in salary_element.text:
				salary = int(salary_element.text.replace('грн', '').replace('день', '').replace('/','').replace(' ', '').split('-')[-1].strip())*30
			elif '$' in salary_element.text:
				salary = int(salary_element.text.replace(' ', '').replace('$', '').split('-')[-1].strip())*27
			elif '€' in salary_element.text:
				salary = int(salary_element.text.replace(' ', '').replace('€', '').split('-')[-1].strip())*32
			elif 'грн' in salary_element.text:
				salary = salary_element.text.replace(' ', '').replace('грн', '').split('-')[-1].strip()
		if not any((title + ' ' + company) in ' '.join(row) for row in db_data):
			print(url, title, company, salary, job_id)
			get_description(url, title, company, salary, job_id)
			job_id += 1
				
def get_description(url, title, company, salary, job_id):
	headers = requests.utils.default_headers()
	headers.update({
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
	})
	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.content, 'html.parser')
	img_src = '/static/logo.svg'
	description_element = soup.select('div[class*="JobDescriptionCard_content"]')[0]
	description_text = description_element.decode_contents().replace('\n\r', '</br>').replace('\n', '</br>')
	exp_final = get_exp(description_text)
	add_job(url, title, company, salary, description_text, img_src, exp_final, job_id)
	