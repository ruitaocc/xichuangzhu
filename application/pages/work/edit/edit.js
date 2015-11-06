(function () {
    "use strict";

    $('.btn-search-wiki').click(function () {
        window.open("http://baike.baidu.com/search?word={{ work.title }}{% if work.title_suffix %}{{ work.title_suffix }}{% endif %}");
    });
})();
