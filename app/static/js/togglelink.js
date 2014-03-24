function ksfToogleLink() {
}

FILE_SIDE_BAR = '#sidebar';

ksfToogleLink.fileSelector;

$(function(){
    ksfToogleLink.fileSelector = $(FILE_SIDE_BAR);
    ksfToogleLink.addToogleFilesListener();
    $(window).resize(function() {
        if(parseInt(ksfToogleLink.fileSelector.css('marginRight'), 10) < 0) {
            ksfToogleLink.fileSelector.css({
                marginRight: -ksfToogleLink.fileSelector.outerWidth()
            });
        }
    });
});

ksfToogleLink.fileSelector = function()
{
    ksfToogleLink.fileSelector.animate({
        marginRight: 0
    });
}

ksfToogleLink.toogleFileSelector = function()
{
    ksfToogleLink.fileSelector.animate({
        marginRight: parseInt(ksfToogleLink.fileSelector.css('marginRight'), 10) == 0 ?
        -ksfToogleLink.fileSelector.outerWidth() : 0
    });
    var browserWidth = $(window).width();
    if(browserWidth <= 767 && parseInt(ksfToogleLink.fileSelector.css('marginRight'), 10) < 0) {
        $('#dropdownmenu').toggleClass('collapse');
        $('#dropdownmenu').toggleClass('in');
    }
}

ksfToogleLink.addToogleFilesListener = function() 
{
    $('.togglefiles').click(ksfToogleLink.toogleFileSelector);
}

