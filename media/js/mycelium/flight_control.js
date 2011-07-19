$(function(){
});



var ReadyList = [];	
$(document).ready(function () {
	if(ReadyList && (ReadyList instanceof Array)) {
		for (var a=0;a<ReadyList.length;a++) {
			ReadyList[a]();	
		}
	}
});
ReadyList.push(function() {
	var sEl,mEl,hEL,
	now = new Date(),
	sVal = now.getSeconds(),
	mVal = now.getMinutes(),
	hVal = now.getHours(),
	am = (hVal < 12)?(true):(false),
	tickCount = 0,
	pad = function(val) {
		var ret = '00' + val;
		return ret.substring(ret.length-2);
	},
	initFlip = function(el,val) {
		el.flip = true;
		el.flipCount = 1;
		$(el).addClass('ani1');
		$(el.ani).removeClass('hide');
		el.top.num.innerHTML = val;
	},
	checkFlip = function (el,val) {
		if(el.flip) {
			$(el).removeClass('ani'+el.flipCount);
			el.flipCount += el.flipDir;
			if(el.flipCount > 4) {
				el.flipDir = -1;
				el.flipCount = 4;
				$(el).addClass('ani'+el.flipCount);
				$(el.ani).removeClass('top').addClass('bottom');
				el.ani.num.innerHTML = val;
			}
			else if (el.flipCount == 0) {
				el.flipDir = 1;
				$(el.ani).removeClass('bottom').addClass('top').addClass('hide');
				el.btm.num.innerHTML = val;
				el.flip = false;
			}
			else {
				$(el).addClass('ani'+el.flipCount);
			}
		}
	},
	checkTime = function() {
		now = new Date();
		var nS = now.getSeconds(),
		nM = now.getMinutes(),
		nH = now.getHours();
		if (!sEl.flip && sVal != nS) {
			sVal = (++sVal < 60)?(sVal):(0); 
			initFlip(sEl,pad(sVal));
		}
		if (!mEl.flip && mVal != nM) {
			mVal = (++mVal < 60)?(mVal):(0); 
			initFlip(mEl,pad(mVal));
		}
		if (!hEl.flip && hVal != nH) {
			hVal = (++hVal < 24)?(hVal):(0);
			initFlip(hEl,hourVal(hVal));
			hEl.ani.ap.innerHTML = hEl.btm.ap.innerHTML = (hVal < 12)?('AM'):('PM');
		}
		
	},
	tick = function() {
		checkFlip(sEl,pad(sVal));
		checkFlip(mEl,pad(mVal));
		checkFlip(hEl,pad(hVal));
		checkTime();
	},
	tickTimer;
	if (window.location.search.match(/reset/)) {
		sVal = mVal = hVal = 0;
		ap = false;
	}
	$('#sec,#min,#hou').each(function() {
		this.ani = $('.front',this).get(0);
		this.ani.num = $('span',this.ani).get(0);
		this.top = $('.top.back',this).get(0);
		this.top.num = $('span',this.top).get(0);
		this.btm = $('.bottom.back',this).get(0);
		this.btm.num = $('span',this.btm).get(0);
		this.flip = false;
		this.flipCount = 0;
		this.flipDir = 1;
		if (this.id == 'hou') {
			hEl = this;
			this.ani.num.innerHTML = this.top.num.innerHTML = this.btm.num.innerHTML = hourVal(hVal);
			this.ani.ap = $('.ap',this.ani).get(0);
			this.btm.ap = $('.ap',this.btm).get(0);
			this.ani.ap.innerHTML = this.btm.ap.innerHTML = (am)?('AM'):('PM');
		}
		if (this.id == 'min') {
			mEl = this;
			this.ani.num.innerHTML = this.top.num.innerHTML = this.btm.num.innerHTML = pad(mVal);
		}
		if (this.id == 'sec') {
			sEl = this;
			this.ani.num.innerHTML = this.top.num.innerHTML = this.btm.num.innerHTML = pad(sVal);
		}
	});
	tickTimer = window.setInterval(tick,50);