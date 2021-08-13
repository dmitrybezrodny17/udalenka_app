from bs4 import BeautifulSoup
import requests
import psycopg2
import time
import re
import base64

class work_ua:
	def __init__(self):
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from jop2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://www.work.ua/jobs-it/?advs=1&employment=76')
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('h2')
		urls = []
		for n in h2s[:-2]:
			try:
				urls.append('https://www.work.ua' + n.findChildren('a')[0]["href"])
			except:
				pass
		for url in urls:
			if not any(word[0] == (url) for word in db_urls):
				self.get_desc(url)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company, links from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_element = soup.find('h1', class_= "add-top-sm")
			title_text = title_element.text
			company_element = soup.find_all('p', class_= "text-indent text-muted add-top-sm")[-1]
			company_text = company_element.findChildren('a')[0].text
			full_text = title_text + ' ' + company_text
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'https://www.work.ua' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				try:
					img = soup.find('img', class_= "logo-job")
					img_src = img['src']
				except Exception as e:
					img_src = '/static/logo.svg'
				description_element = soup.find('div', id= "job-description")
				description_text = description_element.decode_contents()
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				exp_element = soup.find('span', title = "Умови й вимоги").find_parent('p')
				try:
					exp = int(re.search(r'роботи від(.+?) ро', exp_element.text).group(1))
				except Exception:
					exp = 0
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text, description_text, img_src, job_id, exp, url)
				)
				self.conn.commit()
		except Exception as e:
			print(e)
			return
	
class rabota_ua:
	def __init__(self):
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from JOP2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://rabota.ua/zapros/all/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0?scheduleId=3&parentId=1')
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('h2')
		urls = []
		for n in h2s[1:]:
			urls.append('https://rabota.ua' + n.findChildren('a')[0]["href"])
		for url in urls:
			if not any(word[0] == (url) for word in db_urls):
				self.get_desc(url)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company, links from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_element = soup.find('h1')
			title_text = title_element.text
			title = soup.find('title')
			company_text = re.search(r'"vacancy_CompanyName":"(.+?)","vacancy_Description":"', page.content.decode('utf-8'))
			full_text = title_text + ' ' + company_text.group(1)
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'https://rabota.ua/' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				try:
					img = re.search(r',"vacancy_Logo":"(.+?)","vacancy_IsVip":', page.content.decode('utf-8'))
					img_src = re.search(r',","cloudCompanyLogos":"(.+?)","scriptVer":', page.content.decode('utf-8')) + '/cdn-cgi/image/w=250/' + img
				except Exception as e:
					try: 
						img = re.search(r'"@type":(.+?)"},"jobLocation":{"@type":', page.content.decode('utf-8'))
						img_src = img.group(1).split('"logo":"')[-1]
					except Exception as e:
						img_src = img_src = '/static/logo.svg'
				try:
					description = re.search(r'"},"description":"(.+?)","vacancy_NotebookId"', page.content.decode('utf-8'))
					description_text = description.group(1).split('vacancy_Description":"')[-1].replace('\\t','').replace('\\n','').replace('\\"','"')
				except Exception as e:
					description = re.search(r'"vacancy_Description":"(.+?)","vacancy_NotebookId"', page.content.decode('utf-8'))				
					description_text = description.group(1).split('vacancy_Description":"')[-1].replace('\\t','').replace('\\n','').replace('\\"','"')
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				desc_list = list(description_text.replace("<li>", "<p>").replace("<span", "<p>").replace("<br/>", "<p>").replace('&nbsp;', ' ').replace(u'\xa0', u' ').split("<p>"))
				try:
					y1 = ['1+ ', '1 y', '1 г', '1 л', '1 р', '1+ г', '1+ л', '1+ р', '1-го го', 'не менее одного', 'не менее год', 'более одного', 'один год', '1-2', '1-3', '1 to 2', '1 to 3', '1 до 2', '1 до 3', 'half a year', 'полгода', 'півроку']
					y2 = ['2+ ', '2 y', '2 г', '2 л', '2 р', '2+ г', '2+ л', '2+ р', '2-х р', '2-х л', '2х л', '2х р', 'двох', 'двух', '2-3', '2-4', '2-5', '2 to 3', '2 to 4', '2 to 5', '2 до 3', '2 до 4', '2 до 5', '1.5', '1,5', 'полтора', 'півтора']
					y3 = ['3+ ', '3 y', '3 г', '3 л', '3 р', '3+ г', '3+ л', '3+ р', '3-х р', '3-х л', '3х л', '3х р', 'трьох', 'трёх', 'трех', '3-4', '3-5', '3-6', '3 to 4', '3 to 5', '3 to 6', '3 до 4', '3 до 5', '3 до 6', '2.5', '2,5']
					y4 = ['4+ ', '4 y', '4 г', '4 л', '4 р', '4+ г', '4+ л', '4+ р', '4-х р', '4-х л', '4х л', '4х р', '4-5', '4-6', '4 to 5', '4 to 6', '4 до 5', '4 до 6', '3.5', '3,5']
					y5 = ['5+ ', '5 y', '5 г', '5 л', '5 р', '5+ г', '5+ л', '5+ р', 'пяти']
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
						else:
							exp.append(0)
				except Exception as e:
					print(e)
				exp_final = max(exp)
				print(url, title_text, exp_final)
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text.group(1), description_text, img_src, job_id, exp_final, url)
				)
				self.conn.commit()
		except Exception as e:
			print(e) 
			return
			
