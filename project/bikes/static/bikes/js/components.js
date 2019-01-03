$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        var pk =  btn.data("pk");
        var row = (pk >= 1) ? "#row_id_" + pk : "thead";

        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $(row).hide()
                $(row).after(data.html_form)
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        var pk = form.data("pk");
        var row = (pk >= 1) ? "#row_id_" + pk : "thead";
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#edit-form').remove()
                    $("#components-table tbody").html(data.html_list);
                }
                else {
                    $('#edit-form').remove();
                    $(row).after(data.html_form);
                }
            }
        });
        return false;
    };


    var closeForm = function () {
        var form = $(this);
        var pk = form.data("pk");
        var row = (pk >= 1) ? "#row_id_" + pk : "thead";
        $('#edit-form').remove();
        $(row).show();
    };


    /* Binding */

    // Create
    $(".js-create").click(loadForm);
    $("#component-tbody").on("submit", ".js-create-form", saveForm);

    // Update
    $("#component-tbody").on("click", ".js-update", loadForm);
    $("#component-tbody").on("click", ".js-close", closeForm);
    $("#component-tbody").on("submit", ".js-update-form", saveForm);

    // Delete
    $("#component-tbody").on("click", ".js-delete", loadForm);
    $("#component-tbody").on("submit", ".js-delete-form", saveForm);

});
