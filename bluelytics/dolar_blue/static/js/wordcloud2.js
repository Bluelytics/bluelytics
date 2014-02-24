"use strict"
window.setImmediate||(window.setImmediate=function(){return window.msSetImmediate||window.webkitSetImmediate||window.mozSetImmediate||window.oSetImmediate||function(){if(!window.postMessage||!window.addEventListener)return null
var t=[void 0],e="zero-timeout-message",a=function(a){var r=t.length
return t.push(a),window.postMessage(e+r.toString(36),"*"),r}
return window.addEventListener("message",function(a){if("string"==typeof a.data&&a.data.substr(0,e.length)===e){a.stopImmediatePropagation()
var r=parseInt(a.data.substr(e.length),36)
t[r]&&(t[r](),t[r]=void 0)}},!0),window.clearImmediate=function(e){t[e]&&(t[e]=void 0)},a}()||function(t){window.setTimeout(t,0)}}()),window.clearImmediate||(window.clearImmediate=function(){return window.msClearImmediate||window.webkitClearImmediate||window.mozClearImmediate||window.oClearImmediate||function(t){window.clearTimeout(t)}}()),function(t){var e=function(){var t=document.createElement("canvas")
if(!t||!t.getContext)return!1
var e=t.getContext("2d")
return e.getImageData?e.fillText?Array.prototype.some?Array.prototype.push?!0:!1:!1:!1:!1}(),a=function(){if(e){for(var t,a,r=document.createElement("canvas").getContext("2d"),o=20;o;){if(r.font=o.toString(10)+"px sans-serif",r.measureText("Ｗ").width===t&&r.measureText("m").width===a)return o+1
t=r.measureText("Ｗ").width,a=r.measureText("m").width,o--}return 0}}(),r=function(t){for(var e,a,r=t.length;r;e=Math.floor(Math.random()*r),a=t[--r],t[r]=t[e],t[e]=a);return t},o=function(t,o){if(e){Array.isArray(t)||(t=[t]),t.forEach(function(e,a){if("string"==typeof e){if(t[a]=document.getElementById(e),!t[a])throw"The element id specified is not found."}else if(!e.tagName&&!e.appendChild)throw"You must pass valid HTML elements, or ID of the element."})
var n={list:[],fontFamily:'"Trebuchet MS", "Heiti TC", "微軟正黑體", "Arial Unicode MS", "Droid Fallback Sans", sans-serif',fontWeight:"normal",color:"random-dark",minSize:0,weightFactor:1,clearCanvas:!0,backgroundColor:"#fff",gridSize:8,origin:null,drawMask:!1,maskColor:"rgba(255,0,0,0.3)",maskGapWidth:.3,wait:0,abortThreshold:0,abort:function(){},minRotation:-Math.PI/2,maxRotation:Math.PI/2,shuffle:!0,rotateRatio:.1,shape:"circle",ellipticity:.65,hover:null,click:null}
if(o)for(var i in o)i in n&&(n[i]=o[i])
if("function"!=typeof n.weightFactor){var f=n.weightFactor
n.weightFactor=function(t){return t*f}}if("function"!=typeof n.shape)switch(n.shape){case"circle":default:n.shape="circle"
break
case"cardioid":n.shape=function(t){return 1-Math.sin(t)}
break
case"diamond":case"square":n.shape=function(t){var e=t%(2*Math.PI/4)
return 1/(Math.cos(e)+Math.sin(e))}
break
case"triangle-forward":n.shape=function(t){var e=t%(2*Math.PI/3)
return 1/(Math.cos(e)+Math.sqrt(3)*Math.sin(e))}
break
case"triangle":case"triangle-upright":n.shape=function(t){var e=(t+3*Math.PI/2)%(2*Math.PI/3)
return 1/(Math.cos(e)+Math.sqrt(3)*Math.sin(e))}
break
case"pentagon":n.shape=function(t){var e=(t+.955)%(2*Math.PI/5)
return 1/(Math.cos(e)+.726543*Math.sin(e))}
break
case"star":n.shape=function(t){var e=(t+.955)%(2*Math.PI/10)
return(t+.955)%(2*Math.PI/5)-2*Math.PI/10>=0?1/(Math.cos(2*Math.PI/10-e)+3.07768*Math.sin(2*Math.PI/10-e)):1/(Math.cos(e)+3.07768*Math.sin(e))}}n.gridSize=Math.max(n.gridSize,4)
var l,s,c,d,h,u,m,v=n.gridSize,g=v-n.maskGapWidth,w=Math.abs(n.maxRotation-n.minRotation),M=Math.min(n.maxRotation,n.minRotation)
switch(n.color){case"random-dark":m=function(){return"rgb("+Math.floor(128*Math.random()).toString(10)+","+Math.floor(128*Math.random()).toString(10)+","+Math.floor(128*Math.random()).toString(10)+")"}
break
case"random-light":m=function(){return"rgb("+Math.floor(128*Math.random()+128).toString(10)+","+Math.floor(128*Math.random()+128).toString(10)+","+Math.floor(128*Math.random()+128).toString(10)+")"}
break
default:"function"==typeof n.color&&(m=n.color)}var p,x=!1,b=[],I=function(t){var e=canvas.getBoundingClientRect(),a=t.clientX-e.left,r=t.clientY-e.top,o=Math.floor(a*(canvas.width/e.width)/v),n=Math.floor(r*(canvas.height/e.height)/v)
return b[o][n]},C=function(t){var e=I(t)
if(p!==e)return p=e,e?(n.hover(e.item,e.dimension,t),void 0):(n.hover(void 0,void 0,t),void 0)},T=function(t){var e=I(t)
e&&n.click(e.item,e.dimension,t)},S=[],k=function(t){if(S[t])return S[t]
var e=8*t,a=e,r=[]
for(0===t&&r.push([d[0],d[1],0]);a--;){var o=1
"circle"!==n.shape&&(o=n.shape(a/e*2*Math.PI)),r.push([d[0]+t*o*Math.cos(-a/e*2*Math.PI),d[1]+t*o*Math.sin(-a/e*2*Math.PI)*n.ellipticity,a/e*2*Math.PI])}return S[t]=r,r},y=function(){return n.abortThreshold>0&&(new Date).getTime()-u>n.abortThreshold},E=function(){return 0===n.rotateRatio?0:Math.random()>n.rotateRatio?0:0===w?M:M+Math.random()*w},R=function(t,e,r){var o=!1,i=n.weightFactor(e)
if(i<=n.minSize)return!1
var f=1
a>i&&(f=function(){for(var t=2;a>t*i;)t+=2
return t}())
var l=document.createElement("canvas"),s=l.getContext("2d",{willReadFrequently:!0})
s.font=n.fontWeight+" "+(i*f).toString(10)+"px "+n.fontFamily
var c=s.measureText(t).width/f,d=Math.max(i*f,s.measureText("m").width,s.measureText("Ｗ").width)/f,h=c+2*d,u=3*d,m=Math.ceil(h/v),g=Math.ceil(u/v)
h=m*v,u=g*v
var w=-c/2,M=.4*-d,p=Math.ceil((h*Math.abs(Math.sin(r))+u*Math.abs(Math.cos(r)))/v),x=Math.ceil((h*Math.abs(Math.cos(r))+u*Math.abs(Math.sin(r)))/v),b=x*v,I=p*v
l.setAttribute("width",b),l.setAttribute("height",I),o&&document.body.appendChild(l),s.save(),s.scale(1/f,1/f),s.translate(b*f/2,I*f/2),s.rotate(-r),s.font=n.fontWeight+" "+(i*f).toString(10)+"px "+n.fontFamily,s.fillStyle="#000",s.textBaseline="middle",s.fillText(t,w*f,(M+.5*i)*f),s.restore()
var C=s.getImageData(0,0,b,I).data
if(y())return!1
for(var T,S,k,E=[],R=x,P=[p/2,x/2,p/2,x/2];R--;)for(T=p;T--;){k=v
t:{for(;k--;)for(S=v;S--;)if(C[4*((T*v+k)*b+(R*v+S))+3]){E.push([R,T]),R<P[3]&&(P[3]=R),R>P[1]&&(P[1]=R),T<P[0]&&(P[0]=T),T>P[2]&&(P[2]=T),o&&(s.fillStyle="rgba(255, 0, 0, 0.5)",s.fillRect(R*v,T*v,v-.5,v-.5))
break t}o&&(s.fillStyle="rgba(0, 0, 255, 0.5)",s.fillRect(R*v,T*v,v-.5,v-.5))}}return o&&(s.fillStyle="rgba(0, 255, 0, 0.5)",s.fillRect(P[3]*v,P[0]*v,(P[1]-P[3]+1)*v,(P[2]-P[0]+1)*v)),{mu:f,occupied:E,bounds:P,gw:x,gh:p,fillTextOffsetX:w,fillTextOffsetY:M,fillTextWidth:c,fillTextHeight:d,fontSize:i}},P=function(t,e,a,r,o){for(var n=o.length;n--;){var i=t+o[n][0],f=e+o[n][1]
if(i>=s||f>=c||0>i||0>f||!l[i][f])return!1}return!0},F=function(e,a,r,o,i,f,l,s){var c,d=r.fontSize
c=m?m(o,i,d,f,l):n.color
var h,u=r.bounds
h={x:(e+u[3])*v,y:(a+u[0])*v,w:(u[1]-u[3]+1)*v,h:(u[2]-u[0]+1)*v},t.forEach(function(t){if(t.getContext){var i=t.getContext("2d"),f=r.mu
i.save(),i.scale(1/f,1/f),i.font=n.fontWeight+" "+(d*f).toString(10)+"px "+n.fontFamily,i.fillStyle=c,i.translate((e+r.gw/2)*v*f,(a+r.gh/2)*v*f),0!==s&&i.rotate(-s),i.textBaseline="middle",i.fillText(o,r.fillTextOffsetX*f,(r.fillTextOffsetY+.5*d)*f),i.restore()}else{var l=document.createElement("span"),h=""
h="rotate("+-s/Math.PI*180+"deg) ",1!==r.mu&&(h+="translateX(-"+r.fillTextWidth/4+"px) scale("+1/r.mu+")")
var u={position:"absolute",display:"block",font:n.fontWeight+" "+d*r.mu+"px "+n.fontFamily,left:(e+r.gw/2)*v+r.fillTextOffsetX+"px",top:(a+r.gh/2)*v+r.fillTextOffsetY+"px",width:r.fillTextWidth+"px",height:r.fillTextHeight+"px",color:c,lineHeight:d+"px",whiteSpace:"nowrap",transform:h,webkitTransform:h,msTransform:h,transformOrigin:"50% 40%",webkitTransformOrigin:"50% 40%",msTransformOrigin:"50% 40%"}
l.textContent=o
for(var m in u)l.style[m]=u[m]
t.appendChild(l)}})},z=function(t,e,a,r,o){t>=s||e>=c||0>t||0>e||(l[t][e]=!1,a&&ctx.fillRect(t*v,e*v,g,g),x&&(b[t][e]={item:o,dimension:r}))},W=function(t,e,a,r,o,i){var f=o.occupied,l=(v-n.maskGapWidth,n.drawMask)
l&&(ctx.save(),ctx.fillStyle=n.maskColor)
var s
if(x){var c=o.bounds
s={x:(t+c[3])*v,y:(e+c[0])*v,w:(c[1]-c[3]+1)*v,h:(c[2]-c[0]+1)*v}}for(var d=f.length;d--;)z(t+f[d][0],e+f[d][1],l,s,i)
l&&ctx.restore()},L=function(t){var e=t[0],a=t[1],o=E(),i=R(e,a,o)
if(!i)return!1
if(y())return!1
var f=i.bounds
if(f[1]-f[3]+1>s||f[2]-f[0]+1>c)return!1
for(var l=h+1;l--;){var d=k(h-l)
n.shuffle&&(d=[].concat(d),r(d))
var u=d.some(function(r){var n=Math.floor(r[0]-i.gw/2),f=Math.floor(r[1]-i.gh/2),s=i.gw,c=i.gh
return P(n,f,s,c,i.occupied)?(F(n,f,i,e,a,h-l,r[2],o),W(n,f,s,c,i,t),!0):!1})
if(u)return!0}return!1},O=function(e,a,r){return a?!t.some(function(t){var o=document.createEvent("CustomEvent")
return o.initCustomEvent(e,!0,a,r||{}),!t.dispatchEvent(o)},this):(t.forEach(function(t){var o=document.createEvent("CustomEvent")
o.initCustomEvent(e,!0,a,r||{}),t.dispatchEvent(o)},this),void 0)},D=function(){var e=t[0]
if(e.getContext)s=Math.floor(e.width/v),c=Math.floor(e.height/v)
else{var a=e.getBoundingClientRect()
s=Math.floor(a.width/v),c=Math.floor(a.height/v)}if(O("wordcloudstart",!0)){if(d=n.origin?[n.origin[0]/v,n.origin[1]/v]:[s/2,c/2],h=Math.floor(Math.sqrt(s*s+c*c)),l=[],!e.getContext||n.clearCanvas){t.forEach(function(t){if(t.getContext){var e=t.getContext("2d")
e.fillStyle=n.backgroundColor,e.clearRect(0,0,s*(v+1),c*(v+1)),e.fillRect(0,0,s*(v+1),c*(v+1))}else t.textContent="",t.style.backgroundColor=n.backgroundColor})
for(var r,o=s;o--;)for(l[o]=[],r=c;r--;)l[o][r]=!0}else{var i=document.createElement("canvas").getContext("2d")
i.fillStyle=n.backgroundColor,i.fillRect(0,0,1,1)
for(var r,f,m,g,w=i.getImageData(0,0,1,1).data,M=e.getContext("2d").getImageData(0,0,s*v,c*v).data,o=s;o--;)for(l[o]=[],r=c;r--;){m=v
t:for(;m--;)for(f=v;f--;)for(g=4;g--;)if(M[4*((r*v+m)*s*v+(o*v+f))+g]!==w[g]){l[o][r]=!1
break t}l[o][r]!==!1&&(l[o][r]=!0)}M=i=w=void 0}if(n.hover||n.click){x=!0
for(var o=s+1;o--;)b[o]=[]
n.hover&&e.addEventListener("mousemove",C),n.click&&e.addEventListener("click",T),e.addEventListener("wordcloudstart",function F(){e.removeEventListener("wordcloudstart",F),e.removeEventListener("mousemove",C),e.removeEventListener("click",T),p=void 0})}var I,S,g=0
0!==n.wait?(I=window.setTimeout,S=window.clearTimeout):(I=window.setImmediate,S=window.clearImmediate)
var k=function(e,a){t.forEach(function(t){t.addEventListener(e,a)},this)},E=function(e,a){t.forEach(function(t){t.removeEventListener(e,a)},this)},R=function z(){E("wordcloudstart",z),S(P)}
k("wordcloudstart",R),$("#canvas-container span").remove()
var P=I(function W(){if(g>=n.list.length)return S(P),O("wordcloudstop",!1),E("wordcloudstart",R),void 0
u=(new Date).getTime()
var t=L(n.list[g]),e=!O("wordclouddrawn",!0,{item:n.list[g],drawn:t})
return y()||e?(S(P),n.abort(),O("wordcloudabort",!1),O("wordcloudstop",!1),E("wordcloudstart",R),void 0):(g++,P=I(W,n.wait),void 0)},n.wait)}}
D()}}
o.isSupported=e,o.miniumFontSize=a,"function"==typeof define&&define.amd?define("wordcloud",[],function(){return o}):t.WordCloud=o}(this)