class dou_ua:
	def __init__(self):	
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from JOP2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://jobs.dou.ua/vacancies/?remote', headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('a', class_= 'vt')
		urls = []
		for n in h2s:
			urls.append(n["href"])
		for url in urls:
			url_clean = url.split('?')[0]
			if not any(word[0] == (url_clean) for word in db_urls):
				self.get_desc(url_clean)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company, links from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_element = soup.find('h1', class_= "g-h2")
			title_text = title_element.text
			company_element = soup.find('div', class_= "l-n").findChildren('a')[0]
			company_text = company_element.text
			full_text = title_text + ' ' + company_text
			try:
				img = soup.find('a', class_= 'logo').findChildren('img')[0]
				img_src = img['src']
			except Exception as e:
				img_src = '/static/logo.svg'
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'https://jobs.dou.ua/' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				description_element = soup.find('div', class_= 'l-vacancy')
				description_text = description_element.decode_contents().replace('	', '').replace('\n', '').split('<script>')[0].split('</span></div>')[1]
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				desc_list = list(description_text.replace("<li>", "<p>").replace("<span", "<p>").replace("<br/>", "<p>").replace('&nbsp;', ' ').replace(u'\xa0', u' ').split("<p>"))
				try:
					y1 = ['1+ ', '1 y', '1 г', '1 л', '1 р', '1+ г', '1+ л', '1+ р', '1-го го', 'не менее одного', 'не менее год', 'более одного', 'один год', '1-2', '1-3', '1 to 2', '1 to 3', '1 до 2', '1 до 3', 'half a year', 'полгода', 'півроку']
					y2 = ['2+ ', '2 y', '2 г', '2 л', '2 р', '2+ г', '2+ л', '2+ р', '2-х р', '2-х л', '2х л', '2х р', 'двох', 'двух', '2-3', '2-4', '2-5', '2 to 3', '2 to 4', '2 to 5', '2 до 3', '2 до 4', '2 до 5', '1.5', '1,5', 'полтора', 'півтора']
					y3 = ['3+ ', '3 y', '3 г', '3 л', '3 р', '3+ г', '3+ л', '3+ р', '3-х р', '3-х л', '3х л', '3х р', 'трьох', 'трёх', 'трех', '3-4', '3-5', '3-6', '3 to 4', '3 to 5', '3 to 6', '3 до 4', '3 до 5', '3 до 6', '2.5', '2,5']
					y4 = ['4+ ', '4 y', '4 г', '4 л', '4 р', '4+ г', '4+ л', '4+ р', '4-х р', '4-х л', '4х л', '4х р', '4-5', '4-6', '4 to 5', '4 to 6', '4 до 5', '4 до 6', '3.5', '3,5']
					y5 = ['5+ ', '5 y', '5 г', '5 л', '5 р', '5+ г', '5+ л', '5+ р', 'пяти']
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
						else:
							exp.append(0)
				except Exception as e:
					print(e)
				exp_final = max(exp)
				print(url, title_text, exp_final)
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text, description_text, img_src, job_id, exp_final, url)
				)
				self.conn.commit() 
		except Exception as e:
			print(e)
			return
	
