$("#help-force-start").click(helpForceStart);


//Launched when a new file pagelet is fetched
filePreviewStart = function() {
	ksfCanvas.addListener();
	$("#file-selector-open").click(ksfToogleLink.toogleFileSelector);
}