/*! Select2 4.0.13 | https://github.com/select2/select2/blob/master/LICENSE.md */

!function(){if(jQuery&&jQuery.fn&&jQuery.fn.select2&&jQuery.fn.select2.amd)var n=jQuery.fn.select2.amd;n.define("select2/i18n/pl",[],function(){var n=["znak","znaki","znaków"],e=["element","elementy","elementów"],r=function(n,e){return 1===n?e[0]:n>1&&n<=4?e[1]:n>=5?e[2]:void 0};return{errorLoading:function(){return"Nie można załadować wyników."},inputTooLong:function(e){var t=e.input.length-e.maximum;return"Usuń "+t+" "+r(t,n)},inputTooShort:function(e){var t=e.minimum-e.input.length;return"Podaj przynajmniej "+t+" "+r(t,n)},loadingMore:function(){return"Trwa ładowanie…"},maximumSelected:function(n){return"Możesz zaznaczyć tylko "+n.maximum+" "+r(n.maximum,e)},noResults:function(){return"Brak wyników"},searching:function(){return"Trwa wyszukiwanie…"},removeAllItems:function(){return"Usuń wszystkie przedmioty"}}}),n.define,n.require}();