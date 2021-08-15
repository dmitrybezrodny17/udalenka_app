$(function firstData() {
	var currentCategory = window.location.href.split('/')[3];
	var category_tags = [];
	var filters = 0;
	
	// проверяем показываются ли вакансии без зп
	if (JSON.parse(localStorage.getItem("nullzp")) !== null) {
		nullzp = JSON.parse(localStorage.getItem("nullzp"));
		if (nullzp == 1) {
			document.getElementById("zp").checked = true;
		} else {
			document.getElementById("zp").checked = false;
		}
	} else {
		nullzp = 1;
		localStorage.setItem('nullzp', JSON.stringify(nullzp));
	}
	//
	
	// устанавливаем зарплату
	if (JSON.parse(localStorage.getItem("salary")) !== null) {
		salary = JSON.parse(localStorage.getItem("salary"))
		document.querySelector('#salary').value = salary;		
	} else {
		salary = '0';
	}
	//
	
	// поиск по энтеру
	$(".salary").on('keyup', function (e) {
		if (e.key === 'Enter' || e.keyCode === 13) {
			var salary = document.querySelector('#salary').value;
			localStorage.setItem('salary', JSON.stringify(salary));
			if (currentCategory !== 'anything') {
		    	window.location = '/' + currentCategory;
			} else {
		    	window.location = 'https://udalenka.com.ua/';
			}
		}
	});
	//
		
	// парсим сохраненные теги
	if (JSON.parse(localStorage.getItem("tags")) !== null) {
		var selected_tags = JSON.parse(localStorage.getItem("tags"));			
	} else {
		var selected_tags = []
	}
	
	var favorites = JSON.parse(localStorage.getItem("favorites"));
	if (favorites === null || favorites === "" || favorites.length < 1) {
	    document.querySelector('#fav_label').style = "visibility: hidden; margin:0; height:0;";
	    document.querySelector('#fav_list').style = "display:flex; align-items:center; margin:0; justify-content:left; font-size:14px; font-family:'Mont'; flex-wrap: wrap";
	}
	if (currentCategory == 'favorite' || currentCategory === '') {
		$('.favorite').hide();
		if ((favorites === null || favorites === '' || favorites.length < 1) && currentCategory == 'favorite') {
	           document.querySelector('#loader').remove();
		    var btn = document.createElement("DIV"); 
            btn.innerHTML = "Здесь пока ничего нет, нажмите на звездочку в нужной категории чтобы добавить её в список"; 
            btn.style = "text-align:center;"
            document.body.appendChild(btn);
		}
	}
	if (currentCategory !== null && favorites !== null && favorites !== "") {
		if (favorites.includes(currentCategory)) {
			document.querySelector('#favorite').textContent = '★';
	       	document.querySelector('#fav_label').style = "margin:5px 0px 0px 5px; font-size:14px; font-family:'Mont'";
	        document.querySelector('#fav_list').style = "display:flex; align-items:center; margin:5px 10px 5px 0px; justify-content:left; font-size:14px; font-family:'Mont'; flex-wrap: wrap";
		}
	}
	
	// выбор категории
				// Developers
	if (currentCategory == 'databases'){
		$('#select_category option:contains(' + 'Databases' + ')').prop({selected: true}).change();
		category_tags = ["BI", "Oracle", "DBA"];
	} else if (currentCategory == 'network'){
		$('#select_category option:contains(' + 'Network' + ')').prop({selected: true}).change();
		category_tags = ["devops", "linux", "windows", "azure"];
	} else if (currentCategory == 'it-sec'){
		$('#select_category option:contains(' + 'IT Security' + ')').prop({selected: true}).change();
		category_tags = ["pentest", "secops"];
	} else if (currentCategory == 'qa-manual'){
		$('#select_category option:contains(' + 'QA Manual' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'qa-automation'){
		$('#select_category option:contains(' + 'QA Automation' + ')').prop({selected: true}).change();
		category_tags = ["python","java","javascript"];
	} else if (currentCategory == 'gamedev'){
		$('#select_category option:contains(' + 'GameDev' + ')').prop({selected: true}).change();
		category_tags = ["unity", "level", "casual"];
	} else if (currentCategory == 'mobile-dev'){
		$('#select_category option:contains(' + 'Mobile Development' + ')').prop({selected: true}).change();
		category_tags = ["android", "ios", "xamarin", "flutter"];
	} else if (currentCategory == 'full-stack'){
		$('#select_category option:contains(' + 'Full Stack' + ')').prop({selected: true}).change();
		category_tags = ["php", "java", "ruby", "javascript"];
	} else if (currentCategory == 'net'){
		$('#select_category option:contains(' + 'C#/.NET' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'python'){
		$('#select_category option:contains(' + 'Python' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'front-end'){
		$('#select_category option:contains(' + 'Front End' + ')').prop({selected: true}).change();
		category_tags = ["javascript", "react", "angular", "typescript", "wordpress", "vue"];
	} else if (currentCategory == 'java'){
		$('#select_category option:contains(' + 'Java' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'kotlin'){
		$('#select_category option:contains(' + 'Kotlin' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'golang'){
		$('#select_category option:contains(' + 'Golang' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'scala'){
		$('#select_category option:contains(' + 'Scala' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'c++'){
		$('#select_category option:contains(' + 'C/C++' + ')').prop({selected: true}).change();
	} else if (currentCategory == '1C'){
		$('#select_category option:contains(' + '1c' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'php'){
		$('#select_category option:contains(' + 'PHP' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'ruby'){
		$('#select_category option:contains(' + 'Ruby' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'node-js'){
		$('#select_category option:contains(' + 'Node.JS' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'crm'){
		$('#select_category option:contains(' + 'CRM, ERP' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'blockchain'){
		$('#select_category option:contains(' + 'Blockchain' + ')').prop({selected: true}).change();
		category_tags = ["solidity", "smart"];
	} else if (currentCategory == 'embedded'){
		$('#select_category option:contains(' + 'Embedded' + ')').prop({selected: true}).change();
		category_tags = ["firmware", "voip", "hardware"];
	} else if (currentCategory == 'data-science'){
		$('#select_category option:contains(' + 'Data Science' + ')').prop({selected: true}).change();
		category_tags = ["big", "deep", "ai"];
				// Management
	} else if (currentCategory == 'project-management'){
		$('#select_category option:contains(' + 'Project Management' + ')').prop({selected: true}).change();
		category_tags = ["delivery", "engineering", "scrum"];
	} else if (currentCategory == 'product-management'){
		$('#select_category option:contains(' + 'Product Management' + ')').prop({selected: true}).change();
		category_tags = ["r&d", "growth", "engineering"];
	} else if (currentCategory == 'marketing-management'){
		$('#select_category option:contains(' + 'Marketing Management' + ')').prop({selected: true}).change();
		category_tags = ["affiliate", "google", "leads"];
				// Design
	} else if (currentCategory == 'web-design'){
		$('#select_category option:contains(' + 'Web Design' + ')').prop({selected: true}).change();
		category_tags = ["верстка", "css"];
	} else if (currentCategory == 'ui-ux'){
		$('#select_category option:contains(' + 'UI/UX' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'graphic-design'){
		$('#select_category option:contains(' + 'Graphic Design' + ')').prop({selected: true}).change();
		category_tags = ["2d", "character", "иллюстратор"];
	} else if (currentCategory == '3d-design'){
		$('#select_category option:contains(' + '3D Design' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'motion-design'){
		$('#select_category option:contains(' + 'Motion Design' + ')').prop({selected: true}).change();
				// Miscellaneous
	} else if (currentCategory == 'hr'){
		$('#select_category option:contains(' + 'HR' + ')').prop({selected: true}).change();
		category_tags = ["recruiter", "скаут", "серчер", "staff"];
	} else if (currentCategory == 'seo-e-mail'){
		$('#select_category option:contains(' + 'SEO/E-mail' + ')').prop({selected: true}).change();
		category_tags = ["aso", "link", "email"];
	} else if (currentCategory == 'ads-lead'){
		$('#select_category option:contains(' + 'Ads/Lead' + ')').prop({selected: true}).change();
		category_tags = ["affiliate", "ppc", "google", "таргет", "арбитраж"];
	} else if (currentCategory == 'smm'){
		$('#select_category option:contains(' + 'SMM' + ')').prop({selected: true}).change();
		category_tags = ["instagram", "директ", "media", "контент"];
	} else if (currentCategory == 'it-sales'){
		$('#select_category option:contains(' + 'IT-sales' + ')').prop({selected: true}).change();
		category_tags = ["account", "sales"];
	} else if (currentCategory == 'analyst'){
		$('#select_category option:contains(' + 'Analyst' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'support'){
		$('#select_category option:contains(' + 'Support' + ')').prop({selected: true}).change();
		category_tags = ["customer", "helpdesk", "zendesk"];
	} else if (currentCategory == 'copywriting'){
		$('#select_category option:contains(' + 'Copywriting' + ')').prop({selected: true}).change();
	} else if (currentCategory === ''){
		$('#select_category option:contains(' + 'Все вакансии' + ')').prop({selected: true}).change();
		currentCategory = 'anything';
	} else if (currentCategory.includes('fbclid')){
		$('#select_category option:contains(' + 'Все вакансии' + ')').prop({selected: true}).change();
		currentCategory = 'anything';
	} else if (currentCategory == 'favorite'){
		$('#select_category option:contains(' + 'Избранное' + ')').prop({selected: true}).change();
		if (favorites !== null) {
	        currentCategory = favorites.join(" ");
		}
	}
	
	var sentinel = document.querySelector('#sentinel');
	var scroller = document.querySelector("#scroller");
	var template = document.querySelector('#post_template');
	var page_num = 1;
	
	// загружаем избранное
	var fav_template = document.querySelector('#fav_template');
	var fav_list = document.querySelector("#fav_list");
	if (favorites != null) {
		for (i = 0; i < favorites.length; i++) {
			let fav_clone = fav_template.content.cloneNode(true);
			fav_clone.querySelector('#fav').setAttribute("href", "/" + favorites[i]);
			fav_clone.querySelector('#fav').textContent = favorites[i];
			fav_list.appendChild(fav_clone);
		}		
	} 
	
	// загружаем теги
	var tag_template = document.querySelector('#tag_template');
	var tag_list = document.querySelector("#tag_list");
	if (category_tags.length > 0) {
		for (i = 0; i < category_tags.length; i++) {
			let tag_clone = tag_template.content.cloneNode(true);
			if (selected_tags.includes(category_tags[i])) {
				tag_clone.querySelector('#tag').setAttribute("class", "active_tags");
	        	filters++;
			}
			tag_clone.querySelector('#tag').textContent = category_tags[i];
			tag_list.appendChild(tag_clone);
		}
	} else {
		document.querySelector('#tag_label').style = "visibility:hidden; height:0; margin:0";
		document.querySelector('#tag_list').style = "visibility:hidden; height:0; margin:0";
	}
	
	var tag_elements = document.getElementsByClassName('active_tags');
	var tag_list = ''
	for (i = 0; i < tag_elements.length; i++) {
		tag_list += tag_elements[i].innerText + ' ';
	}
	
	// парсим опыт
	if (JSON.parse(localStorage.getItem("exp")) !== null) {
		var current_exp = JSON.parse(localStorage.getItem("exp"));
	} else {
		var current_exp = 69
	}
	    
	document.querySelectorAll('[id=exp_button]').forEach((element)=> {
		if (parseInt(element.getAttribute('value')) === current_exp){
			element.classList.add('active');
		}
	});
	
	// парсим источники
	if (JSON.parse(localStorage.getItem("source")) !== null) {
		var sources = JSON.parse(localStorage.getItem("source"));
	} else {
		var sources = ["work","rabota","grc","dou","freelancehunt","trud","jooble","djinni"];
		localStorage.setItem('source', JSON.stringify(sources));
	}
	
	document.querySelectorAll('[id=source]').forEach((element)=> {
		if (sources.includes(element.getAttribute('value'))){
			element.classList.add('active_sources');
		}
	});
	
	// считаем фильтры
	if (((salary  !== '0') && (salary.length > 0)) || (nullzp == 0)) {
		filters++;
	}
	//if (selected_tags.length > 0) {
//		filters++;
//	}
	if (current_exp !== 69) {
		filters++;
	}
	if (filters > 0) {
		document.querySelector('#filter_label').textContent = 'Фильтр (' + filters.toString() + ')▾';
	}
	// 
		
	var exp_num = document.getElementsByClassName('active')[0].getAttribute('value');
	/*if (parseInt(current_exp) < 11) {
	    document.querySelectorAll('[id=title]')[0].textContent = 'Фильтр (1)▾';
	}*/
		
		
	var intervalID = window.setInterval(CheckNews, 1000*60);

	function CheckNews() {
		$.getJSON('/_search', {
			skill: currentCategory,
			page: 1,
			exp: exp_num,
			tags: tag_list,
			salary: salary,
			nullzp: nullzp,
			sources: sources.join(' ')
		}, function(data) {
			var new_posts = data.list_count;	
			var old_posts = document.querySelector('#old_posts').getAttribute('value');
			if (parseInt(new_posts) > parseInt(old_posts))	{
				document.title = '(' + String(parseInt(new_posts) - parseInt(old_posts)) + ') Удалёнка — Поиск удалённой работы';
				document.querySelector('#news').style = "top: 0; display: block; max-height: 500px; border: 1px solid #D1D1D1; padding: 5px; border-radius: 5px; margin-bottom: 5px; background: lightgoldenrodyellow";
				var dif = parseInt(new_posts) - parseInt(old_posts);
				document.querySelector('#new_posts').textContent = 'Новых вакансий: ' + String(dif);
			}
		});
	}
		
	function loadItems() {
        $.getJSON('/_search', {
			skill: currentCategory,
			page: page_num,
			exp: exp_num,
			tags: tag_list,
			salary: salary,
			nullzp: nullzp,
			sources: sources.join(' ')
	    }, function(data) {
    		if (data.result.length == 0) {
    		    document.querySelector('#loader').remove();
    		    var btn = document.createElement("DIV"); 
    		    if (document.getElementById("title")) {
                  btn.innerHTML = "<br><br>Вакансий больше нет :(<br><br><br><br>"; 
    		    } else {
                  btn.innerHTML = "<br><br>По вашему запросу ничего не найдено :("; 
    		    }
                btn.style = "text-align:center;"
                document.body.appendChild(btn);
    		}
    		console.log(data.list_count);
	        document.querySelector('#loader').visibility = 'visible';
		    document.querySelector('#old_posts').setAttribute("value", data.list_count);
		    for (var i = 0; i < data.result.length; i++) {
				console.log(data.result[i]);
    			if (data.result[i][6] > 0){
	    			let template_clone = template.content.cloneNode(true);
				
    				template_clone.querySelector(".accordion_head").setAttribute("id", data.result[i][8]);
	    			var viewed = JSON.parse(localStorage.getItem("viewed"));
		    		if (viewed != null &&viewed.includes(data.result[i][8].toString())){
			    		template_clone.querySelector("#title").textContent = data.result[i][1];
			    		template_clone.querySelector("#title").style = "color: #D3D3D3;overflow: hidden; white-space: nowrap; text-overflow: ellipsis;margin: 0px;line-height:16px;";
			    		template_clone.querySelector("#company").style = "color: #D3D3D3;overflow: hidden; white-space: nowrap; text-overflow: ellipsis;margin: 0px;line-height:16px;";
			    		template_clone.querySelector("#date").style = "color: #D3D3D3;width:120px;margin: 0px;line-height:16px;position:absolute;bottom:0;right:0;text-align:right;";
			    		//template_clone.querySelector("#salary").style = "color: #D3D3D3;overflow: hidden; white-space: nowrap; text-overflow: ellipsis; line-height:16px;max-width:170px;";
			    	} else {
			    		template_clone.querySelector("#title").textContent = data.result[i][1];
			    	}
				
			    	template_clone.querySelector("#company").textContent = data.result[i][2];
				
			    	if (data.result[i][7] === '/static/logo.svg' || data.result[i][7].includes('superjob.ru') || data.result[i][7].includes('freelancehunt')) {
			         	template_clone.querySelector("#img").style = "border:1px solid #D1D1D1; display:flex; justify-content:center; align-items:center; font-size:20px; color:#D1D1D1;";
		    	    	if (data.result[i][2] === ''){
		    	        	template_clone.querySelector("#img").textContent = data.result[i][1].substring(0,1);
		    	        	template_clone.querySelector("#company").textContent = 'Не указана';
		    	    	} else {
		    	        	template_clone.querySelector("#img").textContent = data.result[i][2].substring(0,1);
	    		    	} 
	    			} else {
	    		    	template_clone.querySelector("#img").style = "background-image: url(" + data.result[i][7] + ");border:1px solid rgb(209, 209, 209);";
	    			}			
	    			
	    			if (parseInt(data.result[i][3]) > 0) {
	    			    template_clone.querySelector("#salary").textContent = 'Платят: ₴' + data.result[i][3].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	    			} else {
	    			    template_clone.querySelector("#salary").style = "display:none;"
	    			}
				
	    			if ((parseInt(data.result[i][9]) > 0) && (data.result[i][9] !== null)) {
	    			    if (parseInt(data.result[i][9]) >= 5) { 
	    			        template_clone.querySelector("#exp").textContent = 'Требуемый опыт: ' + data.result[i][9] + ' лет';
	    			    } else if ((parseInt(data.result[i][9]) <= 4) && (parseInt(data.result[i][9]) >= 2)) {
	    			        template_clone.querySelector("#exp").textContent = 'Требуемый опыт: ' + data.result[i][9] + ' года';
	    			    } else if (parseInt(data.result[i][9]) == 1) {
	    			        template_clone.querySelector("#exp").textContent = 'Требуемый опыт: 1 год';
	    			    }
	    			} else {
	    			    template_clone.querySelector("#exp").style = "display:none;"
	    			}
				
    				template_clone.querySelector("#description").innerHTML = data.result[i][4];
    				template_clone.querySelector("#url").setAttribute("onClick", "window.open('" + data.result[i][0] + "')");
    				var source_list = ["djinni.co", "work.ua", "rabota.ua", "dou.ua", "grc.ua", "trud.com", "freelancehunt.com", "jooble.org", "trud.ua", "superjob.ru", "jobs.ua"];
    				for (var a in source_list) {
    				    if (data.result[i][0].includes(source_list[a])) {
    				        template_clone.querySelector("#url").textContent = "Смотреть на " + source_list[a];
    				    } 
    				}
    				if (Date.now() - (new Date(data.result[i][5]).getTime()) < 60000){
    					template_clone.querySelector("#date").textContent = "Только что";
    				} else if(Date.now() - (new Date(data.result[i][5]).getTime()) < 3600000) {
    					template_clone.querySelector("#date").textContent = Math.ceil((Date.now() - ((new Date(data.result[i][5]).getTime()))) / 60000) + " мин. назад";
    				} else if(Date.now() - (new Date(data.result[i][5]).getTime()) < 86400000) {
    					template_clone.querySelector("#date").textContent = Math.ceil((Date.now() - ((new Date(data.result[i][5]).getTime()))) / 3600000) + " ч. назад";
    				} else if(Date.now() - (new Date(data.result[i][5]).getTime()) < 86400000*2) {
    					template_clone.querySelector("#date").textContent = "Вчера";
    				} else if(Date.now() - (new Date(data.result[i][5]).getTime()) < 86400000*7) {
    					template_clone.querySelector("#date").textContent = "На этой неделе";
    				} else {
    					template_clone.querySelector("#date").textContent = "На прошлой неделе";
    				} 
					
    			   
    			    scroller.appendChild(template_clone);
    			    if (data.result.length < 20) {
            		    document.querySelector('#loader').remove();
            		    var btn = document.createElement("DIV"); 
            		    btn.innerHTML = "<br><br>Вакансий больше нет :(<br><br><br><br><br><br><br><br>";
                        btn.style = "text-align:center;"
                        document.body.appendChild(btn);
    			    }
    			}
    		}
        	if (JSON.parse(localStorage.getItem("isfilteropen")) !== null) {
        	    var panel = document.getElementById("filters").parentNode.querySelector('.panel');	
        	    if (parseInt(JSON.parse(localStorage.getItem("isfilteropen"))) == 1) {
        	            panel.style.maxHeight = panel.scrollHeight + "px";
        				panel.style.backgroundColor = "#fff";
        				document.getElementById("filters").parentNode.style.backgroundColor = "#fff";
        				document.getElementById("filters").parentNode.classList.add('active');
        	    } else {
        			panel.style.maxHeight = null;
        			panel.style.backgroundColor = "white";
        			document.getElementById("filters").parentNode.style.backgroundColor = "white";
        			document.getElementById("filters").parentNode.classList.remove('active');
        	    }
        	} else {
        	    //pass
        	}
        	
    	    document.querySelector('#loader').visibility = 'hidden';
    	    document.querySelector('#loader').style.marginTop = '20px';
    		page_num += 1;
    	  });
    };
    var intersectionObserver = new IntersectionObserver(entries => {
    	if (entries[0].intersectionRatio <= 0) {
    		return;
    	}
    	loadItems();
    }, 
    {
    	rootMargin: '0px 0px 500px 0px',
    	threshold: 0
    });		
    intersectionObserver.observe(sentinel);	
    	  });
