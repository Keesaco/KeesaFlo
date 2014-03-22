$(function(){
	var $marginRighty = $('#sidebar');
	$('.togglefiles').click(function(){
		$marginRighty.animate({
			marginRight: parseInt($marginRighty.css('marginRight'), 10) == 0 ?
			-$marginRighty.outerWidth() : 0
		});
		var $browserWidth = $(window).width();
		if($browserWidth <= 767 && parseInt($marginRighty.css('marginRight'), 10) < 0) {
			$('#dropdownmenu').toggleClass('collapse');
			$('#dropdownmenu').toggleClass('in');
		}
	});
	$(window).resize(function() {
		if(parseInt($marginRighty.css('marginRight'), 10) < 0) {
			$marginRighty.css({
				marginRight: -$marginRighty.outerWidth()
			});
		}
	});
});

function fileSelector()
{
	$('#sidebar').animate({
		marginRight: 0
	});
}

