$(function() {
    $('.toggletools').click(function() {
        var $marginLefty = $('#sidebar2');
        var $marginPanel = $('.apppanel');
        $marginLefty.animate({
            marginLeft: parseInt($marginLefty.css('marginLeft'), 10) == 0 ?
                -$marginLefty.outerWidth() : 0
        });
        $marginPanel.animate({
            marginLeft: parseInt($marginPanel.css('marginLeft'), 10) == 0 ?
                $marginLefty.outerWidth() : 0
        });
    });
});