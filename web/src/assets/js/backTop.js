//返回顶部
var backTopObj = function(){
	this.demo;
	this.bTop;
	this.timer;
	this.speed = 0;
	this.isShowTop = false;
	this.isHideTop = false;
	this.hideTopTimer;
}
backTopObj.prototype.init = function(){
	this.demo = document.getElementById('backTop');
	if(document.documentElement.scrollTop >= 500 || document.body.scrollTop >= 500){
		this.showTop();
	}
	else{
		this.hideTop();
	}
	this.demo.addEventListener('click',back,false);
	document.body.addEventListener('mousewheel',function(){clearInterval(backTop.timer);},false);
}
backTopObj.prototype.showTop = function(){
	this.isShowTop = false;
	this.isHideTop = true;
	clearInterval(this.hideTopTimer);
	this.demo.style.display = 'block';
	this.demo.style.opacity = 1;
	this.demo.style.transition = 'opacity 0.7s';
}
backTopObj.prototype.hideTop = function(){
	this.isShowTop = true;
	this.isHideTop = false;
	this.demo.style.opacity = 0;
	this.demo.style.transition = 'opacity 0.7s';
	this.hideTopTimer = setInterval(function(){
		backTop.demo.style.display = 'none';
		clearInterval(this.hideTopTimer);
	},1000);
}
function back(){
	clearInterval(backTop.timer);
	backTop.timer = setInterval(function(){
		backTop.bTop = document.documentElement.scrollTop || document.body.scrollTop;
		backTop.speed = Math.floor(- backTop.bTop / 6);
		document.documentElement.scrollTop = document.body.scrollTop = backTop.bTop + backTop.speed;
		if(backTop.bTop <= 0){
			clearInterval(backTop.timer);
		}
	},30);
}
//返回顶部按钮和导航栏的显示和隐藏
backTopObj.prototype.backTopBtn = function(){
	if(document.documentElement.scrollTop >= 500 || document.body.scrollTop >= 500){
		if(this.isShowTop){
			this.showTop();
		}
	}
	else if(document.documentElement.scrollTop <= 500 || document.body.scrollTop <= 500){
		if(this.isHideTop){
			this.hideTop();
		}
	}
	else{
		return;
	}
}
var backTop = new backTopObj();
backTop.init();
window.onscroll = function(){
	backTop.backTopBtn();
}