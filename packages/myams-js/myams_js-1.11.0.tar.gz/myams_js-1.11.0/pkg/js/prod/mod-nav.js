!function(e,n){"function"==typeof define&&define.amd?define(["exports"],n):"undefined"!=typeof exports?n(exports):(n(n={}),e.modNav=n)}("undefined"!=typeof globalThis?globalThis:"undefined"!=typeof self?self:this,function(e){"use strict";function d(e,n){return function(e){if(Array.isArray(e))return e}(e)||function(e,n){if("undefined"==typeof Symbol||!(Symbol.iterator in Object(e)))return;var t=[],a=!0,o=!1,i=void 0;try{for(var r,s=e[Symbol.iterator]();!(a=(r=s.next()).done)&&(t.push(r.value),!n||t.length!==n);a=!0);}catch(e){o=!0,i=e}finally{try{a||null==s.return||s.return()}finally{if(o)throw i}}return t}(e,n)||s(e,n)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function u(e,n){var t;if("undefined"==typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(t=s(e))||n&&e&&"number"==typeof e.length){t&&(e=t);var a=0,n=function(){};return{s:n,n:function(){return a>=e.length?{done:!0}:{done:!1,value:e[a++]}},e:function(e){throw e},f:n}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,i=!0,r=!1;return{s:function(){t=e[Symbol.iterator]()},n:function(){var e=t.next();return i=e.done,e},e:function(e){r=!0,o=e},f:function(){try{i||null==t.return||t.return()}finally{if(r)throw o}}}}function s(e,n){if(e){if("string"==typeof e)return a(e,n);var t=Object.prototype.toString.call(e).slice(8,-1);return"Object"===t&&e.constructor&&(t=e.constructor.name),"Map"===t||"Set"===t?Array.from(e):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?a(e,n):void 0}}function a(e,n){(null==n||n>e.length)&&(n=e.length);for(var t=0,a=new Array(n);t<n;t++)a[t]=e[t];return a}function o(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}function i(e,n){for(var t=0;t<n.length;t++){var a=n[t];a.enumerable=a.enumerable||!1,a.configurable=!0,"value"in a&&(a.writable=!0),Object.defineProperty(e,a.key,a)}}function t(e,n,t){return n&&i(e.prototype,n),t&&i(e,t),e}Object.defineProperty(e,"__esModule",{value:!0}),e.linkClickHandler=M,e.nav=e.NavigationMenu=void 0;var f=MyAMS.$,r=function(){function n(e){o(this,n),this.props=e}return t(n,[{key:"render",value:function(){return f('<li class="header"></li>').text(this.props.header||"")}}]),n}(),m=function(){function e(){o(this,e)}return t(e,[{key:"render",value:function(){return f('<li class="divider"></li>')}}]),e}(),l=function(){function c(e){o(this,c),this.items=e}return t(c,[{key:"render",value:function(){var e=f("<div></div>"),n=u(this.items);try{for(n.s();!(a=n.n()).done;){var t=a.value;if(t.label){for(var a=f("<li></li>"),o=f("<a></a>").attr("href",t.href||"#").attr("title",t.label),i=0,r=Object.entries(t.attrs||{});i<r.length;i++){var s=d(r[i],2),l=s[0],s=s[1];o.attr(l,s)}t.icon&&f('<i class="fa-lg fa-fw mr-1"></i>').addClass(t.icon).appendTo(o),f('<span class="menu-item-parent"></span>').text(t.label).appendTo(o),t.badge&&f('<span class="badge ml-1 mr-3 float-right"></span>').addClass("bg-".concat(t.badge.status)).text(t.badge.value).appendTo(o),o.appendTo(a),t.items&&f("<ul></ul>").append(new c(t.items).render()).appendTo(a),a.appendTo(e)}else(new m).render().appendTo(e)}}catch(e){n.e(e)}finally{n.f()}return e.children()}}]),c}(),c=function(){function a(e,n,t){o(this,a),this.menus=e,this.parent=n,this.settings=t}return t(a,[{key:"getMenus",value:function(){var e=f("<ul></ul>"),n=u(this.menus);try{for(n.s();!(t=n.n()).done;){var t=t.value;void 0!==t.header&&e.append(new r(t).render()),e.append(new l(t.items).render())}}catch(e){n.e(e)}finally{n.f()}return e}},{key:"render",value:function(){var e=this.getMenus();this.init(e),this.parent.append(e)}},{key:"init",value:function(t){var s=this.settings;t.find("li").each(function(e,n){var t=f(n);0<t.find("ul").length&&(n=t.find("a:first"),(t=f('<b class="collapse-sign">'.concat(s.closedSign,"</b>"))).on("click",function(e){e.preventDefault()}),n.append(t),"#"===n.attr("href")&&n.click(function(){return!1}))}),t.find("li.active").each(function(e,n){var t=f(n).parents("ul"),n=t.parent("li");t.slideDown(s.speed),n.find("b:first").html(s.openedSign),n.addClass("open")}),t.find("li a").on("click",function(e){var o,i,r,n=f(e.currentTarget);n.hasClass("active")||(n.parents("li").removeClass("active"),o=n.attr("href").replace(/^#/,""),i=n.parent().find("ul"),s.accordion&&(r=n.parent().parents("ul"),t.find("ul:visible").each(function(e,t){var n,a=!0;r.each(function(e,n){if(n===t)return a=!1}),a&&i!==t&&(n=f(t),!o&&n.hasClass("active")||n.slideUp(s.speed,function(){n.parent("li").removeClass("open").find("b:first").delay(s.speed).html(s.closedSign)}))})),e=n.parent().find("ul:first"),o||!e.is(":visible")||e.hasClass("active")?e.slideDown(s.speed,function(){n.parent("li").addClass("open").find("b:first").delay(s.speed).html(s.openedSign)}):e.slideUp(s.speed,function(){n.parent("li").removeClass("open").find("b:first").delay(s.speed).html(s.closedSign)}))})}}]),a}();e.NavigationMenu=c;var n=!1,p=null;function h(e){location&&e.startsWith("#")?e!==location.hash&&(location.hash=e):location.toString()===e?location.reload():window.location=e}function M(l){return new Promise(function(n,t){var e,a,o,i,r=f(l.currentTarget),s=r.data("ams-disabled-handlers");!0!==s&&"click"!==s&&"all"!==s&&(!(i=r.attr("href")||r.data("ams-url"))||i.startsWith("javascript:")||r.attr("target")||!0===r.data("ams-context-menu")||(l.preventDefault(),l.stopPropagation(),e=0<=i.indexOf("?")?(a=(e=i.split("?"))[0],e[1].unserialize()):void(a=i),"function"==typeof(a=MyAMS.core.getFunctionByName(a))&&(i=a(r,e)),i?"function"==typeof i?n(i(r,e)):(i=i.replace(/%23/,"#"),l.ctrlKey?(window.open&&window.open(i),n()):(o=r.data("ams-target")||r.attr("target"))?"_blank"===o?(window.open&&window.open(i),n()):"_top"===o?(window.location=i,n()):MyAMS.form?MyAMS.form.confirmChangedForm().then(function(e){"success"===e&&MyAMS.skin&&MyAMS.skin.loadURL(i,o,r.data("ams-link-options"),r.data("ams-link-callback")).then(n,t)}):MyAMS.skin&&MyAMS.skin.loadURL(i,o,r.data("ams-link-options"),r.data("ams-link-callback")).then(n,t):MyAMS.form?MyAMS.form.confirmChangedForm().then(function(e){"success"===e&&h(i)}).then(n):(h(i),n())):n(null)))})}var y={init:function(){n||(n=!0,f.fn.extend({navigationMenu:function(e){var n,t,a,o,i,r=this;0!==this.length&&(t={accordion:!1!==(n=this.data()).amsMenuAccordion,speed:200},MyAMS.config.useSVGIcons?(a=FontAwesome.findIconDefinition({iconName:"angle-down"}),o=FontAwesome.findIconDefinition({iconName:"angle-up"}),f.extend(t,{closedSign:"<em data-fa-i2svg>".concat(FontAwesome.icon(a).html,"</em>"),openedSign:"<em data-fa-i2svg>".concat(FontAwesome.icon(o).html,"</em>")})):f.extend(t,{closedSign:'<em class="fa fa-angle-down"></em>',openedSign:'<em class="fa fa-angle-up"></em>'}),i=f.extend({},t,e),n.amsMenuConfig?MyAMS.require("ajax","skin").then(function(){MyAMS.ajax.get(n.amsMenuConfig).then(function(e){new(MyAMS.core.getObject(n.amsMenuFactory)||c)(e,f(r),i).render(),MyAMS.skin.checkURL()})}):(e=f("ul",this),new c(null,f(this),i).init(e)))}}),MyAMS.config.ajaxNav&&(f(document).on("click",'a[href="#"]',function(e){e.preventDefault()}),f(document).on("click",'a[href!="#"]:not([data-toggle]), [data-ams-url]:not([data-toggle])',function(e){if(!f(e).data("ams-click-handler"))return M(e)}),f(document).on("click",'a[target="_blank"]',function(e){e.preventDefault();e=f(e.currentTarget);window.open&&window.open(e.attr("href")),MyAMS.stats&&MyAMS.stats.logEvent(e.data("ams-stats-category")||"Navigation",e.data("ams-stats-action")||"External",e.data("ams-stats-label")||e.attr("href"))}),f(document).on("click",'a[target="_top"]',function(n){n.preventDefault(),MyAMS.form&&MyAMS.form.confirmChangedForm().then(function(e){"success"===e&&(window.location=f(n.currentTarget).attr("href"))})}),f(document).on("click",".nav-tabs a[data-toggle=tab]",function(e){if(f(e.currentTarget).parent("li").hasClass("disabled"))return e.stopPropagation(),e.preventDefault(),!1}),f(document).on("show.bs.tab",function(e){var n=f(e.target);n.exists()&&"A"!==n.get(0).tagName&&(n=f("a[href]",n));var t=n.data();t&&t.amsUrl&&(t.amsTabLoaded||(n.append('<i class="fa fa-spin fa-cog ml-1"></i>'),MyAMS.require("skin").then(function(){MyAMS.skin.loadURL(t.amsUrl,n.attr("href")).then(function(){t.amsTabLoadOnce&&(t.amsTabLoaded=!0),f("i",n).remove()},function(){f("i",n).remove()})})))}),MyAMS.config.isMobile?(MyAMS.dom.root.addClass("mobile-detected"),MyAMS.require("ajax").then(function(){MyAMS.config.enableFastclick&&MyAMS.ajax.check(f.fn.noClickDelay,"".concat(MyAMS.env.baseURL,"../ext/js-smartclick").concat(MyAMS.env.extext,".js")).then(function(){f("a",MyAMS.dom.nav).noClickDelay(),f("a","#hide-menu").noClickDelay()}),MyAMS.dom.root.exists()&&MyAMS.ajax.check(window.Hammer,"".concat(MyAMS.env.baseURL,"../ext/hammer").concat(MyAMS.env.extext,".js")).then(function(){(p=new Hammer.Manager(MyAMS.dom.root.get(0))).add(new Hammer.Pan({direction:Hammer.DIRECTION_HORIZONTAL,threshold:200})),p.on("panright",function(){MyAMS.dom.root.hasClass("hidden-menu")||MyAMS.nav.switchMenu()}),p.on("panleft",function(){MyAMS.dom.root.hasClass("hidden-menu")&&MyAMS.nav.switchMenu()})})})):MyAMS.dom.root.addClass("desktop-detected")),y.restoreState())},initElement:function(e){f("nav",e).navigationMenu({speed:MyAMS.config.menuSpeed})},setActiveMenu:function(e){var n,t=MyAMS.dom.nav;f(".active",t).removeClass("active"),e.addClass("open").addClass("active"),e.parents("li").addClass("open active").children("ul").addClass("active").show(),e.parents("li:first").removeClass("open"),e.parents("ul").addClass(e.attr("href").replace(/^#/,"")?"active":"").show(),e.exists()&&(n=t.scrollTop(),((e=f(e).parents("li:last").position()).top<n||e.top>t.height()+n)&&t.scrollTop(e.top))},drawBreadcrumbs:function(){var e,a=f("ol.breadcrumb","#ribbon");f("li",a).not(".persistent").remove(),f("li",a).exists()||(e='<li class="breadcrumb-item">\n\t\t\t\t\t<a class="p-r-1" href="'.concat(f('a[href!="#"]:first',MyAMS.dom.nav).attr("href"),'">\n\t\t\t\t\t\t').concat(MyAMS.i18n.HOME,"\n\t\t\t\t\t</a>\n\t\t\t\t</li>"),a.append(f(e))),f("li.active >a",MyAMS.dom.nav).each(function(e,n){var t=f(n),n=f.trim(t.clone().children(".badge").remove().end().text()),t=t.attr("href"),n=f('<li class="breadcrumb-item"></li>').append(t.replace(/^#/,"")?f("<a></a>").html(n).attr("href",t):n);a.append(n)})},minifyMenu:function(e){e&&e.preventDefault(),MyAMS.dom.root.toggleClass("minified"),MyAMS.dom.root.hasClass("minified")?MyAMS.core.switchIcon(f("i",e.currentTarget),"arrow-circle-left","arrow-circle-right"):MyAMS.core.switchIcon(f("i",e.currentTarget),"arrow-circle-right","arrow-circle-left"),window.localStorage&&(MyAMS.dom.root.hasClass("minified")?localStorage.setItem("window-state","minified"):localStorage.setItem("window-state",""))},switchMenu:function(e){e&&e.preventDefault(),MyAMS.dom.root.toggleClass("hidden-menu"),window.localStorage&&(MyAMS.dom.root.hasClass("hidden-menu")?localStorage.setItem("window-state","hidden-menu"):localStorage.setItem("window-state",""))},restoreState:function(){var e;window.localStorage&&("minified"===(e=localStorage.getItem("window-state"))?MyAMS.nav.minifyMenu({currentTarget:f("#minifyme"),preventDefault:function(){}}):MyAMS.dom.root.addClass(e))}};e.nav=y,MyAMS.env.bundle?MyAMS.config.modules.push("nav"):(MyAMS.nav=y,console.debug("MyAMS: nav module loaded..."))});