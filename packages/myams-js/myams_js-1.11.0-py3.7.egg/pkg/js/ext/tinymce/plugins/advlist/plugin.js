/**
 * Copyright (c) Tiny Technologies, Inc. All rights reserved.
 * Licensed under the LGPL or a commercial license.
 * For LGPL see License.txt in the project root for license information.
 * For commercial licenses see https://www.tiny.cloud/
 *
 * Version: 5.6.2 (2020-12-08)
 */
!function(){"use strict";var n,e,t,r=tinymce.util.Tools.resolve("tinymce.PluginManager"),u=function(n,e,t){var r="UL"===e?"InsertUnorderedList":"InsertOrderedList";n.execCommand(r,!1,!1===t?null:{"list-style-type":t})},l=tinymce.util.Tools.resolve("tinymce.util.Tools"),i=function(n){return function(){return n}},c=i(!1),s=i(!0),o=function(){return a},a=(n=function(n){return n.isNone()},{fold:function(n,e){return n()},is:c,isSome:c,isNone:s,getOr:t=function(n){return n},getOrThunk:e=function(n){return n()},getOrDie:function(n){throw new Error(n||"error: getOrDie called on none.")},getOrNull:i(null),getOrUndefined:i(undefined),or:t,orThunk:e,map:o,each:function(){},bind:o,exists:c,forall:s,filter:o,equals:n,equals_:n,toArray:function(){return[]},toString:i("none()")}),f=function(t){var n=i(t),e=function(){return o},r=function(n){return n(t)},o={fold:function(n,e){return e(t)},is:function(n){return t===n},isSome:s,isNone:c,getOr:n,getOrThunk:n,getOrDie:n,getOrNull:n,getOrUndefined:n,or:e,orThunk:e,map:function(n){return f(n(t))},each:function(n){n(t)},bind:r,exists:r,forall:r,filter:function(n){return n(t)?o:a},toArray:function(){return[t]},toString:function(){return"some("+t+")"},equals:function(n){return n.is(t)},equals_:function(n,e){return n.fold(c,function(n){return e(t,n)})}};return o},d=function(n){return null===n||n===undefined?a:f(n)},g=function(n){return n&&/^(TH|TD)$/.test(n.nodeName)},m=function(r){return function(n){return n&&/^(OL|UL|DL)$/.test(n.nodeName)&&(t=n,(e=r).$.contains(e.getBody(),t));var e,t}},p=function(n,e,t){var r=function(n,e){for(var t=0;t<n.length;t++){if(e(n[t]))return t}return-1}(e.parents,g),o=-1!==r?e.parents.slice(0,r):e.parents,i=l.grep(o,m(n));return 0<i.length&&i[0].nodeName===t},y=function(o,n,e,t,r,i){o.ui.registry.addSplitButton(n,{tooltip:e,icon:"OL"===r?"ordered-list":"unordered-list",presets:"listpreview",columns:3,fetch:function(n){n(l.map(i,function(n){return{type:"choiceitem",value:"default"===n?"":n,icon:"list-"+("OL"===r?"num":"bull")+"-"+("disc"===n||"decimal"===n?"default":n),text:n.replace(/\-/g," ").replace(/\b\w/g,function(n){return n.toUpperCase()})}}))},onAction:function(){return o.execCommand(t)},onItemAction:function(n,e){u(o,r,e)},select:function(e){var n,t,r;return(t=(n=o).dom.getParent(n.selection.getNode(),"ol,ul"),r=n.dom.getStyle(t,"listStyleType"),d(r)).map(function(n){return e===n}).getOr(!1)},onSetup:function(e){var n=function(n){e.setActive(p(o,n,r))};return o.on("NodeChange",n),function(){return o.off("NodeChange",n)}}})},v=function(n,e,t,r,o,i){var u,l,c,s,a;1<i.length?y(n,e,t,r,o,i):(l=e,c=t,s=r,a=o,(u=n).ui.registry.addToggleButton(l,{active:!1,tooltip:c,icon:"OL"===a?"ordered-list":"unordered-list",onSetup:function(e){var n=function(n){e.setActive(p(u,n,a))};return u.on("NodeChange",n),function(){return u.off("NodeChange",n)}},onAction:function(){return u.execCommand(s)}}))};r.add("advlist",function(n){var t,e,r,o;n.hasPlugin("lists")&&(v(e=n,"numlist","Numbered list","InsertOrderedList","OL",(r=e.getParam("advlist_number_styles","default,lower-alpha,lower-greek,lower-roman,upper-alpha,upper-roman"))?r.split(/[ ,]/):[]),v(e,"bullist","Bullet list","InsertUnorderedList","UL",(o=e.getParam("advlist_bullet_styles","default,circle,square"))?o.split(/[ ,]/):[]),(t=n).addCommand("ApplyUnorderedListStyle",function(n,e){u(t,"UL",e["list-style-type"])}),t.addCommand("ApplyOrderedListStyle",function(n,e){u(t,"OL",e["list-style-type"])}))})}();