import requests
import re
from bs4 import BeautifulSoup
from modules.helpers import *
from modules.alchemy import *

def get_urls():
	job_id = get_last_id()
	response = requests.get('https://www.work.ua/jobs-it/?advs=1&employment=76&nosalary=1&page=' + str(i))
	soup = BeautifulSoup(response.content, 'html.parser')
	job_elements = soup.find_all('h2')
	for element in job_elements[:-6]:
		db_data = get_jobs()
		url = 'https://www.work.ua' + element.findChildren('a')[0]["href"]
		title = clean_title(element.findChildren('a')[0].text)
		company = ''
		company_element = element.find_next_sibling('div', class_= "add-top-xs")
		if company_element:
			company = company_element.text.split('·')[0].split(',')[0].strip()
		if not any((title + ' ' + company) in ' '.join(row) for row in db_data):
			get_description(url, title, company, job_id)
			job_id += 1
				
def get_description(url, title, company, job_id):
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
	add_job(url, title, company, salary, description_text, img_src, exp_final, job_id)