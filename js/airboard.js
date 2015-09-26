/**
 *
 */
 $(document).ready(function() {
    $('#dept_time').timepicker({
    	template: 'modal',
    	minuteStep: 30,
    	showMeridian: false,
    	showInputs: false
    });

    function Chg_artime(){
    	var dept_time = $('#dept_time').val();
    	var dist = Number($('#dist').val());
    	var depts = dept_time.split(':');
    	var dept_h = Number(depts[0]);
    	var dept_h2 = dept_h + dist;

    	if (dept_h2 > 23){
    		dept_h2 = dept_h2 - 24;
    	}

    	var arrv_time = dept_h2+':'+depts[1];

    	$('#arrv_time').val(arrv_time);
    }

    $('#dept_time').change(function(){
    	Chg_artime();
    });
    $('#dist').change(function(){
    	Chg_artime();
    });

    $('#airline').change(function(){
    	$('#comp_abb').text($(this).children('option:selected').attr('data-abb'));
    });
 });