var sideBar;

window.onload = function(){
	load();
	if(window.innerWidth >= 1250){
		showSide();
	}
	else{
		hideSide();
	}
}

function load(){
	sideBar = new sideBarObj();
	sideBar.init();
}

window.addEventListener('resize',function(){
	if(window.innerWidth >= 1250){
		showSide();
	}
	else{
		hideSide();
	}
})
window.addEventListener('scroll',function(){
	console.log(document.body.scrollTop);
	if(document.body.scrollTop >= 100){
		getDom('blogTitleBtns').className = 'showShadow';
	}
	else{
		getDom('blogTitleBtns').className = 'none';
	}
})