class djinni_co:
	def __init__(self):	
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from JOP2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://djinni.co/jobs2/?location=remote')
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('a', class_= 'profile')
		urls = []
		for n in h2s:
			urls.append('https://djinni.co' + n['href'])
		for url in urls:
			if not any(word[0] == (url) for word in db_urls):
				self.get_desc(url)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company, links from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_element = soup.find('h1')
			title_text = ' '.join(title_element.text.strip().split())
			company_element = soup.find('div', class_= 'list-jobs__details__info').findChildren('a')[1]
			company_text = company_element.text
			full_text = title_text + ' ' + company_text
			img_src = '/static/logo.svg'
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'https://djinni.co/' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				description_element = soup.find_all('div', class_= 'profile-page-section')[1]
				description_text = description_element.decode_contents().replace('\n\r', '</br>').replace('\n', '</br>')
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				exp_element = soup.find('div', class_= 'list-jobs__details__info')
				try:
					exp = re.search(r'· (.+?) р', exp_element.text).group(1)
				except Exception:
					try:
						exp = re.search(r'· (.+?) р', exp_element.text).group(1)
					except Exception:
						exp = 0
				print(url, title_text, exp)
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text, description_text, img_src, job_id, exp, url)
				)
				self.conn.commit() 
		except Exception as e:
			print(e)
			return
			
class grc_ua:
	def __init__(self):	
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from JOP2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://grc.ua/search/vacancy?area=5&clusters=true&enable_snippets=true&no_magic=true&schedule=remote&specialization=1&order_by=publication_time', headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('a', class_= 'bloko-link')
		urls = []
		for n in h2s:
			if 'vacancy' in n['href']:
				urls.append('https://grc.ua/vacancy/' + n['href'].split('/')[4])
			else:
				pass
		for url in urls:
			if not any(word[0] == (url) for word in db_urls):
				self.get_desc(url)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company, links from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_element = soup.find('h1')
			title_text = title_element.text.strip()
			company_element = soup.find('div', class_= 'vacancy-company__details')
			company_text = company_element.text
			full_text = title_text + ' ' + company_text
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'https://grc.ua/' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				try:
					img_element = soup.find('img', class_= 'vacancy-company-logo__image')
					img_src = img_element['src']
				except Exception as e:
					img_src = '/static/logo.svg'
				try:
					description_element = soup.find('div', class_= 'l-paddings b-vacancy-desc')
					description_text = description_element.decode_contents()
				except Exception as e:
					description_element = soup.find('div', class_= 'vacancy-section')
					description_text = description_element.decode_contents()
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				exp_element = soup.select('span[data-qa="vacancy-experience"]')[0].text[0]
				if (exp_element == 'н'):
					exp = 0
				elif (exp_element == 'б'):
					exp = 6
				else:
					exp = int(exp_element)
				print(url, title_text, exp)
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text, description_text, img_src, job_id, exp, url)
				)
				self.conn.commit() 
		except Exception as e:
			print(e)
			return
						
