import requests
from bs4 import BeautifulSoup
from modules.helpers import *
from modules.alchemy import *

def get_urls():
	job_id = get_last_id()
	response = requests.get('https://grc.ua/search/vacancy?clusters=true&enable_snippets=true&items_on_page=100&no_magic=true&order_by=publication_time&search_period=7&text=&area=5&specialization=1&schedule=remote', headers={'User-Agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(response.content, 'html.parser')
	job_elements = soup.select("a[href*='/vacancy/']")
	for element in job_elements[3:]:
		db_data = get_jobs()
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
			get_description(url, title, company, salary, job_id)
			job_id += 1

def get_description(url, title, company, salary, job_id):
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
	add_job(url, title, company, salary, description_text, img_src, exp_final, job_id) 