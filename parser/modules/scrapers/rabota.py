import requests
from bs4 import BeautifulSoup
from modules.helpers import *
from modules.alchemy import *

def get_urls():
	job_id = get_last_id()
	response = requests.get('https://api.rabota.ua/vacancy/search?count=10&parentId=1&scheduleId=3')
	for new_job in response.json()['documents']:
		db_data = get_jobs()
		title = new_job['name']
		company = new_job['companyName']
		if not any((title + ' ' + company) in ' '.join(row) for row in db_data):
			get_description(title, company, new_job['id'], job_id)
			job_id += 1

def get_description(title, company, jid, job_id):
	response = requests.get('https://api.rabota.ua/vacancy?id=' + str(jid))
	url = 'https://rabota.ua/company' + str(response.json()['notebookId']) + '/vacancy' + str(response.json()['id'])
	img_src = 'https://company-logo-frankfurt.rabota.ua/cdn-cgi/image/w=250/' + response.json()['logo']
	description_text = response.json()['description']
	exp_final = get_exp(description_text)
	salary = max(response.json()['salaryFrom'], response.json()['salaryTo'], response.json()['salary'])
	add_job(url, title, company, salary, description_text, img_src, exp_final, job_id)
