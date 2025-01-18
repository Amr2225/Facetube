addEventListener('load', getbox);

function getbox () {
	addEventListener('beforeunload', clear);  // Page Leave detection
		async function clear(){
			await fetch('/clear')
		}
	// Fetching the Data
	fetch('/facetube/youtube/videos', {headers: {'Accpet': '*/*, application/json'}}).then(res => res.json()).then(data => {
		if (data == []){  // Checks if the data is null
			return getbox()
		}
		let box = '';  
		data.forEach(value => {
			box += `  
			<div class="holder">
				<img src="${value.thumbnail_url}">
				<h5>${value.duration}</h5>
			</div>
				<h4>${value.name}</h4>
				<div class="control">
					<div class="left-content">
						<p>Views</p>
						<p>${value.views}</p>

						<p>Date</p>
						<p>${value.date}</p>
					</div>
					<div class="right-content">
						<p>Size</p>
						<p>${value.size}</p>
						<a href="/facetube/youtube/videos/${value.id}" download="${value.name}" class="btn download">Download</a>
					</div>
				</div>
			`
		});
		document.getElementById('box').innerHTML += box; // Adding the box variable to the DOM
	});
}