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
    	$('#arrv_timeh').val(arrv_time);
    }



    $('#dept_time').change(function(){
    	Chg_artime();
    });
    $('#dist').change(function(){
    	Chg_artime();
    });

    $('#airline').change(function(){
    	$('#comp_abb').text($(this).children('option:selected').attr('data-abb'));
    	$('#comp_abbh').val($('#comp_abb').text());
    });

    $('#logofile').change(function() {
        $('#cover').html($(this).val());
    });

    $('#country').change(function(){
    	$.getJSON("/port_list",{country:$(this).children('option:selected').val()}, function(data){
    		var jsonData = data,
    			len = data.length;
    		for(var i = 0; i < len; i++){
    			$('#airport').append($('<option>').html(data[i]).val(data[i]));
    		}
    	});
    });
    $('#fetch_port').click(function(){
    	$.getJSON("/port_list",{port_id:$('#airport').children('option:selected').val(), mode:$('#mode').val()}, function(data){
    		var jsonData = data
    		$('#portname').val(jsonData.portname);
    		$('#portcode').val(jsonData.portcode);
    		$('#location').val(jsonData.location);
    		$('#portid').val($('#airport').children('option:selected').val());
    	});
    });
    $('#fetch_line').click(function(){
    	var company_id = $('#airline').children('option:selected').val();
    	$.getJSON("/airline_list",{company_id:company_id, mode:$('#mode').val()}, function(data){
    		var jsonData = data
    		$('#company_name').val(jsonData.company_name);
    		$('#company_abb').val(jsonData.company_abb);
    		$('#country').val(jsonData.origin_country);
    		$('#logo_img').attr('src','/get_img?key=' + company_id);
    		$('#company_id').val(company_id);
    	});
    });
 });