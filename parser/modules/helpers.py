def get_exp(description_text):
	description_dict = {"<li>": "<p>", "<span": "<p>", "<br/>": "<p>", "&nbsp;": "<p>", u"\xa0": u" "}
	for i, j in description_dict.items():
		description_text = description_text.replace(i, j).strip()
	desc_list = description_text.split("<p>")
	try:
		y1 = ['1+ ', '1 y', '1 г', '1 ле', '1 р', '1+ г', '1+ л', '1+ р', '1-го го', 'не менее одного', 'не менее год', 'более одного', 'один год', '1-2', '1-3', '1 to 2', '1 to 3', '1 до 2', '1 до 3', 'half a year', 'полгода', 'півроку']
		y2 = ['2+ ', '2 y', '2 г', '2 ле', '2 р', '2+ г', '2+ л', '2+ р', '2-х р', '2-х л', '2х л', '2х р', 'двох', 'двух', '2-3', '2-4', '2-5', '2 to 3', '2 to 4', '2 to 5', '2 до 3', '2 до 4', '2 до 5', '1.5', '1,5', 'полтора', 'півтора']
		y3 = ['3+ ', '3 y', '3 г', '3 ле', '3 р', '3+ г', '3+ л', '3+ р', '3-х р', '3-х л', '3х л', '3х р', 'трьох', 'трёх', 'трех', '3-4', '3-5', '3-6', '3 to 4', '3 to 5', '3 to 6', '3 до 4', '3 до 5', '3 до 6', '2.5', '2,5']
		y4 = ['4+ ', '4 y', '4 г', '4 ле', '4 р', '4+ г', '4+ л', '4+ р', '4-х р', '4-х л', '4х л', '4х р', '4-5', '4-6', '4 to 5', '4 to 6', '4 до 5', '4 до 6', '3.5', '3,5']
		y5 = ['5+ ', '5 y', '5 г', '5 ле', '5 р', '5+ г', '5+ л', '5+ р', 'пяти']
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
			exp_final = max(exp)
	except Exception as e:
		exp_final = 0
	return(exp_final)
	
def clean_title(title):
	title_dic = {"удаленно": "", "удалённо": "", "на дому": "", "-centre": "-центра", " центра": "-центра", "()": ""}
	for i, j in title_dic.items():
		title = title.replace(i, j).strip()
	return title
