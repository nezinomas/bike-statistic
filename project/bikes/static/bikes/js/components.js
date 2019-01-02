$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-book .modal-content").html("");
                $("#modal-book").modal("show");
            },
            success: function (data) {
                $("#modal-book .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#components-table tbody").html(data.html_list);
                    $("#modal-book").modal("hide");
                }
                else {
                    $("#modal-book .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create book
    $(".js-create").click(loadForm);
    $("#modal-book").on("submit", ".js-create-form", saveForm);

    // Update book
    $("#components-table").on("click", ".js-update", loadForm);
    $("#modal-book").on("submit", ".js-update-form", saveForm);

    // Delete book
    $("#components-table").on("click", ".js-delete", loadForm);
    $("#modal-book").on("submit", ".js-delete-form", saveForm);

});
