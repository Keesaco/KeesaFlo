$(function() {
    $('.toggletools').click(function() {
        var $marginLefty = $('#sidebar2');
        $marginLefty.animate({
            marginLeft: parseInt($marginLefty.css('marginLeft'), 10) == 0 ?
                -$marginLefty.outerWidth() : 0
        });  
    });
});