/**
 *
 */
 $(document).ready(function() {
    $('#dept_time').timepicker();

    $('#dept_time').change(function(){
    	var dept_time = $(this).val();
    	var dist = $('#dist').val();
    	var arrv_time = dept_time + dist;

    	$('#arrv_time').val(arrv_time);
    });
    $('#airline').change(function(){
    	$('#comp_abb').text($(this).children('option:selected').attr('data-abb'));
    });
 });