$(document).ready(function() {
	//console.log('jQuery is ready');
	atoggle = 'forward';
	
	
	// globally turn off all animations
	if(screen.width <= 480) jQuery.fx.off = true
	
	$('.block-2 a').click(function(event) {
    	event.preventDefault();
    	if(atoggle == 'back')  {
    	   atoggle = 'forward';
    	   location.reload();
    	}
    });
	
	$('#col_1').click(function() {
        $('#col_2').fadeOut('slow');
        $('#col_3').fadeOut('slow');
        $('#col_1 a').html('Back');
        atoggle = 'back';
        
        
        setTimeout(function() {
        	$('#result').load('/partial/past')
        	},250);
        
	   });
	   
    $('#col_2').click(function() {
        $('#col_1').hide('slow');
        $('#col_3').hide('slow');
        $('#col_2 a').html('Back');
        atoggle = 'back';
        
        
        setTimeout(function() {
        	$('#result').load('/partial/current')
        	}, 250);    	   
	   
	   });
	   
    $('#col_3').click(function() {
        $('#col_1').hide('slow');
        $('#col_2').hide('slow');
        $('#col_3 a').html('Back');
        atoggle = 'back';
        
        
        setTimeout(function() {
        	$('#result').load('/partial/future')
        	}, 250);    	   
	   
	   });
	   
    
});
