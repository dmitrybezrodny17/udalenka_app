$(function firstData() {
	var currentCategory = window.location.href.split('/')[3];
		
	if (JSON.parse(localStorage.getItem("tags")) !== null) {
		var selected_tags = JSON.parse(localStorage.getItem("tags"));			
	} else {
		var selected_tags = []
	}
	var category_tags = []
	
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
				// Developers
	if (currentCategory == 'databases'){
		$('#skilz option:contains(' + 'Databases' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'network'){
		$('#skilz option:contains(' + 'Network' + ')').prop({selected: true}).change();
		category_tags = ["devops"];
	} else if (currentCategory == 'it-sec'){
		$('#skilz option:contains(' + 'IT Security' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'qa-manual'){
		$('#skilz option:contains(' + 'QA Manual' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'qa-automation'){
		$('#skilz option:contains(' + 'QA Automation' + ')').prop({selected: true}).change();
		category_tags = ["python","java","javascript"];
	} else if (currentCategory == 'gamedev'){
		$('#skilz option:contains(' + 'GameDev' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'mobile-dev'){
		$('#skilz option:contains(' + 'Mobile Development' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'full-stack'){
		$('#skilz option:contains(' + 'Full Stack' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'net'){
		$('#skilz option:contains(' + 'C#/.NET' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'python'){
		$('#skilz option:contains(' + 'Python' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'front-end'){
		$('#skilz option:contains(' + 'Front End' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'java'){
		$('#skilz option:contains(' + 'Java' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'kotlin'){
		$('#skilz option:contains(' + 'Kotlin' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'golang'){
		$('#skilz option:contains(' + 'Golang' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'scala'){
		$('#skilz option:contains(' + 'Scala' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'c++'){
		$('#skilz option:contains(' + 'C/C++' + ')').prop({selected: true}).change();
	} else if (currentCategory == '1C'){
		$('#skilz option:contains(' + '1c' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'php'){
		$('#skilz option:contains(' + 'PHP' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'ruby'){
		$('#skilz option:contains(' + 'Ruby' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'node-js'){
		$('#skilz option:contains(' + 'Node.JS' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'crm'){
		$('#skilz option:contains(' + 'CRM, ERP' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'blockchain'){
		$('#skilz option:contains(' + 'Data Science' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'embedded'){
		$('#skilz option:contains(' + 'Blockchain' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'data-science'){
		$('#skilz option:contains(' + 'Embedded' + ')').prop({selected: true}).change();
				// Management
	} else if (currentCategory == 'project-management'){
		$('#skilz option:contains(' + 'Project Management' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'product-management'){
		$('#skilz option:contains(' + 'Product Management' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'marketing-management'){
		$('#skilz option:contains(' + 'Marketing Management' + ')').prop({selected: true}).change();
				// Design
	} else if (currentCategory == 'web-design'){
		$('#skilz option:contains(' + 'Web Design' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'ui-ux'){
		$('#skilz option:contains(' + 'UI/UX' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'graphic-design'){
		$('#skilz option:contains(' + 'Graphic Design' + ')').prop({selected: true}).change();
	} else if (currentCategory == '3d-design'){
		$('#skilz option:contains(' + '3D Design' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'motion-design'){
		$('#skilz option:contains(' + 'Motion Design' + ')').prop({selected: true}).change();
				// Miscellaneous
	} else if (currentCategory == 'hr'){
		$('#skilz option:contains(' + 'HR' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'seo-e-mail'){
		$('#skilz option:contains(' + 'SEO/E-mail' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'ads-lead'){
		$('#skilz option:contains(' + 'Ads/Lead' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'smm'){
		$('#skilz option:contains(' + 'SMM' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'it-sales'){
		$('#skilz option:contains(' + 'IT-sales' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'analyst'){
		$('#skilz option:contains(' + 'Analyst' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'support'){
		$('#skilz option:contains(' + 'Support' + ')').prop({selected: true}).change();
	} else if (currentCategory == 'copywriting'){
		$('#skilz option:contains(' + 'Copywriting' + ')').prop({selected: true}).change();
	} else if (currentCategory === ''){
		$('#skilz option:contains(' + 'Все вакансии' + ')').prop({selected: true}).change();
		currentCategory = 'anything';
	} else if (currentCategory == 'favorite'){
		$('#skilz option:contains(' + 'Избранное' + ')').prop({selected: true}).change();
		if (favorites !== null) {
	        currentCategory = favorites.join(" ");
		}
	}
	
	var sentinel = document.querySelector('#sentinel');
	var scroller = document.querySelector("#scroller");
	var template = document.querySelector('#post_template');
	var page_num = 1;
	
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
	
	var tag_template = document.querySelector('#tag_template');
	var tag_list = document.querySelector("#tag_list");
	if (category_tags.length > 0) {
		for (i = 0; i < category_tags.length; i++) {
			let tag_clone = tag_template.content.cloneNode(true);
			if (selected_tags.includes(category_tags[i])) {
				tag_clone.querySelector('#tag').setAttribute("class", "active_tags");
			}
			tag_clone.querySelector('#tag').setAttribute("href", "/" + currentCategory);
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
		var current_exp = JSON.parse(localStorage.getItem("exp"));
	if (current_exp === null) {
	    document.querySelectorAll('[id=page]')[0].classList.add('active');
	} 
	    
	document.querySelectorAll('[id=page]').forEach((element)=> {
		if (parseInt(element.getAttribute('value')) === current_exp){
			element.classList.add('active');
		}
	});
	
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
		    tags: tag_list
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
			tags: tag_list
	    }, function(data) {
	        document.querySelector('#loader').visibility = 'visible';
		    document.querySelector('#old_posts').setAttribute("value", data.list_count);
		    for (var i = 0; i < data.result.length; i++) {
    			if (data.result[i][6] > 0){
	    			let template_clone = template.content.cloneNode(true);
				
    				template_clone.querySelector(".accordion_head").setAttribute("id", data.result[i][8]);
	    			var viewed = JSON.parse(localStorage.getItem("viewed"));
		    		if (viewed != null &&viewed.includes(data.result[i][8].toString())){
			    		template_clone.querySelector("#title").textContent = data.result[i][1];
			    		template_clone.querySelector("#title").style = "color: #D3D3D3;overflow: hidden; white-space: nowrap; text-overflow: ellipsis;";
			    		template_clone.querySelector("#company").style = "color: #D3D3D3;overflow: hidden; white-space: nowrap; text-overflow: ellipsis;";
			    		template_clone.querySelector("#date").style = "color: #D3D3D3";
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
	    		    	template_clone.querySelector("#img").style = "background-image: url(" + data.result[i][7] + ")";
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
					
    			    if (data.result[i][10].includes(",")) {
    			        var links = data.result[i][10].split(",");
    			        for (x in links) {
    			            for (y in source_list) {
        			            if (links[x].includes(source_list[y]) && !(data.result[i][0].includes(source_list[y]))) {
        			                template_clone.querySelector("#"+CSS.escape(source_list[y])).style = "margin-top:5px;";
        			                template_clone.querySelector("#"+CSS.escape(source_list[y])).textContent = "Смотреть на " + source_list[y];
        			            	template_clone.querySelector("#"+CSS.escape(source_list[y])).setAttribute("onClick", "window.open('" + links[x] + "')");
        			            }
    			            }
    			        }
    		    	}
    			    scroller.appendChild(template_clone);
    			}
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
