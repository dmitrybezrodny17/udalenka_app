import psycopg2
from flask import Flask, render_template, request, jsonify, Markup
import re
import math
import config as c
from modules.categorization import *

app = Flask(__name__, template_folder='template')

def search(search_terms, exp_in, tag_list, sort_by):
	conn = psycopg2.connect(dbname=c.DBNAME, user=c.USER, 
					   password=c.PASSWORD, host=c.HOST)
	cur = conn.cursor()
	cur.execute("SELECT url, title, company, salary, description, date, img, id, exp, links from jop2")
	rows = cur.fetchall()
	conn.commit() 
	conn.close()
	job_list = []
	match = 0
	for row in rows:
		url = row[0]
		title = row[1]
		company = row[2]
		salary = row[3]
		description = Markup(row[4])
		date = row[5]
		img = row[6]
		job_id = row[7]
		exp = row[8]
		links = row[9]
		if links == '' or links == ' ' or links is None:
			links = url
		for term in search_terms.split(' '):
			match = detect_category(term, title)
		job = (url, title, company, salary, description, date, match, img, job_id, exp, links)
		if exp is None:
			exp = 0
		if match > 0 and exp_in >= exp:
			if tag_list == "anything":
				job_list.append(job)
			else:
				for i in tag_list.split(' '):
				    if i == "java":
    					if (i in title.lower() or i in description.lower()) and not('javascript' in title.lower() or 'javascript' in description.lower()):
    						job_list.append(job)
    					else:
    						pass
				    else:
    					if i in title.lower() or i in description:
    						job_list.append(job)
    					else:
    						pass
		else:
			pass
		match = 0
	sorted_job_list = sorted(job_list, key=lambda x: x[5], reverse=True)
	return(sorted_job_list)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/faq")
def faq():
	return render_template("faq.html")

@app.route("/blog")
def blog():
	return render_template("blog.html")

@app.route("/<category>")
def category(category):
	if (category in ['favorite', 'node-js', 'ruby', 'motion-design', 'blockchain', 'copywriting', 'marketing-management', 'gamedev', 'mobile-dev', 'analyst', 'databases', 'network', 'qa-manual', 'qa-automation', 'crm', 'support', 'it-sec', 'full-stack', 'net', '1c', 'c-sharp', 'c++', 'java', 'kotlin', 'go', 'php', 'python', 'front-end', 'data-science', 'scala', 'embedded', 'top-management', 'project-management', 'product-management', 'web-design', 'ui-ux', 'graphic-design', '3d-design', 'other-design', 'hr', 'finances', 'seo-e-mail', 'ads-lead', 'smm', 'it-sales']):
		return render_template("index.html")
	else:
		return render_template("404.html")

@app.route('/_search')
def get():
	search_terms = request.args.get('skill')
	tag_list = request.args.get('tags')
	if tag_list is not None:
		tag_list = tag_list.rstrip()
	else:
		tag_list = "anything"
	page = int(request.args.get('page'))
	print(search_terms, page)
	exp_in = int(request.args.get('exp'))
	search_string = ' '.join(search_terms)
	job_list = search(search_terms, exp_in, tag_list, "1")
	return jsonify(result=job_list[page*20-20:page*20], page_count=math.ceil(len(job_list)/20), list_count=len(job_list))

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(threaded=True, debug=True)