class freelancehunt_com:
	def __init__(self):	
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from JOP2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://t.me/s/FreelancehuntJobs', headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('a', class_= 'tgme_widget_message_inline_button url_button')
		urls = []
		for n in h2s:
			urls.append('https://freelancehunt.com/' + n['href'].replace('?', '/').split('/')[3] + '/' + n['href'].replace('?', '/').split('/')[4] + '/' + n['href'].replace('?', '/').split('/')[5])
		for url in urls:
			if not any(word[0] == (url) for word in db_urls):
				self.get_desc(url)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
		time.sleep(10)
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_text = str(soup.title).replace('> ', '|').replace('Вакансия ', '|').replace(' в ', '|').replace(' ≡', '|').split('|')[1]
			company_text = str(soup.title).split(' ≡')[0].split(' в ')[-1]
			full_text = title_text + ' ' + company_text
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'https://freelancehunt.com/' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				try:
					img = soup.find('div', class_= 'company-logo-container container-size-95').findChildren('img')[0]
					img_src = img['src']
				except Exception as e:
					img_src = '/static/logo.svg'
				description_element = soup.find('div', class_= 'well description linkify-marker img-responsive-container')
				description_text = description_element.decode_contents()
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				desc_list = list(description_text.replace("<li>", "<p>").replace("<span", "<p>").replace("<br/>", "<p>").replace('&nbsp;', ' ').replace(u'\xa0', u' ').split("<p>"))
				try:
					y1 = ['1+ ', '1 y', '1 г', '1 л', '1 р', '1+ г', '1+ л', '1+ р', '1-го го', 'не менее одного', 'не менее год', 'более одного', 'один год', '1-2', '1-3', '1 to 2', '1 to 3', '1 до 2', '1 до 3', 'half a year', 'полгода', 'півроку']
					y2 = ['2+ ', '2 y', '2 г', '2 л', '2 р', '2+ г', '2+ л', '2+ р', '2-х р', '2-х л', '2х л', '2х р', 'двох', 'двух', '2-3', '2-4', '2-5', '2 to 3', '2 to 4', '2 to 5', '2 до 3', '2 до 4', '2 до 5', '1.5', '1,5', 'полтора', 'півтора']
					y3 = ['3+ ', '3 y', '3 г', '3 л', '3 р', '3+ г', '3+ л', '3+ р', '3-х р', '3-х л', '3х л', '3х р', 'трьох', 'трёх', 'трех', '3-4', '3-5', '3-6', '3 to 4', '3 to 5', '3 to 6', '3 до 4', '3 до 5', '3 до 6', '2.5', '2,5']
					y4 = ['4+ ', '4 y', '4 г', '4 л', '4 р', '4+ г', '4+ л', '4+ р', '4-х р', '4-х л', '4х л', '4х р', '4-5', '4-6', '4 to 5', '4 to 6', '4 до 5', '4 до 6', '3.5', '3,5']
					y5 = ['5+ ', '5 y', '5 г', '5 л', '5 р', '5+ г', '5+ л', '5+ р', 'пяти']
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
						else:
							exp.append(0)
				except Exception as e:
					print(e)
				exp_final = max(exp)
				print(url, title_text, exp_final)
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text, description_text, img_src, job_id, exp_final, url)
				)
				self.conn.commit() 
		except Exception as e:
			print(e)
			return
		
class jooble_org:
	def __init__(self):	
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from JOP2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://ua.jooble.org/SearchResult?date=8&loc=2&p=2')
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('h2', class_= 'JobCard_position_heading__15V35')
		urls = []
		for n in h2s:
			a = n.findChildren('a')[0]['href']
			if '/jdp/' in a:
				urls.append('https://ua.jooble.org/jdp/' + a.split('/')[4])
			else:
				pass
		for url in urls:
			if not any(word[0] == (url) for word in db_urls):
				self.get_desc(url)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company, links from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_element = soup.find('h1')
			title_text = title_element.text.strip()
			company_element = soup.select('p[class*="GoodEmployerWidget_company"]')[0]
			company_text = company_element.text
			full_text = title_text + ' ' + company_text
			img_src = '/static/logo.svg'
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'jooble.org' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				description_element = soup.select('div[class*="JobDescriptionCard_content"]')[0]
				description_text = description_element.decode_contents().replace('\n\r', '</br>').replace('\n', '</br>')
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				desc_list = list(description_text.replace("<li>", "<p>").replace("<span", "<p>").replace("<br/>", "<p>").replace('&nbsp;', ' ').replace(u'\xa0', u' ').split("<p>"))
				try:
					y1 = ['1+ ', '1 y', '1 г', '1 л', '1 р', '1+ г', '1+ л', '1+ р', '1-го го', 'не менее одного', 'не менее год', 'более одного', 'один год', '1-2', '1-3', '1 to 2', '1 to 3', '1 до 2', '1 до 3', 'half a year', 'полгода', 'півроку']
					y2 = ['2+ ', '2 y', '2 г', '2 л', '2 р', '2+ г', '2+ л', '2+ р', '2-х р', '2-х л', '2х л', '2х р', 'двох', 'двух', '2-3', '2-4', '2-5', '2 to 3', '2 to 4', '2 to 5', '2 до 3', '2 до 4', '2 до 5', '1.5', '1,5', 'полтора', 'півтора']
					y3 = ['3+ ', '3 y', '3 г', '3 л', '3 р', '3+ г', '3+ л', '3+ р', '3-х р', '3-х л', '3х л', '3х р', 'трьох', 'трёх', 'трех', '3-4', '3-5', '3-6', '3 to 4', '3 to 5', '3 to 6', '3 до 4', '3 до 5', '3 до 6', '2.5', '2,5']
					y4 = ['4+ ', '4 y', '4 г', '4 л', '4 р', '4+ г', '4+ л', '4+ р', '4-х р', '4-х л', '4х л', '4х р', '4-5', '4-6', '4 to 5', '4 to 6', '4 до 5', '4 до 6', '3.5', '3,5']
					y5 = ['5+ ', '5 y', '5 г', '5 л', '5 р', '5+ г', '5+ л', '5+ р', 'пяти']
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
						else:
							exp.append(0)
				except Exception as e:
					print(e)
				exp_final = max(exp)
				print(url, title_text, exp_final)
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text, description_text, img_src, job_id, exp_final, url)
				)
				self.conn.commit() 
		except Exception as e:
			print(e)
			return
				
