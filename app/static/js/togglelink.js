/*
 * \file app/static/js/togglelink.js
 * \brief JavaScript library to manage toggling the file selector panel
 * \author mrudelle@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 */

/*
* \fn ksfGraphTools()
* \brief ksfToggleLink constructor used for namespace
* \author mrudelle@keesaco.com of Keesaco
* \note This constructor currently (intentionally) does not have any effect
*/
function ksfToggleLink() {
}

FILE_SIDE_BAR = '#sidebar';

ksfToggleLink.fileSelector;

/*
* \fn ksfToggleLink.fileSelector
* \brief Oppens the file selector panel
* \author swhitehouse@keesaco.com of Keesaco
*/
ksfToggleLink.fileSelector = function()
{
    ksfToggleLink.fileSelector.animate({
        marginRight: 0
    });
}

/*
* \fn ksfToggleLink.toggleFileSelector
* \brief Toggle the file selector panel
* \author hdoughty@keesaco.com of Keesaco
* \author mrudelle@keesaco.com of Keesaco
*/
ksfToggleLink.toggleFileSelector = function()
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

/*
* \fn ksfToggleLink.addToggleFilesListener
* \brief Adds the listener to toggle the file selector panel 
* \author hdoughty@keesaco.com of Keesaco
* \author mrudelle@keesaco.com of Keesaco
*/
ksfToggleLink.addToggleFilesListener = function() 
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

