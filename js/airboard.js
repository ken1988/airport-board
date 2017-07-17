/**
 *
 */
 $(document).ready(function() {
	 Initcanv();
	$('#dept_time').timepicker({
    	template: 'modal',
    	minuteStep: 30,
    	showMeridian: false,
    	showInputs: false
    });
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

    $('.apdez').on('click',function(){
    	var portid = $(this).attr('id');
    	$.get('/port_designer',
    			{id: portid},
    			function(data){
	    		$('#port_design').html(data);
	    		Initcanv();

	    		 $('.Runway').each(function(){
	    			 var px = $(this).data('pointx');
	    			 var py = $(this).data('pointy');
	    			 var dist = $(this).data('distance');
	    			 var degree = $(this).data('degree');
	    			 var id = $(this).attr('id');

	    			 dist = dist / 20;

	    			 Myimage(px,py,dist,degree);
	    		 });
    		});
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

    function Myimage(px,py,dist,degree){
  	  /* canvas要素のノードオブジェクト */
  	  var canvas = document.getElementById('port_map');
  	  /* canvas要素の存在チェックとCanvas未対応ブラウザの対処 */
  	  if ( ! canvas || ! canvas.getContext ) {
  	    return false;
  	  }
  	  /* 2Dコンテキスト */
  	  var ctx = canvas.getContext('2d');
  	  /* 四角を描く */
  	  ctx.strokeStyle = "gray";
  	  ctx.fillStyle = "gray";

  	  ctx.rotate( degree * Math.PI / 180 );
  	  ctx.strokeRect(px, py, dist, 10);
  	  ctx.fillRect(px, py, dist, 10);
  	  ctx.rotate( -degree * Math.PI / 180 );
    }

    function Initcanv(){
  	  /* canvas要素のノードオブジェクト */
  	  var canvas = document.getElementById('port_map');
  	  /* canvas要素の存在チェックとCanvas未対応ブラウザの対処 */
  	  if ( ! canvas || ! canvas.getContext ) {
  	    return false;
  	  }
  	  /* 2Dコンテキスト */
  	  var ctx = canvas.getContext('2d');
  	  ctx.fillStyle = "green";
  	  ctx.fillRect(0, 0, 300, 300);
    }
 });