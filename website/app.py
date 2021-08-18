import psycopg2
from flask import Flask, render_template, request, jsonify, Markup
import re
import math
import modules.config as c
from modules.categorization import *
from modules.search import *
import views

app = Flask(__name__, template_folder='template')

app.add_url_rule('/', view_func=views.home)
app.add_url_rule('/faq', view_func=views.faq)
app.add_url_rule('/blog', view_func=views.blog)
app.add_url_rule('/<category>', view_func=views.category)
app.add_url_rule('/_search', view_func=views.get)

if __name__ == '__main__':
	app.run(threaded=True)