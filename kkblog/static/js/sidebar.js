var sideBarObj = function(){
	this.dom;
	this.show;
	this.btn;
}
sideBarObj.prototype.init = function(){
	this.dom = getDom('sideBar');
	this.show = true;
	this.btn = getDom('change');
	this.btn.addEventListener('click',changeSide,false);
	changeSide();
}
function changeSide(){
	if(sideBar.show){
		hideSide();
	}
	else{
		showSide();
	}
}
function hideSide(){
	sideBar.dom.className = 'hide';
	sideBar.show = false;
	sideBar.btn.style.marginLeft = '0px';
}
function showSide(){
	sideBar.dom.className = 'show';
	sideBar.show = true;
	sideBar.btn.style.marginLeft = '240px';
}