$(function() {
    $('.togglefiles').click(function() {
        var $marginRighty = $('#sidebar');
        $marginRighty.animate({
            marginRight: parseInt($marginRighty.css('marginRight'), 10) == 0 ?
                -$marginRighty.outerWidth() : 0
        });  
    });
});