$("#help-force-start").click(helpForceStart);
ksfToggleLink.addToggleFilesListener();


/*
* \fn filePreviewStart()
* \brief Contains all the code to run after a new graph is fetched 
* \author mrudelle@keesaco.com of Keesaco
*/
filePreviewStart = function() {
	ksfCanvas.addListener();
	$("#file-selector-open").click(ksfToggleLink.toggleFileSelector);
}