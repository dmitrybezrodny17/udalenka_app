import requests
import re
from bs4 import BeautifulSoup
from modules.helpers import *
from modules.alchemy import *

def get_urls():
	job_id = get_last_id()
	response = requests.get('https://jobs.dou.ua/vacancies/?remote', headers={'User-Agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(response.content, 'html.parser')
	job_elements = soup.find_all('a', class_= 'vt')
	for element in job_elements:
		db_data = get_jobs()
		url = element["href"].split('?')[0]
		title = element.text.strip()
		company_element = element.find_next_sibling('strong').findChildren('a', class_ = 'company')[0]
		company = company_element.text.strip()
		salary = 0
		salary_element = element.find_next_sibling('span', class_= "salary")
		if salary_element:
			salary = int(salary_element.text.split('$')[1].split('–')[-1])*27
		if not any((title + ' ' + company) in ' '.join(row) for row in db_data):
			get_description(url, title, company, salary, job_id)
			job_id += 1
				
def get_description(url, title, company, salary, job_id):
	page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(page.content, 'html.parser')
	img_src = '/static/logo.svg'
	img_element = soup.find('a', class_= 'logo').findChildren('img')[0]
	if img_element:
		img_src = img_element['src']
	description_element = soup.find('div', class_= 'l-vacancy')
	description_text = description_element.decode_contents().replace('	', '').replace('\n', '').split('<script>')[0].split('</span></div>')[1]
	exp_final = get_exp(description_text)
	add_job(url, title, company, salary, description_text, img_src, exp_final, job_id)