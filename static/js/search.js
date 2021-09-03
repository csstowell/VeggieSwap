

// Code goes here
$(document).ready(function () {
    $("#searchForm").submit(function (event) {
        // Stop form from submitting normally
        event.preventDefault();

        // Get some values from elements on the page:
        var $form = $(this),
            term = $form.find("produce[name='s']").val(),
            url = $form.attr("action");

        // Send the data using post

        var posting = $.post(
            url, {
            s: term
        },
            myPostWasSuccessful,
            'html'
        );
    });
});

function myPostWasSuccessful(data, textStatus, jqXHR) {
    $("#result").html(data);
}