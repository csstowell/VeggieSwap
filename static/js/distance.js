// SHOW DISTANCE
function showDistance(evt) {
    evt.preventDefault();

    let url = "/exchange/distance/int"
    let formData = {"radius": $("#radius-field").val() };

    $.get(url, formData, function (results) {
        $("#distance-info").html(results.users);
    });
}

$("#distance-form").on('submit', showDistance);