class trud_ua:
	def __init__(self):	
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from JOP2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://trud.ua/jobs/list/filter_show/state/schedule/udalennaia-rabota.html')
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('a', class_= 'item-link')
		urls = []
		for n in h2s:
			urls.append('https://trud.ua' + n['href'])
		for url in list(set(urls)):
			if not any(word[0] == (url) for word in db_urls):
				self.get_desc(url)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company, links from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_element = soup.find('h1')
			title_text = title_element.text.strip().replace('Вакансія ', '')
			company_element = soup.find('a', class_= 'blc-un')
			company_text = company_element.text
			full_text = title_text + ' ' + company_text
			img_src = '/static/logo.svg'
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'https://trud.ua/' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				description_element = soup.find_all('div', class_= 'info-block')[2]
				description_text = description_element.decode_contents().replace('\n\r', '</br>').replace('\n', '</br>')
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				desc_list = list(description_text.replace("<li>", "<p>").replace("<span", "<p>").replace("<br/>", "<p>").replace('&nbsp;', ' ').replace(u'\xa0', u' ').split("<p>"))
				exp = []
				if soup(text=' Від 1 до 3х років '):
					exp.append(1)
				elif soup(text=' Від 3х до 6 років '):
					exp.append(3)
				elif soup(text=' Більше 6 років '):
					exp.append(6)
				else:
					exp.append(0)
				try:
					y1 = ['1+ ', '1 y', '1 г', '1 л', '1 р', '1+ г', '1+ л', '1+ р', '1-го го', 'не менее одного', 'не менее год', 'более одного', 'один год', '1-2', '1-3', '1 to 2', '1 to 3', '1 до 2', '1 до 3', 'half a year', 'полгода', 'півроку']
					y2 = ['2+ ', '2 y', '2 г', '2 л', '2 р', '2+ г', '2+ л', '2+ р', '2-х р', '2-х л', '2х л', '2х р', 'двох', 'двух', '2-3', '2-4', '2-5', '2 to 3', '2 to 4', '2 to 5', '2 до 3', '2 до 4', '2 до 5', '1.5', '1,5', 'полтора', 'півтора']
					y3 = ['3+ ', '3 y', '3 г', '3 л', '3 р', '3+ г', '3+ л', '3+ р', '3-х р', '3-х л', '3х л', '3х р', 'трьох', 'трёх', 'трех', '3-4', '3-5', '3-6', '3 to 4', '3 to 5', '3 to 6', '3 до 4', '3 до 5', '3 до 6', '2.5', '2,5']
					y4 = ['4+ ', '4 y', '4 г', '4 л', '4 р', '4+ г', '4+ л', '4+ р', '4-х р', '4-х л', '4х л', '4х р', '4-5', '4-6', '4 to 5', '4 to 6', '4 до 5', '4 до 6', '3.5', '3,5']
					y5 = ['5+ ', '5 y', '5 г', '5 л', '5 р', '5+ г', '5+ л', '5+ р', 'пяти']
					exps = ['exp', 'досв', 'опыт', 'years in']
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
						else:
							exp.append(0)
				except Exception as e:
					print(e)
				exp_final = max(exp)
				print(url, title_text, exp_final)
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text, description_text, img_src, job_id, exp_final, url)
				)
				self.conn.commit() 	
		except Exception as e:
			print(e)
			return		

