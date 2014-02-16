$(function() {
    var $marginRighty = $('#sidebar');
    $('.togglefiles').click(function() {
        $marginRighty.animate({
            marginRight: parseInt($marginRighty.css('marginRight'), 10) == 0 ?
                -$marginRighty.outerWidth() : 0
        });  
    });
    $(window).resize(function() {
        if(parseInt($marginRighty.css('marginRight'), 10) < 0) {
            $marginRighty.css({
                marginRight: -$marginRighty.outerWidth()
            });
        }
    });
});