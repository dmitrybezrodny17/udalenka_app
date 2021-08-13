 $(function() {
	$('#skilz').on('select2:select', function() {
		txt = $('select :selected').text();
					// Developers
		if (txt.includes("Databases")) {
				window.location.href = '/databases';
			} else if (txt.includes("SysAdmin/Network")){
				window.location.href = '/network';
			} else if (txt.includes("IT Security")){
				window.location.href = '/it-sec';
			} else if (txt.includes("QA Manual")){
				window.location.href = '/qa-manual';
			} else if (txt.includes("QA Automation")){
				window.location.href = '/qa-automation';
			} else if (txt.includes("Game Development")){
				window.location.href = '/gamedev';
			} else if (txt.includes("Mobile Development")){
				window.location.href = '/mobile-dev';
			} else if (txt.includes("Full Stack")){
				window.location.href = '/full-stack';
			} else if (txt.includes("C#/.NET")){
				window.location.href = '/net';
			} else if (txt.includes("Python")){
				window.location.href = '/python';
			} else if (txt.includes("Front End")){
				window.location.href = '/front-end';
			} else if (txt.includes("Java")){
				window.location.href = '/java';
			} else if (txt.includes("Golang")){
				window.location.href = '/golang';
			} else if (txt.includes("Scala")){
				window.location.href = '/scala';
			} else if (txt.includes("C/C++")){
				window.location.href = '/c++';
			} else if (txt.includes("1C")){
				window.location.href = '/1c';
			} else if (txt.includes("PHP")){
				window.location.href = '/php';
			} else if (txt.includes("Ruby")){
				window.location.href = '/ruby';
			} else if (txt.includes("Node.JS")){
				window.location.href = '/node-js';
			} else if (txt.includes("CRM, ERP")){
				window.location.href = '/crm';
			} else if (txt.includes("Embedded")){
				window.location.href = '/embedded';
			} else if (txt.includes("Data Science")){
				window.location.href = '/data-science';
			} else if (txt.includes("Blockchain")){
				window.location.href = '/blockchain';
					// Management
			} else if (txt.includes("Project Management")){
				window.location.href = '/project-management';
			} else if (txt.includes("Product Management")){
				window.location.href = '/product-management';
			} else if (txt.includes("Marketing Management")){
				window.location.href = '/marketing-management';
					// Design
			} else if (txt.includes("Web Design")){
				window.location.href = '/web-design';
			} else if (txt.includes("UI/UX")){
				window.location.href = '/ui-ux';
			} else if (txt.includes("Graphic Design")){
				window.location.href = '/graphic-design';
			} else if (txt.includes("3D Design")){
				window.location.href = '/3d-design';
			} else if (txt.includes("Motion Design")){
				window.location.href = '/motion-design';
					// Miscellaneous
			} else if (txt.includes("HR")){
				window.location.href = '/hr';
			} else if (txt.includes("SEO/E-mail")){
				window.location.href = '/seo-e-mail';
			} else if (txt.includes("Ads/Lead")){
				window.location.href = '/ads-lead';
			} else if (txt.includes("SMM")){
				window.location.href = '/smm';
			} else if (txt.includes("IT-sales")){
				window.location.href = '/it-sales';
			} else if (txt.includes("Analyst")){
				window.location.href = '/analyst';
			} else if (txt.includes("Support")){
				window.location.href = '/support';
			} else if (txt.includes("Copywriting")){
				window.location.href = '/copywriting';
					// All 
			} else if (txt.includes("Все вакансии")){
				window.location.href = '/';	
			} else if (txt.includes("Избранное")){
				window.location.href = '/favorite';			
				}
	});
 });