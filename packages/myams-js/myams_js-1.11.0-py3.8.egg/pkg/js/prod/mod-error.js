!function(e,t){"function"==typeof define&&define.amd?define(["exports","jsrender"],t):"undefined"!=typeof exports?t(exports,require("jsrender")):(t(t={},e.jsrender),e.modError=t)}("undefined"!=typeof globalThis?globalThis:"undefined"!=typeof self?self:this,function(e,t){"use strict";function d(e,t){var r;if("undefined"==typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(r=function(e,t){if(!e)return;if("string"==typeof e)return i(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return i(e,t)}(e))||t&&e&&"number"==typeof e.length){r&&(e=r);var n=0,t=function(){};return{s:t,n:function(){return n>=e.length?{done:!0}:{done:!1,value:e[n++]}},e:function(e){throw e},f:t}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var a,o=!0,s=!1;return{s:function(){r=e[Symbol.iterator]()},n:function(){var e=r.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||null==r.return||r.return()}finally{if(s)throw a}}}}function i(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}Object.defineProperty(e,"__esModule",{value:!0}),e.error=void 0;var c=MyAMS.$,y=c.templates({markup:'\n\t<div class="alert alert-{{:status}}" role="alert">\n\t\t<button type="button" class="close" data-dismiss="alert" \n\t\t\t\taria-label="{{*: MyAMS.i18n.BTN_CLODE }}">\n\t\t\t<i class="fa fa-times" aria-hidden="true"></i>\t\n\t\t</button>\n\t\t{{if header}}\n\t\t<h5 class="alert-heading">{{:header}}</h5>\n\t\t{{/if}}\n\t\t{{if message}}\n\t\t<p>{{:message}}</p>\n\t\t{{/if}}\n\t\t{{if messages}}\n\t\t<ul>\n\t\t{{for messages}}\n\t\t\t<li>\n\t\t\t\t{{if header}}<strong>{{:header}} :</strong>{{/if}}\n\t\t\t\t{{:message}}\n\t\t\t</li>\n\t\t{{/for}}\n\t\t</ul>\n\t\t{{/if}}\n\t\t{{if widgets}}\n\t\t<ul>\n\t\t{{for widgets}}\n\t\t\t<li>\n\t\t\t\t{{if header}}<strong>{{:header}} :</strong>{{/if}}\n\t\t\t\t{{:message}}\n\t\t\t</li>\n\t\t{{/for}}\n\t\t</ul>\n\t\t{{/if}}\n\t</div>',allowCode:!0}),r={showErrors:function(f,u){return new Promise(function(e,t){("string"==typeof u?MyAMS.require("i18n","alert").then(function(){MyAMS.alert.alert({parent:f,status:"danger",header:MyAMS.i18n.ERROR_OCCURED,message:u})}):c.isArray(u)?MyAMS.require("i18n","alert").then(function(){MyAMS.alert.alert({parent:f,status:"danger",header:MyAMS.i18n.ERRORS_OCCURED,message:u})}):MyAMS.require("i18n","ajax","alert","form").then(function(){MyAMS.form.clearAlerts(f);var e=[],t=d(u.messages||[]);try{for(t.s();!(r=t.n()).done;){var r=r.value;"string"==typeof r?e.push({header:null,message:r}):e.push(r)}}catch(e){t.e(e)}finally{t.f()}var n=d(u.widgets||[]);try{for(n.s();!(a=n.n()).done;){var a=a.value;e.push({header:a.label,message:a.message})}}catch(e){n.e(e)}finally{n.f()}var o={status:"danger",header:u.header||(1<e.length?MyAMS.i18n.ERRORS_OCCURED:MyAMS.i18n.ERROR_OCCURED),message:u.error||null,messages:e};c(y.render(o)).prependTo(f);var s=d(u.widgets||[]);try{for(s.s();!(l=s.n()).done;){var i=l.value,l=void 0;(l=i.id?c("#".concat(i.id),f):c('[name="'.concat(i.name,'"]'),f)).exists()&&MyAMS.form.setInvalid(f,l,i.message)}}catch(e){s.e(e)}finally{s.f()}MyAMS.ajax.check(c.fn.scrollTo,"".concat(MyAMS.env.baseURL,"../ext/jquery-scrollto").concat(MyAMS.env.extext,".js")).then(function(){var e=f.parents(".modal-body");e.exists()||(e=c("#main")),e.scrollTo(f,{offset:-15})})})).then(e,t)})},showHTTPError:function(r){return new Promise(function(e,t){MyAMS.require("alert").then(function(){MyAMS.alert.messageBox({status:"error",title:r.title,message:r.message,hideTimestamp:!1,timeout:0})}).then(e,t)})}};e.error=r,window.MyAMS&&(MyAMS.env.bundle?MyAMS.config.modules.push("error"):(MyAMS.error=r,console.debug("MyAMS: error module loaded...")))});