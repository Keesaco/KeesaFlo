$(function() {
    $('.togglefiles').click(function() {
        $(this).attr('href', $(this).attr('href') == '#' ? '#sidebar' : '#');
    });
});