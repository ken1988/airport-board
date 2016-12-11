/**
 *
 */

 $(document).ready(function() {
	    function Myimage(){
	        var circle = document.getElementById('circle');
	        var ctx = circle.getContext('2d');
	        ctx.beginPath();
	        ctx.arc(50,50,50,0,Math.PI*2,true);
	        ctx.fillStyle = "#ff0000";
	        ctx.fill();
	    }
	    $('#updCanv').click(function(){
	    	Myimage();
	    });
 });