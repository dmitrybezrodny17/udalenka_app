import requests
from bs4 import BeautifulSoup
from modules.helpers import *
from modules.alchemy import *

def get_urls():
	job_id = get_last_id()
	response = requests.get('https://djinni.co/jobs/?remote_type=remote')
	soup = BeautifulSoup(response.content, 'html.parser')
	job_elements = soup.find_all('a', class_= 'profile')
	for element in job_elements:
		db_data = get_jobs()
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
			get_description(url, title, company, salary, job_id)
			job_id += 1
				
def get_description(url, title, company, salary, job_id):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	img_src = '/static/logo.svg'
	description_element = soup.find_all('div', class_= 'profile-page-section')[1]
	description_text = description_element.decode_contents().replace('\n\r', '</br>').replace('\n', '</br>')
	exp_element = soup.find('div', class_= 'list-jobs__details__info')
	exp_in_info = 0
	if exp_element and not 'без досв' in exp_element.text:
		exp_in_info = int(exp_element.text.split(' р')[0].split('·')[-1])
	exp_in_description = get_exp(description_text)
	exp_final = max(exp_in_description, exp_in_info)
	add_job(url, title, company, salary, description_text, img_src, exp_final, job_id)
	
