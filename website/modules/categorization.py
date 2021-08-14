def detect_category(term, title):
	match = 0
	tl = title.lower()
	if (term == 'anything'):
		match += 1
	elif (term == 'it-sales'): 
		m1 = ['sales', 'account', 'продаж']
		if any(x in tl for x in m1) and not 'salesforce' in tl:
			match += 1
	elif (term == 'support'): 
		m1 = ['поддержк', 'customer', 'support', 'helpdesk', 'підтримк', 'zendesk', 'контакт', 'cliend man']
		if any(x in tl for x in m1):
			match += 1
	elif (term == 'analyst'):
		m1 = ['business', 'бизнес', 'бізнес', 'analyst', 'аналитик', 'аналітик']
		m2 = ['data', 'product', 'developer', 'qa ']
		if any(x in tl for x in m1) and not any(x in tl for x in m2) or 'BA' in title:
			match += 1
	elif (term == 'smm'):
		m1 = ['страниц', 'инста', 'сторінк', 'instagram', 'директ', 'ведени', 'контент', 'content', 'social media']
		m2 = 'директор'
		m3 = ['SMM', 'СММ']
		if (any(x in tl for x in m1) and not m2 in tl) or any(x in title for x in m3):
			match += 1
	elif (term == 'ads-lead'):
		m1 = ['affiliate', 'ppc', 'google', 'ads', 'таргет', 'lead gen', 'лидо', 'арбитраж', 'контекст']
		m2 = ['dev', 'head', 'officer']
		if any(x in tl for x in m1) and not any(x in tl for x in m2):
			match += 1
	elif (term == 'seo-e-mail'):
		m1 = ['link', 'email', 'e-mail']
		m2 = ['SEO', 'ASO']
		if (any(x in tl for x in m1) or any(x in title for x in m2)) and not 'manage' in tl:
			match += 1
	elif (term == '3d-design'):
		if '3d' in tl and not 'unity' in tl:
			match += 1
	elif (term == 'marketing-management'):
		m1 = ['manager', 'менеджер', 'head', 'officer']
		m2 = ['marketing', 'brand', 'affiliate', 'lead gen', 'cpa', 'маркет', 'traffic', 'google', 'ads', 'acquisition']
		if (any(x in tl for x in m1) and any(x in tl for x in m2)) or ('marketing' in tl and 'special' in tl):
			match += 1
	elif (term == 'graphic-design'):
		m1 = ['2d', 'character', 'graphic', 'графич', 'графіч', 'иллю', 'illust', 'іллю']
		if any(x in tl for x in m1):
			match += 1
	elif (term == 'ui-ux'):
		m1 = ['UI', 'UX']
		m2 = ['business', 'react', 'angular', 'hybris']
		if any(x in title for x in m1) and not any(x in tl for x in m2):
			match += 1
	elif (term == 'web-design'):
		m1 = ['web', 'веб']
		m2 = ['design', 'дизайн']
		m3 = ['верст', 'html', 'css']
		m4 = ['full', 'game', 'html 5', 'html5']
		if ((any(x in tl for x in m1) and any(x in tl for x in m2)) or any(x in tl for x in m3)) and not any(x in tl for x in m4):
			match += 1
	elif (term == 'data-science'):
		m1 = ['scien', 'anal', 'engine', 'model', 'big', 'lead', 'head']
		m2 = ['ML', 'AI', 'DL', 'ETL']
		m3 = ['machine', 'deep']
		m4 = ['html', 'qml']
		if (('data' in tl and any(x in tl for x in m1)) or any(x in title for x in m2) or ('learn' in tl and any(x in tl for x in m3)) or ('comp' in tl and 'vision' in tl)) and not any(x in tl for x in m4):
			match += 1
	elif (term == 'embedded'):  
		m1 = ['embedded', 'firmware', 'radio', 'voip', 'telephony', 'hardware']
		m2 = ['RF', 'DSP', 'IoT', 'HW']
		if any(x in tl for x in m1) or any(x in title for x in m2):
			match += 1
	elif (term == 'crm'):
		m1 = ['salesforce', 'впровадженн', 'супроводженн', 'внедрен', 'интегр', 'business intelligence', 'tableau']
		m2 = ['manage', 'менедж', 'java']
		m3 = ['CRM', 'ERP', 'SAP', 'WMS', 'BI', 'NAV', 'WMS']
		if (any(x in tl for x in m1) or any(x in title for x in m3)) and not any(x in tl for x in m2):
			match += 1
	elif (term == 'php'):
		m1 = ['php', 'laravel', 'magento', 'wordpress', 'symfony', 'drupal', 'yii']
		if (((any(x in tl for x in m1) or ('back' in tl and 'php' in description)) and not 'full' in tl) or (any(x in tl for x in m1) or ('back' in tl and 'php' in description) and ' or ' in tl and 'full' in tl)) and not 'front' in tl and not 'full' in tl:
			match += 1
	elif (term == '1c'):
		m1 = ['1c', '1с']
		if any(x in tl for x in m1):
			match += 1
	elif (term == 'с++'):
		m1 = ['c++', 'qt', 'с++']
		if any(x in tl for x in m1):
			match += 1
	elif (term == 'scala'):
		if 'scala' in tl:
			match += 1
	elif (term == 'go'):
		m1 = ['full', 'google']
		if 'Go' in title and not any(x in tl for x in m1):
			match += 1
	elif (term == 'java'):
		m1 = ['java', 'kotlin']
		m2 = ['full', 'javascript', 'qa', 'quality']
		if (any(x in tl for x in m1) or ('back' in tl and 'java' in description)) and not any(x in tl for x in m2):
			match += 1
	elif (term == 'front-end'):
		m1 = ['javascript', 'react', 'front', 'angular', 'typescript', 'wordpress', 'html', 'vue', 'web dev']
		m2 = ['full', 'native', 'node']
		m3 = 'JS'
		if any(x in tl for x in m1) and not any(x in tl for x in m2) or m3 in title:
			match += 1
	elif (term == 'python'):
		if 'python' in tl:
			match += 1
	elif (term == 'net'):
		m1 = ['.net', 'c#', 'c #']
		if any(x in tl for x in m1):
			match += 1
	elif (term == 'full-stack'):
		if 'full' in tl or 'AEM' in title:
			match += 1
	elif (term == 'mobile-dev'): 
		m1 = ['android', 'flutter', 'ios', 'mobile', 'xamarin', 'андроид', 'swift', 'react native']
		m2 = ['qa', 'quality', 'test', 'тест']
		if any(x in tl for x in m1) and not any(x in tl for x in m2):
			match += 1
	elif (term == 'gamedev'):
		m1 = ['game', 'unity', 'киберсп', 'игр', 'level design', 'гейм', 'casual']
		if any(x in tl for x in m1):
			match += 1
	elif (term == 'it-sec'):
		m1 = ['sec', 'безпек', 'penet', 'безоп', 'доступ']
		if any(x in tl for x in m1):
			match += 1
	elif (term == 'network'):
		m1 = ['админ', 'інженер', 'инженер', 'архитек', 'архітек']
		m2 = ['систем', 'сервис', 'сервіс', 'web']
		m3 = ['admin', 'engineer']
		m4 = ['system', 'support', 'structure', 'web', 'service']
		m5 = ['мереж', 'сете', 'network', "зв'яз", 'связ', 'devops', 'monitoring', 'мониторинг', 'моніторинг', 'linux', 'datacenter', 'techops', 'unix', 'azure', 'windows', 'cloud', 'hyper-v']
		m6 = 'IP'
		if (((any(x in tl for x in m1) and any(x in tl for x in m2)) or (any(x in tl for x in m3) and any(x in tl for x in m4)) or any(x in tl for x in m5) or m6 in title) and not 'support' in tl) or 'AWS' in title:
			match += 1
	elif (term == 'databases'):
		m1 = ['qlik', 'sql', 'database', 'data base', 'oracle', 'firebird', 'mariadb', 'баз ', 'snowflake']
		m2 = ['DB', 'DWH', 'BI']
		m3 = 'full'
		if any(x in tl for x in m1) or any(x in title for x in m2) and not m3 in tl:
			match += 1
	elif (term == 'hr'):
		m1 = ['рекрут', 'recruit', 'персонал', 'talent', 'скаут', 'sourc', 'карьер', 'people', 'труд', 'прац', 'research', 'ресерч', 'staff', 'тренинг', 'тренінг', 'кадр', 'интервью', 'candidat', 'hrd']
		m2 = 'HR'
		if any(x in tl for x in m1) or m2 in title:
			match +=1
	elif (term == 'project-management'):
		m1 = ['project', 'проект', 'проєкт', 'delivery', 'engineering']
		m2 = ['manager', 'менедж', 'assistant', 'head', 'керівн', 'master', 'admin']
		m3 = 'PM'
		m4 = ['scrum', 'coordinat', 'координат']
		if (any(x in tl for x in m1) and any(x in tl for x in m2)) or any(x in tl for x in m4) or m3 in title:
			match +=1
	elif (term == 'product-management'):
		m1 = ['product', 'продакт', 'продукт', 'growth', 'engineer', 'R&D']
		m2 = ['manager', 'менеджер', 'officer', 'director', 'head', 'specialist', 'owner']
		m3 = ['продаж', 'marketing', 'маркетинг']
		if (any(x in tl for x in m1) and any(x in tl for x in m2)) and not any(x in tl for x in m3):
			match += 1
	elif (term == 'qa-automation'):
		m1 = ['qa', 'qc', 'quality', 'test', 'тест']
		m2 = ['aqa', 'auto']
		if any(x in tl for x in m1) and any(x in tl for x in m2):
			match += 1
	elif (term == 'qa-manual'):
		m1 = ['qa', 'qc', 'quality', 'test', 'тест']
		m2 = ['aqa', 'auto']
		if any(x in tl for x in m1) and not any(x in tl for x in m2):
			match += 1
	elif (term == 'ruby'):
		if 'ruby' in tl:
			match += 1
	elif (term == 'node-js'):
		if 'node.js' in tl or 'node js' in tl:
			match += 1
	elif (term == 'blockchain'):
		m1 = ['solidity', 'smart cont', 'blockchain']
		if any(x in tl for x in m1):
			match += 1
	elif (term == 'motion-design'):
		if 'motion' in tl or 'моушн' in tl:
			match += 1
	elif (term == 'copywriting'):
		m1 = ['writer', 'копирайт']
		if any(x in tl for x in m1):
			match += 1
	else:
		if (term.lower()) in tl:
			match += 1
	return(match)