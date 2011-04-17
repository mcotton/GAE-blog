$(document).ready(function() {
	//console.log('jQuery is ready');
	
	$('.block-2 a').click(function(event) {
    	event.preventDefault();
    });
	
	$('#col_1').click(function() {
        $('#col_2').fadeOut('slow');
        $('#col_3').fadeOut('slow');
        
        setTimeout(function() {
        	$('#result').load('/partial/past')
        	}, 500);
        
	   });
	   
    $('#col_2').click(function() {
        $('#col_1').hide('slow');
        $('#col_3').hide('slow');

        setTimeout(function() {
        	$('#result').load('/partial/current')
        	}, 500);    	   
	   
	   });
	   
    $('#col_3').click(function() {
        $('#col_1').hide('slow');
        $('#col_2').hide('slow');
	   
        setTimeout(function() {
        	$('#result').load('/partial/future')
        	}, 500);    	   
	   
	   });
	   
    
});
