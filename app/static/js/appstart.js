/*
 * \file app/static/js/appstart.js
 * \brief Sets the hook on the page and pagelet when they are fetched
 * \author jmccrea@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 */

 $("#help-tour-begin").click(function() { helpTourBegin(true); });
 

qTipOptions =
{
style: 		{ classes: 'qtip-bootstrap qtip-shadow qtip-rounded' },
position: 	{ container: $('div.tooltips') }
};
$(document).ready(function()
{
	ksfViews.loadFromLocation(true)
				  
	$("#ksf-help-begin").click(function() { ksfHelp.mainTourBegin(true); } );
	ksfLayout.addToggleHook();

	$('.togglefiles').click(ksfLayout.toggleFileSelector);
	$('.toggletools').click(ksfLayout.toggleToolBar);
	
	
	tipSelector = $('[title!=""]').not('.notip');
	[	{ name: '.tip-right',	ext: { position: {my: 'center left', at: 'center right' } } },
		{ name: '.tip-left', 	ext: { position: {my: 'center right', at: 'center left' } } },
		{ name: '.tip-top', 	ext: { position: {my: 'bottom center', at: 'top center' } } },
		{ name: '.tip-bottom', 	ext: { position: {my: 'top center', at: 'bottom center' } } } ]
		.forEach( function(t) {
			tipSelector.filter(t.name).qtip($.extend(true, {}, qTipOptions, t.ext ) );
		} );

});