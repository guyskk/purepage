var sideBarObj = function(){
	this.dom;
	this.show;
	this.btn;
	this.menu;
	this.close;
	this.clickBox;
}
sideBarObj.prototype.init = function(){
	this.dom = getDom('sideBar');
	this.show = false;
	this.btn = getDom('change');
	this.menu = getDom('menu');
	this.close = getDom('close');
	this.clickBox = getDom('clickBox');
	this.btn.addEventListener('click',changeSide,false);
	this.clickBox.addEventListener('click',hideSide,false);
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
	sideBar.menu.style.display = 'block';
	sideBar.close.style.display = 'none';
	sideBar.clickBox.style.display = 'none';
}
function showSide(){
	sideBar.dom.className = 'show';
	sideBar.show = true;
	if(window.innerWidth <= 1250){
		sideBar.btn.style.marginLeft = '0px';
		sideBar.clickBox.style.display = 'block';
	}
	else{
		sideBar.btn.style.marginLeft = '240px';
	}
	sideBar.menu.style.display = 'none';
	sideBar.close.style.display = 'block';
}