function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    $(".showinfo").on("click", function ( event ) {
        var name = $(this).attr('id');
        var f = $("form").serialize();
        $.ajax({
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            url: "info/",
            data: {
                item: name,
                form: f,
            },
            success: function( data ){
                document.write(data);
            }
        });
    });
});

$(document).ready( function () {

    $('#table_id').DataTable();
});