class superjob_ru:
	def __init__(self):	
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from JOP2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://www.superjob.ru/vakansii/na-domu.html?geo%5Bc%5D%5B0%5D=9&click_from=facet')
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('div', class_= 'f-test-search-result-item')
		urls = []
		for n in h2s:
			try:
				clear = n.findChildren('a')[0]['href']
				if 'vakansii' in clear:
					urls.append('https://www.superjob.ru' + clear)
				else:
					pass
			except Exception as e:
				pass
		for url in urls:
			if not any(word[0] == (url) for word in db_urls):
				self.get_desc(url)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company, links from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_element = soup.find('h1')
			title_text = title_element.text.strip().replace('Вакансія ', '')
			company_element = soup.find_all('h2')[2]
			company_text = company_element.text
			full_text = title_text + ' ' + company_text
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'https://www.superjob.ru/' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				description_element = soup.find('span', class_= '_1h3Zg _2LeqZ _1TK9I _2hCDz _2ZsgW _2SvHc')
				try:
					img_src = 'https:' + company_element.find_parent('a').find_previous_sibling('img')['src']
				except Exception as e:
					img_src = '/static/logo.svg'
				description_text = description_element.decode_contents().replace('\n\r', '</br>').replace('\n', '</br>')
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				desc_list = list(description_text.replace("<li>", "<p>").replace("<span", "<p>").replace("<br/>", "<p>").replace('&nbsp;', ' ').replace(u'\xa0', u' ').split("<p>"))
				exp = []
				if soup(text='Опыт работы от 3 лет'):
					exp.append(3)
				elif soup(text='Опыт работы от 1 года'):
					exp.append(1)
				elif soup(text='Опыт работы от 6 лет'):
					exp.append(6)
				else:
					exp.append(0)
				try:
					y1 = ['1+ ', '1 y', '1 г', '1 л', '1 р', '1+ г', '1+ л', '1+ р', '1-го го', 'не менее одного', 'не менее год', 'более одного', 'один год', '1-2', '1-3', '1 to 2', '1 to 3', '1 до 2', '1 до 3', 'half a year', 'полгода', 'півроку']
					y2 = ['2+ ', '2 y', '2 г', '2 л', '2 р', '2+ г', '2+ л', '2+ р', '2-х р', '2-х л', '2х л', '2х р', 'двох', 'двух', '2-3', '2-4', '2-5', '2 to 3', '2 to 4', '2 to 5', '2 до 3', '2 до 4', '2 до 5', '1.5', '1,5', 'полтора', 'півтора']
					y3 = ['3+ ', '3 y', '3 г', '3 л', '3 р', '3+ г', '3+ л', '3+ р', '3-х р', '3-х л', '3х л', '3х р', 'трьох', 'трёх', 'трех', '3-4', '3-5', '3-6', '3 to 4', '3 to 5', '3 to 6', '3 до 4', '3 до 5', '3 до 6', '2.5', '2,5']
					y4 = ['4+ ', '4 y', '4 г', '4 л', '4 р', '4+ г', '4+ л', '4+ р', '4-х р', '4-х л', '4х л', '4х р', '4-5', '4-6', '4 to 5', '4 to 6', '4 до 5', '4 до 6', '3.5', '3,5']
					y5 = ['5+ ', '5 y', '5 г', '5 л', '5 р', '5+ г', '5+ л', '5+ р', 'пяти']
					exps = ['exp', 'досв', 'опыт', 'years in']
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
						else:
							exp.append(0)
				except Exception as e:
					print(e)
				exp_final = max(exp)
				print(url, title_text, exp_final)
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text, description_text, img_src, job_id, exp_final, url)
				)
				self.conn.commit() 				
		except Exception as e:
			print(e)
			return
	
