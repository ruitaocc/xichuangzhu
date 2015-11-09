(function () {
    "use strict";

    var $workInput = $page('.input-work-title').first();
    var $btnAddWork = $page('.btn-add-work').first();
    var $workSelect = $page('.work-select').first();
    var $worksList = $page('.works-list').first();

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

    $worksList.sortable({
        helper: fixHelper,
        stop: function () {
            var orders = [];

            $worksList.find('tr').each(function (index) {
                var order = parseInt($(this).attr('data-order'));
                var id = parseInt($(this).attr('data-id'));

                if (order !== index) {
                    orders.push({'id': id, 'order': index});
                }
            });

            if (orders.length === 0) {
                return;
            }

            $.ajax({
                url: urlFor('collection.update_works_order'),
                method: 'POST',
                data: {
                    'orders': JSON.stringify(orders)
                }
            }).done(function (response) {
                if (response.result) {
                    $worksList.find('tr').each(function (index) {
                        $(this).attr('data-order', index);
                    });
                }
            });
        }
    }).disableSelection();

    function fixHelper(e, ui) {
        ui.children().each(function () {
            $(this).width($(this).width());
        });
        return ui;
    }
})();
