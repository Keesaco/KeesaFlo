$(function() {
    var $marginLefty = $('#sidebar2');
    var $marginPanel = $('.apppanel');
    $('.toggletools').click(function() {
        $marginLefty.animate({
            marginLeft: parseInt($marginLefty.css('marginLeft'), 10) == 0 ?
                -$marginLefty.outerWidth() : 0
        });
        $marginPanel.animate({
            marginLeft: parseInt($marginPanel.css('marginLeft'), 10) == 0 ?
                $marginLefty.outerWidth() : 0
        });
    });
    $(window).resize(function() {
        var $browserWidth = $(window).width();
        if($browserWidth > 767 && parseInt($marginLefty.css('marginLeft'), 10) == 0) {
            $marginPanel.css({
                marginLeft: '0'
            });
        }
        else if($browserWidth > 767) {
            $marginLefty.css({
                marginLeft: '0'
            });
        }
        else {
            $marginLefty.css({
                marginLeft: -$marginLefty.outerWidth()
            });
        }
    });
});