/*
 * \file app/static/js/togglelink.js
 * \brief JavaScript library to manage toggling the file selector panel
 * \author mrudelle@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 */

/*
* constructor used for namespace
* \author mrudelle@keesaco.com of Keesaco
* \note This constructor currently (intentionally) does not have any effect
*/
function ksfToggleLink() {
}

FILE_SIDE_BAR = '#sidebar';

ksfToggleLink.fileSelector;

/*
* Oppens the file selector panel
* \author swhitehouse@keesaco.com of Keesaco
*/
ksfToggleLink_fileSelector = function()
{
    ksfToggleLink.fileSelector.animate({
        marginRight: 0
    });
}
ksfToggleLink.fileSelector = ksfToggleLink_fileSelector;


/*
* Toggle the file selector panel
* \author hdoughty@keesaco.com of Keesaco
* \author mrudelle@keesaco.com of Keesaco
*/
ksfToggleLink_toggleFileSelector = function()
{
    ksfToggleLink.fileSelector.animate({
        marginRight: parseInt(ksfToggleLink.fileSelector.css('marginRight'), 10) == 0 ?
        -ksfToggleLink.fileSelector.outerWidth() : 0
    });
    var browserWidth = $(window).width();
    if(browserWidth <= 767 && parseInt(ksfToggleLink.fileSelector.css('marginRight'), 10) < 0) {
        $('#dropdownmenu').toggleClass('collapse');
        $('#dropdownmenu').toggleClass('in');
    }
}
ksfToggleLink.toggleFileSelector = ksfToggleLink_toggleFileSelector;


/*
* Adds the listener to toggle the file selector panel 
* \author hdoughty@keesaco.com of Keesaco
* \author mrudelle@keesaco.com of Keesaco
*/
ksfToggleLink_addToggleFilesListener = function() 
{
    ksfToggleLink.fileSelector = $(FILE_SIDE_BAR);
    $('.togglefiles').click(ksfToggleLink.toggleFileSelector);

    $(window).resize(function() {
        if(parseInt(ksfToggleLink.fileSelector.css('marginRight'), 10) < 0) {
            ksfToggleLink.fileSelector.css({
                marginRight: -ksfToggleLink.fileSelector.outerWidth()
            });
        }
    });
}
ksfToggleLink.addToggleFilesListener = ksfToggleLink_addToggleFilesListener;

