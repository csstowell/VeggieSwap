$(document).ready(function () {
    $('.edit-modal-opener').click(function () {
        var url = $(this).data('whatever');
        $.get(url, function (data) {
            $('#Modal .modal-content').html(data);
            $('#Modal').modal();
            $('#submit').click(function (event) {
                event.preventDefault();
                $.post(url, data = $('#ModalForm').serialize(), function (
                    data) {
                    if (data.status == 'ok') {
                        $('#Modal').modal('hide');
                        location.reload();
                    } else {
                        var obj = JSON.parse(data);
                        for (var key in obj) {
                            if (obj.hasOwnProperty(key)) {
                                var value = obj[key];
                            }
                        }
                        $('.help-block').remove()
                        $('<p class="help-block">' + value + '</p>')
                            .insertAfter('#' + key);
                        $('.form-group').addClass('has-error')
                    }
                })
            });
        })
    });
});