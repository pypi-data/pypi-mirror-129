!function(e,o){"function"==typeof define&&define.amd?define(["exports"],o):"undefined"!=typeof exports?o(exports):(o(o={}),e.modClipboard=o)}("undefined"!=typeof globalThis?globalThis:"undefined"!=typeof self?self:this,function(e){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.clipboard=void 0;var t=MyAMS.$;function n(e){var o=!1;if(window.clipboardData&&window.clipboardData.setData)o=clipboardData.setData("Text",e);else if(document.queryCommandSupported&&document.queryCommandSupported("copy")){var n=t("<textarea>");n.val(e).css("position","fixed").appendTo(MyAMS.dom.root),n.get(0).select();try{document.execCommand("copy"),o=!0}catch(e){console.warn("Clipboard copy failed!",e)}finally{n.remove()}}o?MyAMS.require("i18n","alert").then(function(){MyAMS.alert.smallBox({status:"success",message:1<e.length?MyAMS.i18n.CLIPBOARD_TEXT_COPY_OK:MyAMS.i18n.CLIPBOARD_CHARACTER_COPY_OK,icon:"fa-info-circle",timeout:3e3})}):MyAMS.require("i18n").then(function(){prompt(MyAMS.i18n.CLIPBOARD_COPY,e)})}var o={copy:function(e){if(void 0===e)return function(){var e=t(this),o=e.text();e.parents(".btn-group").removeClass("open"),n(o)};n(e)}};e.clipboard=o,window.MyAMS&&(MyAMS.env.bundle?MyAMS.config.modules.push("clipboard"):(MyAMS.clipboard=o,console.debug("MyAMS: clipboard module loaded...")))});