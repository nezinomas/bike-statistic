/* focus on [autofocus] attribute */
$(document).on('shown.bs.modal', '#modal', function () {
    $(this).find('[autofocus]').focus();
});


htmx.on("htmx:afterSwap", (e) => {
    /* Response targeting #dialog => show the modal */
    if (e.detail.target.id == "dialog") {
        $("#modal").modal("show").draggable({ handle: ".modal-header" });
    }
})


htmx.on("htmx:beforeSwap", (e) => {
    if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        $('#modal').modal('hide');
        e.detail.shouldSwap = false;
    }
})


$(document).on('hidden.bs.modal', '#modal', function () {
    var form = $('.form');
    var trigger_name = form.attr("data-hx-trigger-form");

    if (trigger_name === 'None' || trigger_name == undefined) {
        return;
    } else {
        htmx.trigger("body", trigger_name, { });
    }
});
