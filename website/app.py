import psycopg2
from flask import Flask, render_template, request, jsonify, Markup
import re
import math
import modules.config as c
from modules.categorization import *
from modules.search import *

app = Flask(__name__, template_folder='template')
	
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
	search_terms = request.args['skill']
	tag_list = request.args['tags']
	salary = request.args['salary']
	nullzp = int(request.args['nullzp'])
	sources = request.args['sources']
	page = int(request.args['page'])
	exp_in = int(request.args['exp'])
	if salary is not None and salary is not '':
		salary = int(salary.replace(',','').replace('.',''))
	else:
		salary = 0
	if tag_list is not None and tag_list is not '':
		tag_list = tag_list.rstrip()
	else:
		tag_list = "anything"
	job_list = search(search_terms, exp_in, tag_list, salary, nullzp, sources, "1")
	#print(job_list[page*20-20:page*20][0])
	#print(math.ceil(len(job_list)/20))
	#print(len(job_list))
	return jsonify(result=job_list[page*20-20:page*20], page_count=math.ceil(len(job_list)/20), list_count=len(job_list))
	
@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(threaded=True)