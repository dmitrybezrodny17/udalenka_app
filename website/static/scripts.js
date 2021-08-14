function tags(e) {
	var tag = e.innerText;
	var list = [];
	var tags = JSON.parse(localStorage.getItem("tags"));
	for (i in tags) {
		list.push(tags[i]);
	}

	if (tags != null){
		if (!tags.includes(tag)){
			list.push(tag);
		} else {
			const index = list.indexOf(tag);
			list.splice(index, 1);
		}
	
	} else {
		list.push(tag);
	}

	localStorage.setItem('tags', JSON.stringify(list));
};

function set_experience(e) {
	if (!$(event.target).hasClass('button')){
		document.querySelectorAll('[id=page]').forEach((element)=> {
			element.classList.remove('active');
		});
		var current_exp = JSON.parse(localStorage.getItem("exp"));
		e.classList.add('active');
		localStorage.setItem('exp', e.getAttribute('value'));
		location.reload();
		}
};

function favorite(e) {
	var category = window.location.href.split('/')[3].split('#')[0];
	var list = []
	var favorites = JSON.parse(localStorage.getItem("favorites"));
	for (i in favorites) {
		list.push(favorites[i]);
	}
				
	if (favorites != null){
		if (!favorites.includes(category)){
			e.textContent = '★';
       	    document.querySelector('#fav_label').style = "margin:5px 0px 0px 5px; font-size:14px; font-family:'Mont'";
            document.querySelector('#fav_list').style = "display:flex; align-items:center; margin:5px 10px 10px 0px; justify-content:left; font-size:14px; font-family:'Mont'; flex-wrap: wrap";
			list.push(category);
			console.log(list)
			var fav_template = document.querySelector('#fav_template');
			var fav_list = document.querySelector("#fav_list");
			let fav_clone = fav_template.content.cloneNode(true);
			fav_clone.querySelector('#fav').setAttribute("href", "/" + category);
			fav_clone.querySelector('#fav').textContent = category;
			fav_list.appendChild(fav_clone);
		} else {
			const index = list.indexOf(category);
			list.splice(index, 1);
			console.log(list)
			e.textContent = '☆';
			var created_favs = document.getElementsByClassName("fav");
			for (var i = 0; i < created_favs.length; i++) {
				if (created_favs[i].textContent == category) {
					created_favs[i].remove();
				}
			}
			console.log(list.length);
			if (list.length == 0) {
	               document.querySelector('#fav_label').style = "visibility: hidden; margin:0; height:0;";
	               document.querySelector('#fav_list').style = "display:flex; align-items:center; margin:0; justify-content:left; font-size:14px; font-family:'Mont'; flex-wrap: wrap";
			}
		}
						
		} else {
			e.textContent = '★';
	   	    document.querySelector('#fav_label').style = "margin:5px 0px 0px 5px; font-size:14px; font-family:'Mont'";
	        document.querySelector('#fav_list').style = "display:flex; align-items:center; margin:5px 10px 10px 0px; justify-content:left; font-size:14px; font-family:'Mont'; flex-wrap: wrap";
			list.push(category);
			console.log(list)
			var fav_template = document.querySelector('#fav_template');
			var fav_list = document.querySelector("#fav_list");
			let fav_clone = fav_template.content.cloneNode(true);
			fav_clone.querySelector('#fav').setAttribute("href", "/" + category);
			fav_clone.querySelector('#fav').textContent = category;
			fav_list.appendChild(fav_clone);
		}
						
		localStorage.setItem('favorites', JSON.stringify(list));
};

function acc(e) {
	var panel = e.querySelector('.panel');
	if (panel.style.maxHeight) {
		panel.style.maxHeight = null;
		panel.style.backgroundColor = "white";
		e.style.backgroundColor = "white";
		e.classList.remove('active');
	} else {
		panel.style.maxHeight = panel.scrollHeight + "px";
		panel.style.backgroundColor = "#fff";
		e.style.backgroundColor = "#fff";
		e.classList.add('active');
	} 
};

function accordion(e) {
	if (!$(event.target).hasClass('button') && !$(event.target).hasClass('favorite')){
		var post = $(e.querySelector('.accordion_head'));
		var job_id = post.attr('id');
		var list = []
		var viewed = JSON.parse(localStorage.getItem("viewed"));
		for (i in viewed) {
				list.push(viewed[i]);
			}
		if (viewed != null){
			if (!viewed.includes(job_id)){
				e.querySelector("#title").style = "color: #D3D3D3;overflow: hidden; white-space: nowrap; text-overflow: ellipsis;";
				e.querySelector("#company").style = "color: #D3D3D3;overflow: hidden; white-space: nowrap; text-overflow: ellipsis;";
				e.querySelector("#date").style = "color: #D3D3D3";
				list.push(job_id);
			}
		} else {
			e.querySelector("#title").style = "color: #D3D3D3;overflow: hidden; white-space: nowrap; text-overflow: ellipsis;";
			e.querySelector("#company").style = "color: #D3D3D3;overflow: hidden; white-space: nowrap; text-overflow: ellipsis;";
			e.querySelector("#date").style = "color: #D3D3D3";
			list.push(job_id);
		}
		localStorage.setItem('viewed', JSON.stringify(list));
		var localValue = localStorage.getItem('viewed');
		var panel = e.querySelector('.panel');
		if (panel.style.maxHeight) {
		  panel.style.maxHeight = null;
		  panel.style.backgroundColor = "white";
		  e.style.backgroundColor = "white";
		  if (e.getBoundingClientRect().top < 0) {
			window.scroll({top: findPos(e), behavior: 'smooth'});
			function findPos(obj) {
				var curtop = 0;
				if (obj.offsetParent) {
					do {
						curtop += obj.offsetTop;
					} while (obj = obj.offsetParent);
				return [curtop];
				}
			}
		  }
		} else {
    		panel.style.maxHeight = panel.scrollHeight + "px";
    		panel.style.backgroundColor = "#fff";
    		e.style.backgroundColor = "#fff";
    		e.classList.add('active');
		} 
	}
};

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
	mybutton = document.getElementById("myBtn");
	myimage = document.getElementById("myImg");
	if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
		mybutton.style.display = "block";
		myimage.style.display = "block";
	} else {
		mybutton.style.display = "none";
		myimage.style.display = "none";
	}
}

function topFunction() {
	document.body.scrollTop = 0;
	document.documentElement.scrollTop = 0;
}