class jobs_ua:
	def __init__(self):	
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from JOP2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://jobs.ua/vacancy?work_graph=4')
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('a', class_= 'b-vacancy__top__title js-item_title')
		urls = []
		for n in h2s:
			urls.append(n['href'])
		for url in urls:
			if not any(word[0] == (url) for word in db_urls):
				self.get_desc(url)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company, links from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_element = soup.find('h1')
			title_text = title_element.text.strip()
			company_element = soup.find('span', class_='for_print').find_previous_sibling('a')
			company_text = company_element.text
			full_text = title_text + ' ' + company_text
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'https://jobs.ua/' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				img_src = '/static/logo.svg'
				description_element = soup.find('div', class_= 'b-vacancy-full__block b-text js-phone-replace')
				description_text = description_element.decode_contents().replace('\n\r', '</br>').replace('\n', '</br>').replace('<h2 class="b-vacancy-full__block-title"><span>Опис вакансії</span></h2>', '')
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				desc_list = list(description_text.replace("<li>", "<p>").replace("<span", "<p>").replace("<br/>", "<p>").replace('&nbsp;', ' ').replace(u'\xa0', u' ').split("<p>"))
				exp = []
				if soup(text='від двох років'):
					exp.append(2)
				elif soup(text='від року'):
					exp.append(1)
				elif soup(text="від п'яти років"):
					exp.append(5)
				else:
					exp.append(0)
				try:
					y1 = ['1+ ', '1 y', '1 г', '1 л', '1 р', '1+ г', '1+ л', '1+ р', '1-го го', 'не менее одного', 'не менее год', 'более одного', 'один год', '1-2', '1-3', '1 to 2', '1 to 3', '1 до 2', '1 до 3', 'half a year', 'полгода', 'півроку']
					y2 = ['2+ ', '2 y', '2 г', '2 л', '2 р', '2+ г', '2+ л', '2+ р', '2-х р', '2-х л', '2х л', '2х р', 'двох', 'двух', '2-3', '2-4', '2-5', '2 to 3', '2 to 4', '2 to 5', '2 до 3', '2 до 4', '2 до 5', '1.5', '1,5', 'полтора', 'півтора']
					y3 = ['3+ ', '3 y', '3 г', '3 л', '3 р', '3+ г', '3+ л', '3+ р', '3-х р', '3-х л', '3х л', '3х р', 'трьох', 'трёх', 'трех', '3-4', '3-5', '3-6', '3 to 4', '3 to 5', '3 to 6', '3 до 4', '3 до 5', '3 до 6', '2.5', '2,5']
					y4 = ['4+ ', '4 y', '4 г', '4 л', '4 р', '4+ г', '4+ л', '4+ р', '4-х р', '4-х л', '4х л', '4х р', '4-5', '4-6', '4 to 5', '4 to 6', '4 до 5', '4 до 6', '3.5', '3,5']
					y5 = ['5+ ', '5 y', '5 г', '5 л', '5 р', '5+ г', '5+ л', '5+ р', 'пяти']
					exps = ['exp', 'досв', 'опыт', 'years in']
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
						else:
							exp.append(0)
				except Exception as e:
					print(e)
				exp_final = max(exp)
				print(url, title_text, exp_final)
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text, description_text, img_src, job_id, exp_final, url)
				)
				self.conn.commit() 	
		except Exception as e:
			return		
	
