var _JUPYTERLAB;(()=>{"use strict";var e,r,t,a,o,n,i,c,l,u,s,f,d,p,h,v,y,b,m={5116:(e,r,t)=>{var a={"./index":()=>Promise.all([t.e(217),t.e(216),t.e(784)]).then((()=>()=>t(3106))),"./extension":()=>Promise.all([t.e(217),t.e(480)]).then((()=>()=>t(4480)))},o=(e,r)=>(t.R=r,r=t.o(a,e)?a[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),n=(e,r)=>{if(t.S){var a=t.S.default,o="default";if(a&&a!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[o]=e,t.I(o,r)}};t.d(r,{get:()=>o,init:()=>n})}},g={};function w(e){var r=g[e];if(void 0!==r)return r.exports;var t=g[e]={id:e,loaded:!1,exports:{}};return m[e].call(t.exports,t,t.exports,w),t.loaded=!0,t.exports}w.m=m,w.c=g,w.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return w.d(r,{a:r}),r},w.d=(e,r)=>{for(var t in r)w.o(r,t)&&!w.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},w.f={},w.e=e=>Promise.all(Object.keys(w.f).reduce(((r,t)=>(w.f[t](e,r),r)),[])),w.u=e=>e+"."+{58:"fde94a378ce516996dfe",69:"766fd55b470a4fa78bae",106:"268f5e0137066962d5de",142:"c313db5f79c09f004811",216:"3f1591f76a687e846cfd",217:"16fb3ca21db4b2325549",480:"c195c498c04af8ea2b53",578:"09ce99ddc2c07047f895",703:"293e1b765e744ce5b028",784:"a96990dfcff5e7b93a11",878:"afc7af901c2338934a68",981:"3153022aa852d392db21"}[e]+".js?v="+{58:"fde94a378ce516996dfe",69:"766fd55b470a4fa78bae",106:"268f5e0137066962d5de",142:"c313db5f79c09f004811",216:"3f1591f76a687e846cfd",217:"16fb3ca21db4b2325549",480:"c195c498c04af8ea2b53",578:"09ce99ddc2c07047f895",703:"293e1b765e744ce5b028",784:"a96990dfcff5e7b93a11",878:"afc7af901c2338934a68",981:"3153022aa852d392db21"}[e],w.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),w.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="jupyter-cytoscape:",w.l=(t,a,o,n)=>{if(e[t])e[t].push(a);else{var i,c;if(void 0!==o)for(var l=document.getElementsByTagName("script"),u=0;u<l.length;u++){var s=l[u];if(s.getAttribute("src")==t||s.getAttribute("data-webpack")==r+o){i=s;break}}i||(c=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,w.nc&&i.setAttribute("nonce",w.nc),i.setAttribute("data-webpack",r+o),i.src=t),e[t]=[a];var f=(r,a)=>{i.onerror=i.onload=null,clearTimeout(d);var o=e[t];if(delete e[t],i.parentNode&&i.parentNode.removeChild(i),o&&o.forEach((e=>e(a))),r)return r(a)},d=setTimeout(f.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=f.bind(null,i.onerror),i.onload=f.bind(null,i.onload),c&&document.head.appendChild(i)}},w.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},w.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),(()=>{w.S={};var e={},r={};w.I=(t,a)=>{a||(a=[]);var o=r[t];if(o||(o=r[t]={}),!(a.indexOf(o)>=0)){if(a.push(o),e[t])return e[t];w.o(w.S,t)||(w.S[t]={});var n=w.S[t],i="jupyter-cytoscape",c=(e,r,t,a)=>{var o=n[e]=n[e]||{},c=o[r];(!c||!c.loaded&&(!a!=!c.eager?a:i>c.from))&&(o[r]={get:t,from:i,eager:!!a})},l=[];return"default"===t&&(c("cytoscape-cola","2.5.0",(()=>w.e(703).then((()=>()=>w(703))))),c("cytoscape-dagre","2.3.2",(()=>w.e(142).then((()=>()=>w(9142))))),c("cytoscape-klay","3.1.4",(()=>w.e(878).then((()=>()=>w(3878))))),c("cytoscape-popper","1.0.7",(()=>Promise.all([w.e(981),w.e(578)]).then((()=>()=>w(578))))),c("cytoscape","3.20.0",(()=>w.e(58).then((()=>()=>w(9058))))),c("jupyter-cytoscape","1.3.0",(()=>Promise.all([w.e(217),w.e(216),w.e(784)]).then((()=>()=>w(3106))))),c("tippy.js","5.2.1",(()=>Promise.all([w.e(981),w.e(69)]).then((()=>()=>w(7584)))))),e[t]=l.length?Promise.all(l).then((()=>e[t]=1)):1}}})(),(()=>{var e;w.g.importScripts&&(e=w.g.location+"");var r=w.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");t.length&&(e=t[t.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),w.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),a=t[1]?r(t[1]):[];return t[2]&&(a.length++,a.push.apply(a,r(t[2]))),t[3]&&(a.push([]),a.push.apply(a,r(t[3]))),a},a=(e,r)=>{e=t(e),r=t(r);for(var a=0;;){if(a>=e.length)return a<r.length&&"u"!=(typeof r[a])[0];var o=e[a],n=(typeof o)[0];if(a>=r.length)return"u"==n;var i=r[a],c=(typeof i)[0];if(n!=c)return"o"==n&&"n"==c||"s"==c||"u"==n;if("o"!=n&&"u"!=n&&o!=i)return o<i;a++}},o=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var a=1,n=1;n<e.length;n++)a--,t+="u"==(typeof(c=e[n]))[0]?"-":(a>0?".":"")+(a=2,c);return t}var i=[];for(n=1;n<e.length;n++){var c=e[n];i.push(0===c?"not("+l()+")":1===c?"("+l()+" || "+l()+")":2===c?i.pop()+" "+i.pop():o(c))}return l();function l(){return i.pop().replace(/^\((.+)\)$/,"$1")}},n=(e,r)=>{if(0 in e){r=t(r);var a=e[0],o=a<0;o&&(a=-a-1);for(var i=0,c=1,l=!0;;c++,i++){var u,s,f=c<e.length?(typeof e[c])[0]:"";if(i>=r.length||"o"==(s=(typeof(u=r[i]))[0]))return!l||("u"==f?c>a&&!o:""==f!=o);if("u"==s){if(!l||"u"!=f)return!1}else if(l)if(f==s)if(c<=a){if(u!=e[c])return!1}else{if(o?u>e[c]:u<e[c])return!1;u!=e[c]&&(l=!1)}else if("s"!=f&&"n"!=f){if(o||c<=a)return!1;l=!1,c--}else{if(c<=a||s<f!=o)return!1;l=!1}else"s"!=f&&"n"!=f&&(l=!1,c--)}}var d=[],p=d.pop.bind(d);for(i=1;i<e.length;i++){var h=e[i];d.push(1==h?p()|p():2==h?p()&p():h?n(h,r):!p())}return!!p()},i=(e,r)=>{var t=w.S[e];if(!t||!w.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},c=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&a(e,r)?r:e),0)},l=(e,r,t,a)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+o(a)+")",u=(e,r,t,a)=>{var o=c(e,t);return n(a,o)||"undefined"!=typeof console&&console.warn&&console.warn(l(e,t,o,a)),f(e[t][o])},s=(e,r,t)=>{var o=e[r];return(r=Object.keys(o).reduce(((e,r)=>!n(t,r)||e&&!a(e,r)?e:r),0))&&o[r]},f=e=>(e.loaded=1,e.get()),p=(d=e=>function(r,t,a,o){var n=w.I(r);return n&&n.then?n.then(e.bind(e,r,w.S[r],t,a,o)):e(r,w.S[r],t,a,o)})(((e,r,t,a)=>(i(e,t),u(r,0,t,a)))),h=d(((e,r,t,a,o)=>{var n=r&&w.o(r,t)&&s(r,t,a);return n?f(n):o()})),v={},y={4217:()=>p("default","@jupyter-widgets/base",[,[1,4,0,0],[1,3],[1,2],[1,1,1,10],1,1,1]),1054:()=>h("default","cytoscape-cola",[1,2,3,0],(()=>w.e(703).then((()=>()=>w(703))))),3262:()=>h("default","cytoscape-dagre",[1,2,2,2],(()=>w.e(142).then((()=>()=>w(9142))))),4773:()=>h("default","cytoscape-popper",[1,1,0,6],(()=>Promise.all([w.e(981),w.e(578)]).then((()=>()=>w(578))))),7251:()=>h("default","tippy.js",[1,5,2,1],(()=>Promise.all([w.e(981),w.e(69)]).then((()=>()=>w(7584))))),8961:()=>h("default","cytoscape",[1,3,14,0],(()=>w.e(58).then((()=>()=>w(9058))))),9002:()=>h("default","cytoscape-klay",[1,3,1,3],(()=>w.e(878).then((()=>()=>w(3878)))))},b={106:[1054,3262,4773,7251,8961,9002],216:[1054,3262,4773,7251,8961,9002],217:[4217]},w.f.consumes=(e,r)=>{w.o(b,e)&&b[e].forEach((e=>{if(w.o(v,e))return r.push(v[e]);var t=r=>{v[e]=0,w.m[e]=t=>{delete w.c[e],t.exports=r()}},a=r=>{delete v[e],w.m[e]=t=>{throw delete w.c[e],r}};try{var o=y[e]();o.then?r.push(v[e]=o.then(t).catch(a)):t(o)}catch(e){a(e)}}))},(()=>{var e={146:0};w.f.j=(r,t)=>{var a=w.o(e,r)?e[r]:void 0;if(0!==a)if(a)t.push(a[2]);else if(/^21[67]$/.test(r))e[r]=0;else{var o=new Promise(((t,o)=>a=e[r]=[t,o]));t.push(a[2]=o);var n=w.p+w.u(r),i=new Error;w.l(n,(t=>{if(w.o(e,r)&&(0!==(a=e[r])&&(e[r]=void 0),a)){var o=t&&("load"===t.type?"missing":t.type),n=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+o+": "+n+")",i.name="ChunkLoadError",i.type=o,i.request=n,a[1](i)}}),"chunk-"+r,r)}};var r=(r,t)=>{var a,o,[n,i,c]=t,l=0;if(n.some((r=>0!==e[r]))){for(a in i)w.o(i,a)&&(w.m[a]=i[a]);c&&c(w)}for(r&&r(t);l<n.length;l++)o=n[l],w.o(e,o)&&e[o]&&e[o][0](),e[n[l]]=0},t=self.webpackChunkjupyter_cytoscape=self.webpackChunkjupyter_cytoscape||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})();var j=w(5116);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["jupyter-cytoscape"]=j})();