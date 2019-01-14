$(function () {

    /* Functions */

    var loadFormBtn = function() {
        var btn = $(this);
        loadFormAjax(btn.data("tbl"), btn.data("pk"), btn.attr("data-url"));
    };

    var loadFormDblClc = function(tbl, pk, url) {
        loadFormAjax(tbl, pk, url)
    };

    var loadFormAjax = function(tbl, pk, url) {
        if (pk == undefined && url == undefined) {
            return;
        }

        var row = (pk !== undefined) ? `#row_id_${pk}` : `#tbl-${tbl}`;
        $('#edit-form').remove();
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (row !== `#tbl-${tbl}`){
                    $(row).hide();
                    $(row).after(data.html_form);
                }
                else {
                    $(row).prepend(data.html_form);
                }
            }
        });
    };

    var saveForm = function() {
        var form = $(this);
        var pk = form.data("pk");
        var tbl = form.data("tbl")
        var row = (pk >= 1) ? `#row_id_${pk}` : `#tbl-${tbl}`;
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#edit-form').remove();
                    $(`#tbl-${tbl}`).html(data.html_list);
                }
                else {
                    $('#edit-form').remove();
                    if (row !== `#tbl-${tbl}`) {
                        $(row).after(data.html_form);
                    }
                    else {
                        $(row).prepend(data.html_form);
                    }
                }
            }
        });
        return false;
    };

    var closeForm = function () {
        $('#edit-form').remove();
        var form = $(this);
        var pk = form.data("pk");
        var row = (pk >= 1) ? "#row_id_" + pk : "thead";
        $(row).show();
    };

    $('tr').dblclick(function () {
        loadFormDblClc($(this).data("tbl"), $(this).data("pk"), $(this).data('url'))
    });

    /* Binding */

    // Create
    $(".js-create").click(loadFormBtn);
    // $(`#tbl-${tbl}`).on("submit", ".js-create-form", saveForm);

    // Update
    $(".tbl-js").on("click", ".js-update", loadFormBtn);
    $(".tbl-js").on("click", ".js-close", closeForm);
    $(".tbl-js").on("submit", ".js-update-form", saveForm);

    // Delete
    $(".tbl-js").on("click", ".js-delete", loadFormBtn);
    $(".tbl-js").on("submit", ".js-delete-form", saveForm);

});
