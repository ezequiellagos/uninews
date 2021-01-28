$(document).ready(function() {

    // Si no encuentra una imagen la reemplaza
    $(".no-image").on("error", function() {
        $(this).attr('src', '/static/img/no-image.png');
    });

    // Si no tiene fuente src, la reemplaza
    const images = document.querySelectorAll('.no-image');
    images.forEach((image) => {
    let src = image.getAttribute('src');
    if (src === '') image.src = '/static/img/no-image.png';
    });

    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('#back-to-top').fadeIn();
        } else {
            $('#back-to-top').fadeOut();
        }

    });

    // scroll body to 0px on click
    $('#back-to-top').click(function() {
        $('#back-to-top').tooltip('hide');
        $('body,html').animate({
            scrollTop: 0
        }, 800);
        return false;
    });

    $("#back-to-top").mouseover(function() {
        $('#back-to-top').tooltip('show');
    });
});

var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function() {
        $('.loading').show();
    },
    onAfterPageLoad: function($items) {
        $('.loading').hide();

        // Si no encuentra una imagen la reemplaza
        $(".no-image").on("error", function() {
            $(this).attr('src', '/static/img/no-image.png');
        });
    }
});