class trud_com:
	def __init__(self):	
		self.conn = psycopg2.connect(dbname='***', user='***', 
						password='***', host='***')
		self.cur = self.conn.cursor() 
		
	def get_urls(self):
		self.cur.execute("SELECT URL from JOP2")
		db_urls = self.cur.fetchall()
		page = requests.get('https://ua.trud.com/jobs/it_kompyutery_internet/schedule_f/udalennaya_rabota/', headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(page.content, 'html.parser')
		h2s = soup.find_all('a', class_= 'item-link')
		urls = []
		for n in h2s:
			clear_n = 'https://ua.trud.com/ua/search/item/item_id/' + str(base64.b64decode(n['hval'])).split('/')[7]
			if not (clear_n) in urls:
				urls.append(clear_n)
		for url in urls:
			if not any(word[0] == (url) for word in db_urls):
				self.get_desc(url)
			else:
				pass
		self.conn.close()	
				
	def get_desc(self, url):
		self.cur.execute("SELECT title, company, links from jop2")
		db_desc = self.cur.fetchall()
		joiner = " ".join
		jobs = [joiner(words) for words in db_desc]
		page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			title_element = soup.find('h1')
			title_text = title_element.text.strip()
			company_element = soup.find('div', class_= 'ap__em')
			try:
				child = company_element.findChildren('a')[0]
				company_text = child.text
			except Exception as e:
				company_text = company_element.text
			full_text = title_text + ' ' + company_text
			if any(full_text in x for x in jobs):
				for i in jobs:
					old_links = i.split(' ')[-1] 
					if 'https://ua.trud.com/' not in old_links and full_text in i:
						new_links = old_links + ',' + url
						self.cur.execute(
							"UPDATE jop2 SET links = '{0}' WHERE links = '{1}'".format(new_links, old_links)
						)
						self.conn.commit()
						break
					else:
						pass
			else:
				img_src = '/static/logo.svg'
				description_element = soup.find('div', class_= 'ap__d')
				description_text = description_element.decode_contents().replace(' <div class="ap__d_t">Опис вакансії</div> ', '')
				self.cur.execute("SELECT date, id FROM jop2 ORDER BY date DESC LIMIT 1")
				dates_and_ids = self.cur.fetchall()
				job_id = dates_and_ids[0][1] + 1
				desc_list = list(description_text.replace("<li>", "<p>").replace("<span", "<p>").replace("<br/>", "<p>").replace('&nbsp;', ' ').replace(u'\xa0', u' ').split("<p>"))
				try:
					y1 = ['1+ ', '1 y', '1 г', '1 л', '1 р', '1+ г', '1+ л', '1+ р', '1-го го', 'не менее одного', 'не менее год', 'более одного', 'один год', '1-2', '1-3', '1 to 2', '1 to 3', '1 до 2', '1 до 3', 'half a year', 'полгода', 'півроку']
					y2 = ['2+ ', '2 y', '2 г', '2 л', '2 р', '2+ г', '2+ л', '2+ р', '2-х р', '2-х л', '2х л', '2х р', 'двох', 'двух', '2-3', '2-4', '2-5', '2 to 3', '2 to 4', '2 to 5', '2 до 3', '2 до 4', '2 до 5', '1.5', '1,5', 'полтора', 'півтора']
					y3 = ['3+ ', '3 y', '3 г', '3 л', '3 р', '3+ г', '3+ л', '3+ р', '3-х р', '3-х л', '3х л', '3х р', 'трьох', 'трёх', 'трех', '3-4', '3-5', '3-6', '3 to 4', '3 to 5', '3 to 6', '3 до 4', '3 до 5', '3 до 6', '2.5', '2,5']
					y4 = ['4+ ', '4 y', '4 г', '4 л', '4 р', '4+ г', '4+ л', '4+ р', '4-х р', '4-х л', '4х л', '4х р', '4-5', '4-6', '4 to 5', '4 to 6', '4 до 5', '4 до 6', '3.5', '3,5']
					y5 = ['5+ ', '5 y', '5 г', '5 л', '5 р', '5+ г', '5+ л', '5+ р', 'пяти']
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
						else:
							exp.append(0)
				except Exception as e:
					print(e)
				exp_final = max(exp)
				print(url, title_text, exp_final)
				self.cur.execute(
					"INSERT INTO jop2 (url, title, company, description, img, id, exp, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (url, title_text, company_text, description_text, img_src, job_id, exp_final, url)
				)
				self.conn.commit() 
		except Exception as e:
			print(e)
			return

	
def main():
	parser = work_ua()
	parser.get_urls()
	parser = rabota_ua()
	parser.get_urls()
	parser = dou_ua()
	parser.get_urls()
	parser = djinni_co()
	parser.get_urls()
	parser = grc_ua()
	parser.get_urls()
	parser = freelancehunt_com()
	parser.get_urls()
	parser = jooble_org()
	parser.get_urls()
	parser = trud_ua()
	parser.get_urls()
	parser = superjob_ru()
	parser.get_urls()
	parser = jobs_ua()
	parser.get_urls()
	parser = trud_com()
	parser.get_urls()

if __name__ == '__main__':
	main()
