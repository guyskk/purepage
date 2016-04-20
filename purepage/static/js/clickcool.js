var clickCoolObj = function(){
	this.dom;
  this.timer;
  this.height;
  this.width;
  this.left;
  this.top;
}
clickCoolObj.prototype.init = function(left,top){
  this.dom = document.createElement('div');
  this.dom.className = 'round';
  this.height = 0;
  this.width = 0;
  drawCool(left,top);
}
function drawCool(left,top){
  document.body.appendChild(clickCool.dom);
  clickCool.timer = setInterval(function(){
    clickCool.dom.style.left = left + 'px';
    clickCool.dom.style.top = top + 'px';
    clickCool.height += 2;
    clickCool.width += 2;
    console.log(clickCool.height);
    clickCool.dom.style.height = clickCool.height + 'px';
    clickCool.dom.style.width = clickCool.width + 'px';
    if(clickCool.height >= 50 || clickCool.width >= 50){
      clearInterval(clickCool.timer);
    }
  },30);
}