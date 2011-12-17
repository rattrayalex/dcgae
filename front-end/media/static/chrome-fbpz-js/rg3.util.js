/**
 * RG3 FB Photo Zoom
 * Author: Regis Gaughan, III
 * Email:  regis.gaughan@gmail.com
 * Web:    http://regisgaughan.com
 * (c) Copyright 2011. All Right Reserved
 */
var RG3=RG3||{};RG3.util=RG3.util||{newElement:function(c,a,d){d=d||window.document;var b=d.createElement(c);if(a){this.setProperties(b,a)}return b},setProperties:function(c,b){for(var a in b){this.setProperty(c,a,b[a])}},setProperty:function(b,a,c){if((a=="style"||a=="styles")&&typeof(c)=="object"){return RG3.util.setStyles(b,c)}else{if(a=="html"){a="innerHTML"}else{if(a=="text"){a="textContent"}}}return b[(a=="class"?"className":a)]=c},camelCase:function(a){return a.replace(/-\D/g,function(b){return b.charAt(1).toUpperCase()})},setStyles:function(b,c){for(var a in c){this.setStyle(b,a,c[a])}return b},setStyle:function(a,c,b){if(c=="opacity"){if(a.style.opacity!==undefined){a.style.opacity=b}else{if(a.style.MozOpacity!==undefined){a.style.MozOpacity=b}else{if(a.style.msFilter!==undefined){a.style.msFilter="progid:DXImageTransform.Microsoft.Alpha(Opacity="+(b*100)+")"}else{if(a.style.filter!==undefined){a.style.filter="alpha(opacity="+(b*100)+")"}}}}}else{if(c=="box-shadow"){this.setStyle(a,"-moz-box-shadow",b);this.setStyle(a,"-webkit-box-shadow",b);a.style[this.camelCase(c)]=b;return a}else{if(c=="float"){c="cssFloat"}a.style[this.camelCase(c)]=b}}return a},getEvent:function(a){return !a?a=window.event:a},preventEventDefault:function(a){a=this.getEvent(a);if(a){if(a.preventDefault){a.preventDefault()}else{a.returnValue=false}}return false},getEventTarget:function(a){if(a.target){targ=a.target}else{if(a.srcElement){targ=a.srcElement}}if(targ.nodeType==3){targ=targ.parentNode}return targ},addEvent:function(b,c,a){if(b.addEventListener){b.addEventListener(c,a,false)}else{if(window.attachEvent){b.attachEvent("on"+c,a)}else{b["on"+c]=a}}},removeEvent:function(b,c,a){if(b.removeEventListener){b.removeEventListener(c,a,false)}else{if(window.detachEvent){b.detachEvent("on"+c,a)}else{b["on"+c]=a}}},splat:function(a){return(typeof(a))?((!a.push&&!a.callee)?[a]:a):[]},extendArray:function(d,c){for(var b=0,a=c.length;b<a;b++){d.push(c[b])}return d},bind:function(c,b,a){return this.createFn(b,{bind:c,"arguments":a})},createFn:function(c,b){var a=c;b=b||{};return function(e){var d=b.arguments,f;d=(d!=undefined)?RG3.util.splat(d):arguments;if(b.event){d=RG3.util.extendArray(d,[e||window.event])}f=function(){return a.apply(b.bind||null,d)};return f()}},setOptions:function(b,a){a=a||{};for(var c in b){b[c]=(typeof(a[c])!=="undefined")?a[c]:b[c]}return b},toQueryString:function(b){b=b||{};var c="?";for(var a in b){c+=a+"="+b[a]+"&"}return c.replace(/\&$/,"")},merge:function(c,b){var a;for(a in b){c[a]=b[a]}return c}};RG3.Request=function(a){return this.init(a)};RG3.Request.prototype={options:{method:"get",url:null,data:null,onSuccess:function(){},onError:function(){}},init:function(a){RG3.util.setOptions(this.options,a);this.binds={onReadyStateChange:RG3.util.bind(this,this.onReadyStateChange)};this.xhr=new XMLHttpRequest()},onReadyStateChange:function(){if(this.xhr.readyState==4){if(this.xhr.status>=200&&this.xhr.status<300){this.options.onSuccess(JSON.parse(this.xhr.responseText))}else{this.options.onError(JSON.parse(this.xhr.responseText))}}},send:function(){this.xhr.onreadystatechange=this.binds.onReadyStateChange;this.xhr.open(this.options.method.toUpperCase(),this.options.url+RG3.util.toQueryString(this.options.data),true);this.xhr.send()}};