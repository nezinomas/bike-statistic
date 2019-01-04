$(function () {

    /* Functions */

    var loadFormBtn = function() {
        var btn = $(this);
        loadFormAjax(btn.data("pk"), btn.attr("data-url"));
    };

    var loadFormDblClc = function(pk, url) {
        loadFormAjax(pk, url)
    };

    var loadFormAjax = function(pk, url) {
        if (pk == undefined && url == undefined) {
            return;
        }

        var row = (pk !== undefined) ? `#row_id_${pk}` : "#component-tbody";
        $('#edit-form').remove();
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (row !== "#component-tbody"){
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
        var row = (pk >= 1) ? `#row_id_${pk}` : "#component-tbody";
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#edit-form').remove();
                    $("#components-table tbody").html(data.html_list);
                }
                else {
                    $('#edit-form').remove();
                    if (row !== "#component-tbody") {
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
        loadFormDblClc($(this).data("pk"), $(this).data('url'))
    });

    /* Binding */

    // Create
    $(".js-create").click(loadFormBtn);
    // $("#component-tbody").on("submit", ".js-create-form", saveForm);

    // Update
    $("#component-tbody").on("click", ".js-update", loadFormBtn);
    $("#component-tbody").on("click", ".js-close", closeForm);
    $("#component-tbody").on("submit", ".js-update-form", saveForm);

    // Delete
    $("#component-tbody").on("click", ".js-delete", loadFormBtn);
    $("#component-tbody").on("submit", ".js-delete-form", saveForm);

});
