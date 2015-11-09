(function () {
    "use strict";

    var $workInput = $page('.input-work-title').first();
    var $btnAddWork = $page('.btn-add-work').first();
    var $workSelect = $page('.work-select').first();

    $workInput.keyup(function (event) {
        if (event.keyCode == 13) {
            var workTitle = $.trim($workInput.val());

            $.ajax({
                url: urlFor('work.search'),
                method: 'POST',
                data: {
                    'title': workTitle
                }
            }).done(function (response) {
                if (response.result) {
                    $workSelect.empty();

                    $.each(response.works, function (index, work) {
                        var option = "<option value=" + work['id'] + ">〔" + work['author'] + '〕'
                            + work['title'] + "</option>";
                        $(option).appendTo($workSelect);
                    });
                }
            });
        }
    });

    $btnAddWork.click(function () {
        $.ajax({
            url: urlFor('collection.do_add_work', {uid: g.collectionId}),
            method: 'POST',
            data: {
                'work_id': $workSelect.val()
            }
        }).done(function (response) {
            if (response.result) {
                location.reload(true);
            }
        });
    });
})();
