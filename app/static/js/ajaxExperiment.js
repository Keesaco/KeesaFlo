function fetchNewFile(filename) {
	xmlhttp=new XMLHttpRequest();
	xmlhttp.onreadystatechange=function()
	  {
	  if (xmlhttp.readyState==4 && xmlhttp.status==200)
	    {
	    	document.getElementById("apppanel").innerHTML=xmlhttp.responseText;
	    }
	  }
	document.getElementById("apppanel").innerHTML="<h1>loading " + filename + "</h1>";
	xmlhttp.open("GET","app?xhr=" + filename,true);
	xmlhttp.send();
}