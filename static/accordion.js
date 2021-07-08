 $(function() {
	var acc = document.getElementsByClassName("accordion");
	var i;
	
	for (i = 0; i < acc.length; i++) {
	  acc[i].addEventListener("click", function(e) {
		  
		
		if (!$(e.target).hasClass('button')){
			var panel = this.querySelector('.panel');
			if (panel.style.maxHeight) {
			  panel.style.maxHeight = null;
			  panel.style.backgroundColor = "white";
			  this.style.backgroundColor = "white";
			  this.classList.remove('active');
			} else {
			  panel.style.maxHeight = panel.scrollHeight + "px";
			  panel.style.backgroundColor = "#fff";
			  this.style.backgroundColor = "#fff";
			  this.classList.add('active');
		} 
	  }});
	}
 });