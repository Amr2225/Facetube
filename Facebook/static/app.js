// DOM Elements
const model = document.getElementById('model');
const body = document.querySelector('body');
const sidebar = document.getElementById('second');

// Event Listeners
document.getElementById('ham').addEventListener('click', () =>{
    sidebar.classList.toggle('show');
});

document.getElementById('img').addEventListener('click', redirect)
document.getElementById('span').addEventListener('click', redirect)

document.getElementById('facetube').addEventListener('click', () =>{
  window.location.href = 'http://localhost:5000/facetube';
});

body.addEventListener('click', e =>{
  if (e.target.id != 'ham'){
    if (sidebar.classList.contains('show')){
      if (e.pageX > 150 || e.pageY > 320 || e.pageY < 220){
        sidebar.classList.remove('show');
      }
    }
  }
  if (e.pageX > ((window.innerWidth/2)+200) || e.pageX < ((window.innerWidth/2)-200) || e.pageY > ((window.innerHeight/2)+200) || e.pageY < ((window.innerHeight/2)-200)){
        close();
  }
});

//Funtion for redirecting when clicked on the images
function redirect(){
  window.location.href = 'http://localhost:5000/facetube/facebook';
}

document.getElementById('close').addEventListener('click', close);

// Function for closing the model
function close(){
   model.classList.remove('active');
   body.classList.remove('fade');
   model.parentElement.classList.remove('overflow');
}

// Media Query
let x = window.matchMedia("(max-width: 400px)");
if (x.matches){
    // console.log('matches')
    document.querySelector('body').addEventListener('click', e =>{
	    if (e.pageX > ((window.innerWidth/2)+100) || e.pageX < ((window.innerWidth/2)-100) || e.pageY > ((window.innerHeight/2)+125) || e.pageY < ((window.innerHeight/2)-125)){
	        close();
	    }
	});
}