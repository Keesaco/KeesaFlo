$("#help-force-start").click(helpForceStart);
ksfToogleLink.addToogleFilesListener();

//Launched when a new file pagelet is fetched
filePreviewStart = function() {
	ksfCanvas.addListener();
	$("#file-selector-open").click(ksfToogleLink.toogleFileSelector);
}